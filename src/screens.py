import pygame
import os
pygame.mixer.init()

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 128)
        self.button_font = pygame.font.Font(None, 72)

        w, h = pygame.display.get_surface().get_size()

        self.button_color = (0, 200, 0)
        self.button_hover_color = (0, 255, 0)
        self.button_rect = pygame.Rect(w//2-250, h//2+100, 500, 100)
        self.button_text = "Start"
        
        self.button_hover = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        title_text = self.font.render("Welcome to Monster Battle!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        self.button_hover = self.button_rect.collidepoint(pygame.mouse.get_pos())
        button_color = self.button_hover_color if self.button_hover else self.button_color
        pygame.draw.rect(self.screen, button_color, self.button_rect)
        
        button_text_surface = self.button_font.render(self.button_text, True, (255, 255, 255))
        button_text_rect = button_text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text_surface, button_text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                return True
        return False

class LevelSelectionScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 128)
        self.button_font = pygame.font.Font(None, 72)

        w, h = pygame.display.get_surface().get_size()

        self.button_color = (0, 200, 0)
        self.button_hover_color = (0, 255, 0)
        self.level_1_rect = pygame.Rect(w//2-450-200, h//2, 400, 100)
        self.level_2_rect = pygame.Rect(w//2-200, h//2, 400, 100)
        self.level_3_rect = pygame.Rect(w//2+450-200, h//2, 400, 100)
        
        self.button_hover = None

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        title_text = self.font.render("Welcome to Monster Battle!", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 200))
        self.screen.blit(title_text, title_rect)
        
        self.button_hover = None
        for level, rect in enumerate([self.level_1_rect, self.level_2_rect, self.level_3_rect], start=1):
            hover = rect.collidepoint(pygame.mouse.get_pos())
            if hover:
                self.button_hover = level
            button_color = self.button_hover_color if hover else self.button_color
            pygame.draw.rect(self.screen, button_color, rect)
            
            button_text_surface = self.button_font.render(f"Level {level}", True, (255, 255, 255))
            button_text_rect = button_text_surface.get_rect(center=rect.center)
            self.screen.blit(button_text_surface, button_text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for level, rect in enumerate([self.level_1_rect, self.level_2_rect, self.level_3_rect], start=1):
                if rect.collidepoint(event.pos):
                    return level
        return None

class GameOverScreen:
    def __init__(self, screen, lose=True):
        self.screen = screen
        self.font = pygame.font.Font(None, 128)
        self.button_font = pygame.font.Font(None, 72)
        
        self.button_color = (200, 0, 0) if lose else (0, 200, 0)
        self.button_hover_color = (255, 0, 0) if lose else (0, 255, 0)
        self.button_rect = pygame.Rect(screen.get_width() // 2 - 250, screen.get_height() // 2 + 100, 500, 100)
        self.button_text = "Play Again"
        
        self.button_hover = False
        self.lose = lose

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        game_over_text = self.font.render("You Died!" if self.lose else "You Won!", True, (255, 0, 0) if self.lose else (0, 255, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        self.button_hover = self.button_rect.collidepoint(pygame.mouse.get_pos())
        button_color = self.button_hover_color if self.button_hover else self.button_color
        pygame.draw.rect(self.screen, button_color, self.button_rect)
        
        button_text_surface = self.button_font.render(self.button_text, True, (255, 255, 255))
        button_text_rect = button_text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text_surface, button_text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                return True
        return False

