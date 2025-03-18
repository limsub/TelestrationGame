import asyncio  # 🔥 추가
import pygame
import config
import time
import hand_tracking
from Utils import font_manager, image_manager

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

title_font = font_manager.get_font(40, "bold")
word_font = font_manager.get_font(68, "bold")
count_font = font_manager.get_font(36, "bold")
button_font = font_manager.get_font(40, "bold")

empty_screen = image_manager.empty_screen_image
photo_back_view = image_manager.photo_view_image
next_button = image_manager.next_button_image

BUTTON_WIDTH, BUTTON_HEIGHT = 250, 80
BUTTON_RADIUS = 16
button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT - 120, BUTTON_WIDTH, BUTTON_HEIGHT)

async def run(screen, initial_word, total_time):

    clicked = False 
    start_time = time.time()

    while not clicked:
        # time over
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, total_time - elapsed_time)
        if remaining_time <= 0:
            break

        # UI Components
        screen.blit(empty_screen, (0, 0))

        photo_rect = photo_back_view.get_rect(center=(screen.get_width() // 2, 290))
        screen.blit(photo_back_view, photo_rect) # 768x450
        
        title_text = title_font.render("첫 제시어를 확인하세요", True, config.BLACK)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_text, title_rect)

        word_text = word_font.render(initial_word, True, config.BLACK)
        word_rect = word_text.get_rect(center=photo_rect.center)
        screen.blit(word_text, word_rect)

        count_text = count_font.render(f"남은 시간: {remaining_time}s", True, config.BLACK)
        count_rect = count_text.get_rect(center=(screen.get_width() - 120, 100))
        screen.blit(count_text, count_rect)

        screen.blit(next_button, button_rect.topleft)

        # hand tracking
        hand_data, cursor_x, cursor_y = hand_tracking.detect_hand_gesture(screen.get_width(), screen.get_height())
        if hand_data == config.PEN_ON:
            pygame.draw.circle(screen, config.BLACK, (cursor_x, cursor_y), 15)  # 🔵 파란색으로 채운 원
        else:
            pygame.draw.circle(screen, config.BLACK, (cursor_x, cursor_y), 15, 5)  # ⚪ 파란색 테두리만 있는 원


        # 1초 후부터 버튼 클릭 가능
        if elapsed_time >= 1 and button_rect.collidepoint(cursor_x, cursor_y) and hand_data == config.PEN_ON:
            print("[initial_word_display.py] 버튼 클릭")
            clicked = True
 
        pygame.display.update()
    
    used_time = int(time.time() - start_time)
    return used_time