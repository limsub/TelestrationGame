import pygame
import os

pygame.font.init()

BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 
FONT_DIR = os.path.join(BASE_DIR, "Resources", "Fonts") 
FONT_FILE = "KOTRA HOPE.otf"

def get_font(size=30, weight="regular"):
    font_path = os.path.join(FONT_DIR, FONT_FILE)

    if not os.path.exists(font_path):
        print(f"❌ 폰트 파일이 존재하지 않음: {font_path}")
        return pygame.font.Font(None, size)  # 기본 폰트로 대체

    try:
        return pygame.font.Font(font_path, size)
    except Exception as e:
        print(f"❌ 폰트 로딩 실패: {e}")
        return pygame.font.Font(None, size)  # 기본 폰트로 대체



