import asyncio
import pygame
import config
import time
import hand_tracking
from Utils import font_manager, image_manager

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

title_font = font_manager.get_font(40, "bold")
count_font = font_manager.get_font(36, "bold")
button_font = font_manager.get_font(40, "bold")

BUTTON_WIDTH, BUTTON_HEIGHT = 250, 80
BUTTON_RADIUS = 16
button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT - 120, BUTTON_WIDTH, BUTTON_HEIGHT)

IMAGE_WIDTH = 546
IMAGE_HEIGHT = 320

empty_screen = image_manager.empty_screen_image
photo_back_view = image_manager.photo_view_image
next_button = image_manager.next_button_image

async def run(screen, image_surface, total_time, round_num):

    clicked = False 
    start_time = time.time()

    image_surface = pygame.transform.scale(image_surface, (IMAGE_WIDTH, IMAGE_HEIGHT))

    title_text_str = "그림을 보고 정답을 맞춰주세요" if round_num % 2 == 0 else "글씨를 보고 그림을 그려주세요"
    button_text_str = "글씨 적기" if round_num % 2 == 0 else "그림 그리기"


    while not clicked:
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, total_time - elapsed_time)
        if remaining_time <= 0:
            break


        # UI Components
        screen.blit(empty_screen, (0, 0))

        photo_rect = photo_back_view.get_rect(center=(screen.get_width() // 2, 290))
        screen.blit(photo_back_view, photo_rect) # 768x450


        image_rect = image_surface.get_rect(center=(screen.get_width() // 2, 310))
        screen.blit(image_surface, image_rect)

        title_text = title_font.render(title_text_str, True, config.BLACK)
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_text, title_rect)

        screen.blit(next_button, button_rect.topleft)

        count_text = count_font.render(f"남은 시간: {remaining_time}s", True, config.BLACK)
        count_rect = count_text.get_rect(center=(screen.get_width() - 120, 100))
        screen.blit(count_text, count_rect)


        # hand tracking
        hand_data, cursor_x, cursor_y = hand_tracking.detect_hand_gesture(screen.get_width(), screen.get_height())
        if hand_data == config.PEN_ON:
            pygame.draw.circle(screen, config.BLACK, (cursor_x, cursor_y), 15)  
        else:
            pygame.draw.circle(screen, config.BLACK, (cursor_x, cursor_y), 15, 5)


        if button_rect.collidepoint(cursor_x, cursor_y) and hand_data == config.PEN_ON:
            print("[received_image_display.py] 버튼 클릭")
            clicked = True

        pygame.display.update()
    
    used_time = int(time.time() - start_time)
    return used_time
