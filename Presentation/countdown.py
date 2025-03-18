import pygame
import time
import config
from Utils import font_manager

count_font = font_manager.get_font(150, "bold")
title_font = font_manager.get_font(48, "bold")

async def run(screen):

    for i in range(5, 0, -1):
        screen.fill((0, 0, 0))  # 배경 검은색

        title_text = title_font.render("게임이 곧 시작됩니다", True, config.WHITE)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(title_text, title_rect)

        count_text = count_font.render(str(i), True, config.WHITE)
        count_rect = count_text.get_rect(center=(screen.get_width() // 2, 400))
        screen.blit(count_text, count_rect)

        pygame.display.update()
        time.sleep(1)
