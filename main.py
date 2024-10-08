import pygame
import os
import threading
import time
from src.player import Player
from src.weapons import WeaponGroup
from src.obstacles import ObstacleGroup
from src.monster import MonsterGroup
from src.screens import StartScreen, LevelSelectionScreen, GameOverScreen

pygame.init()
pygame.mixer.init()

screen_width, screen_height = 1600, 1000
map_width, map_height = 1921, 1021
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Monster Battle")

game_over_sound = pygame.mixer.Sound(os.path.join('assets', 'gameover.mp3'))
win_sound = pygame.mixer.Sound(os.path.join('assets', 'win.mp3'))
bg_music = pygame.mixer.music.load(os.path.join('assets', "background_music.mp3"))

def play_background_music():
    pygame.mixer.music.play(-1)
    while True:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

background_music_thread = threading.Thread(target=play_background_music)
background_music_thread.daemon = True
background_music_thread.start()

def init(level=1):
    number_monsters = [10, 25, 100]
    monster_speed = [1, 2, 3]
    weapon_health = [5, 10, 50]
    player = Player(screen, 150, 150, 'player_fists1.png')
    obstacles = ObstacleGroup(screen, 'obstacles.png')
    weapons = WeaponGroup(screen, map_width, map_height, 5, obstacles, weapon_health[level-1])
    monsters = MonsterGroup(screen, map_width, map_height, number_monsters[level-1], obstacles, monster_speed[level-1])
    bullets = pygame.sprite.Group()
    return player, weapons, obstacles, monsters, bullets

def main():
    running = True
    clock = pygame.time.Clock()

    player, weapons, obstacles, monsters, bullets = init()

    level_screen = LevelSelectionScreen(screen)
    lost_screen = GameOverScreen(screen, True)
    won_screen = GameOverScreen(screen, False)
    
    game_running = False
    game_over = False
    won = False
    selected_level = False
    level = 1

    while running:
        if game_running:
            screen.fill((150, 100, 50))

            keys = pygame.key.get_pressed()
            player.update(keys, obstacles, weapons, monsters)
            if player.health <= 0:
                game_running = False
                game_over = True
                selected_level = False
                game_over_sound.play()

            weapons.update()
            obstacles.update()

            offset_x = screen_width // 2 - player.rect.centerx
            offset_y = screen_height // 2 - player.rect.centery

            obstacles.draw(offset_x, offset_y)
            weapons.draw(offset_x, offset_y)
            player.update_direction(obstacles, offset_x, offset_y)
            player.draw(offset_x, offset_y)

            monsters.update(bullets, player.rect, obstacles, offset_x, offset_y)
            monsters.draw(offset_x, offset_y)

            bullets.update(obstacles, monsters)
            for bullet in bullets:
                bullet.draw(offset_x, offset_y)
        
        else:
            if game_over and not selected_level:
                if won:
                    won_screen.draw()
                else:
                    lost_screen.draw()
            else:
                level_screen.draw()
        
        if len(monsters.monsters) == 0:
            game_running = False
            game_over = True
            won = True
            selected_level = False
            win_sound.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.weapon and game_running:
                    bullet = player.weapon.shoot(player, pygame.mouse.get_pos(), offset_x, offset_y, map_width, map_height)
                    if bullet is not None: 
                        bullets.add(bullet)

            if not game_running and not selected_level and level_screen.handle_event(event):
                selected_level = True
                level = level_screen.handle_event(event)
                player, weapons, obstacles, monsters, bullets = init(level)
                game_running = True

            if game_over and (lost_screen.handle_event(event) or won_screen.handle_event(event)):
                game_over = False
                won = False
                time.sleep(0.1)
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: 
            running = False

        pygame.display.flip()
        clock.tick(100)

    pygame.quit()

if __name__ == "__main__":
    main()
