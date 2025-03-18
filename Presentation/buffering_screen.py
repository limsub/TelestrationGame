import pygame
import time
import config
from Utils import font_manager, image_manager

title_font = font_manager.get_font(48, "bold")

empty_screen = image_manager.empty_screen_image

async def run(screen):

    screen.blit(empty_screen, (0, 0))
    
    # UI Components
    title_text = title_font.render("다른 플레이어들의 그림을 기다리는 중...", True, config.BLACK)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 280))
    screen.blit(title_text, title_rect)

    pygame.display.update()
