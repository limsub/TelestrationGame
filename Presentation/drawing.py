import pygame
import time
import hand_tracking  
import config
from Utils import font_manager, image_manager
import os


ERASER_SIZE = 20
PEN_SIZE = 10

DRAW_COLOR = config.BLACK
ERASER_COLOR = (0, 0, 0, 0)

count_font = font_manager.get_font(36, "bold")
mode_font = font_manager.get_font(40, "bold")

empty_screen = image_manager.empty_screen_image

async def run(screen, total_time):
    # canvas(Surface)에다가 그림
    # canvas = pygame.Surface((screen.get_width(), screen.get_height()))
    # canvas.fill(config.WHITE)

    canvas = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    canvas.fill((0, 0, 0, 0))

    prev_x, prev_y = None, None

    drawing = False
    eraser_mode = False
    last_toggle_time = 0

    start_time = time.time()

    clock = pygame.time.Clock()
    running = True

    enableDrawing = False

    while running:
        # time over
        elapsed_time = time.time() - start_time
        remaining_time = max(0, total_time - int(elapsed_time))
        if remaining_time <= 0:
            break 
        
        # enable drawing
        if elapsed_time > 0.5:
            enableDrawing = True

        # hand tracking
        hand_data, cursor_x, cursor_y = hand_tracking.detect_hand_gesture(screen.get_width(), screen.get_height())

        current_time = time.time()
        if hand_data == config.PEN_ON:
            drawing = True
        elif hand_data == config.PEN_TOGGLE:
            # 토글에 1초 필요
            if current_time - last_toggle_time > 1:
                eraser_mode = not eraser_mode
                last_toggle_time = current_time
        else:
            drawing = False


        # drawing
        if prev_x is not None and prev_y is not None:
            if drawing and enableDrawing: 
                if eraser_mode:
                    pygame.draw.circle(canvas, ERASER_COLOR, (cursor_x, cursor_y), ERASER_SIZE)
                else:
                    pygame.draw.line(canvas, DRAW_COLOR, (prev_x, prev_y), (cursor_x, cursor_y), PEN_SIZE)


        prev_x = cursor_x
        prev_y = cursor_y

        # UI Component
        screen.blit(empty_screen, (0, 0))
        screen.blit(canvas, (0, 0))

        if hand_data == config.PEN_ON:
            pygame.draw.circle(screen, config.BLUE if eraser_mode else config.BLACK, (cursor_x, cursor_y), 20)
        elif hand_data == config.ERASE_ALL:
            canvas.fill((0, 0, 0, 0))
            pygame.draw.circle(screen, config.BLUE, (cursor_x, cursor_y), 0)
        else:
            pygame.draw.circle(screen, config.BLUE if eraser_mode else config.BLACK, (cursor_x, cursor_y), 20, 5)
        
        count_text = count_font.render(f"남은 시간: {remaining_time}s", True, config.BLACK)
        count_rect = count_text.get_rect(center=(screen.get_width() - 120, 100))
        screen.blit(count_text, count_rect)


        pygame.display.update()

    return canvas
        
