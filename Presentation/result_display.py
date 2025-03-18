import pygame
import asyncio
import hand_tracking
from Utils.image_utils import convert_string_to_surface  
from Utils import font_manager, image_manager
import config

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

IMAGE_WIDTH = 320
IMAGE_HEIGHT = 180

BUTTON_WIDTH, BUTTON_HEIGHT = 250, 80
BUTTON_RADIUS = 16
button_rect = pygame.Rect((SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT - 120, BUTTON_WIDTH, BUTTON_HEIGHT)

answer_text_pos = (240, 65)
result_text_pos = (690, 70)
positions = [(80, 140), (640, 140), (80, 340), (640, 340)]

title_font = font_manager.get_font(40, "bold")

result_screen = image_manager.result_screen_image
next_button = image_manager.next_button_image

# deprecated
BG_COLOR = (255, 255, 255)  # 배경색 (흰색)
IMG_CORNER_RADIUS = 16  # 이미지 코너 반경
BORDER_COLOR = (0, 0, 0)  # 테두리 색 (검은색)
BORDER_WIDTH = 2  # 테두리 두께
CORRECT_COLOR = (0, 200, 0)
INCORRECT_COLOR = (200, 0, 0)


def draw_rounded_image_with_border(screen, img, pos, size, corner_radius=16, border_color=(0, 0, 0), border_width=2):
    # 둥근 모서리 + 테두리 적용 후 이미지 출력"""
    img_rect = pygame.Rect(pos, size)

    # ✅ 테두리용 서피스 생성 (배경 투명)
    border_surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(border_surface, border_color, (0, 0, *size), border_radius=corner_radius, width=border_width)

    # ✅ 둥근 모서리 마스크 생성
    mask = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (border_width, border_width, size[0] - 2 * border_width, size[1] - 2 * border_width), border_radius=corner_radius - border_width)

    # # ✅ 이미지 크기 조정 및 둥근 모서리 적용
    resized_img = pygame.transform.scale(img, size)
    resized_img.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # ✅ 테두리 먼저 출력 → 이미지 출력
    # screen.blit(border_surface, pos)
    screen.blit(resized_img, pos)

async def run(screen, image_strings, correct_answer, result_answer):

    clicked = False

    images = [convert_string_to_surface(img_str) for img_str in image_strings]
    resized_images = [pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_HEIGHT)) for img in images if img]

    is_correct = correct_answer == result_answer
    result_color = CORRECT_COLOR if is_correct else INCORRECT_COLOR

    start_time = pygame.time.get_ticks()

    while not clicked:

        # UI Components
        screen.blit(result_screen, (0, 0))

        answer_text = title_font.render(correct_answer, True, (0, 0, 0))
        screen.blit(answer_text, answer_text_pos)   

        result_text = title_font.render(result_answer, True, (0, 0, 0))
        screen.blit(result_text, result_text_pos)

        for img, pos in zip(resized_images, positions):
            draw_rounded_image_with_border(screen, img, pos, (IMAGE_WIDTH, IMAGE_HEIGHT), corner_radius=IMG_CORNER_RADIUS, border_color=BORDER_COLOR, border_width=BORDER_WIDTH)

        screen.blit(next_button, button_rect.topleft)


        # hand tracking
        hand_data, cursor_x, cursor_y = hand_tracking.detect_hand_gesture(SCREEN_WIDTH, SCREEN_HEIGHT)
        if hand_data == config.PEN_ON:
            pygame.draw.circle(screen, config.BLACK, (cursor_x, cursor_y), 15) 
        else:
            pygame.draw.circle(screen, config.BLACK, (cursor_x, cursor_y), 15, 5) 

        
        elapsed_time = pygame.time.get_ticks() - start_time     # 연속 클릭 방지
        if elapsed_time >= 1000 and button_rect.collidepoint(cursor_x, cursor_y) and hand_data == config.PEN_ON:
            print("[result_display.py] Next Button Clicked")
            clicked = True

        pygame.display.update()

    return True
