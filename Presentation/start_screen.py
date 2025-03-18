import pygame
import asyncio
import hand_tracking
import json
from Utils import font_manager, image_manager
import config

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

BUTTON_WIDTH, BUTTON_HEIGHT = 250, 80
BUTTON_RADIUS = 16
button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT - 120, BUTTON_WIDTH, BUTTON_HEIGHT)

async def run(screen, ws_client):
    clicked = False

    while not clicked:
        
        screen.blit(image_manager.start_screen_image, (0, 0))
        screen.blit(image_manager.start_button_image, button_rect.topleft)

        # hand tracking
        hand_data, cursor_x, cursor_y = hand_tracking.detect_hand_gesture(SCREEN_WIDTH, SCREEN_HEIGHT)
        # pygame.draw.circle(screen, (0, 0, 255), (cursor_x, cursor_y), 15)

        if hand_data == config.PEN_ON:
            pygame.draw.circle(screen, config.BLACK, (cursor_x, cursor_y), 15)
        else:
            pygame.draw.circle(screen, config.BLACK, (cursor_x, cursor_y), 15, 5)

        # button clicked
        if button_rect.collidepoint(cursor_x, cursor_y) and hand_data == config.PEN_ON:
            clicked = True
            await ws_client.send_message({"action": "start"})  # 서버에 게임 시작 요청 전송

        pygame.display.update()

    return True
