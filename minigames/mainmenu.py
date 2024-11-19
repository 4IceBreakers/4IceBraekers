# main.py
import pygame
import sys
import os
from pacman import PacmanGame
# wntjr
# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("미니게임 컬렉션")

# 색상 정의
WHITE = (255, 255, 255)
LIGHT_BLUE = (135, 206, 235)  # 하늘색
DEEP_SKY_BLUE = (0, 191, 255)
ROYAL_BLUE = (65, 105, 225)
YELLOW = (255, 223, 0)
ORANGE = (255, 140, 0)

# 폰트 설정
if os.name == 'nt':  # Windows
    title_font = pygame.font.SysFont("malgun gothic", 74, bold=True)
    menu_font = pygame.font.SysFont("malgun gothic", 54)
elif os.name == 'posix':  # macOS
    title_font = pygame.font.SysFont("applegothic", 74, bold=True)
    menu_font = pygame.font.SysFont("applegothic", 54)

def draw_gradient_background(surface):
    """그라데이션 배경 그리기"""
    for y in range(SCREEN_HEIGHT):
        # 위에서 아래로 그라데이션
        ratio = y / SCREEN_HEIGHT
        color = [int(LIGHT_BLUE[i] * (1 - ratio) + DEEP_SKY_BLUE[i] * ratio) for i in range(3)]
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.is_hovered = False
        self.original_y = y
        self.hover_offset = 0
        self.animation_speed = 0.5
        
    def draw(self, surface):
        # 그림자 효과
        shadow_rect = self.rect.copy()
        shadow_rect.y += 5
        pygame.draw.rect(surface, (0, 0, 0, 128), shadow_rect, border_radius=15)
        
        # 버튼 본체
        color = [min(255, c + 30) for c in self.color] if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        
        # 하이라이트 효과 (버튼 상단에 밝은 선)
        highlight_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 2)
        pygame.draw.rect(surface, (255, 255, 255, 128), highlight_rect, border_radius=2)
        
        # 텍스트 그리기
        text_surface = menu_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
        # 호버 애니메이션
        if self.is_hovered:
            self.hover_offset = min(self.hover_offset + self.animation_speed, 5)
        else:
            self.hover_offset = max(self.hover_offset - self.animation_speed, 0)
        
        self.rect.y = self.original_y - self.hover_offset
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return self.text
        return None

class MainMenu:
    def __init__(self):
        button_width = 200
        button_height = 50
        start_y = 200
        gap = 70
        
        # 각 버튼에 다른 색상 부여
        self.buttons = [
            Button(SCREEN_WIDTH//2 - button_width//2, start_y, button_width, button_height, 
                  "팩맨", ROYAL_BLUE),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + gap, button_width, button_height, 
                  "캐논", ORANGE),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + gap*2, button_width, button_height, 
                  "메모리", ROYAL_BLUE),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + gap*3, button_width, button_height, 
                  "타일즈", ORANGE),
            Button(SCREEN_WIDTH//2 - button_width//2, start_y + gap*4, button_width, button_height, 
                  "종료", (200, 50, 50))
        ]
        
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                for button in self.buttons:
                    result = button.handle_event(event)
                    if result == "종료":
                        pygame.quit()
                        sys.exit()
                    elif result == "팩맨":
                        pygame.quit()
                        game = PacmanGame()
                        game.run()
                        pygame.init()
                        global screen
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        pygame.display.set_caption("미니게임 컬렉션")
                        return
                    elif result:
                        print(f"{result} 게임 시작!")
            
            # 그라데이션 배경 그리기
            draw_gradient_background(screen)
            
            # 제목 그리기
            title_shadow = title_font.render("미니게임 컬렉션", True, (0, 0, 0))
            title_surface = title_font.render("미니게임 컬렉션", True, YELLOW)
            
            # 그림자
            shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 3, 103))
            screen.blit(title_shadow, shadow_rect)
            
            # 실제 텍스트
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(title_surface, title_rect)
            
            # 버튼 그리기
            for button in self.buttons:
                button.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    while True:
        menu = MainMenu()
        menu.run()