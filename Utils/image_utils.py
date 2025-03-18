import pygame
import base64
import io

# def convert_surface_to_string(surface):
#     """Pygame Surface를 Base64 문자열로 변환"""
#     img_str = pygame.image.tostring(surface, "RGB")
#     return base64.b64encode(img_str).decode("utf-8")
from PIL import Image  # 🔥 PIL 라이브러리 사용

MAX_IMAGE_SIZE = 1_048_576  # 1MB (Base64 인코딩된 문자열 크기 제한)

def convert_surface_to_string(surface):
    """Pygame Surface를 640x480으로 변환 후 Base64 문자열로 변환"""
    quality = 90  # 초기 품질 설정

    # ✅ 무조건 640x480 크기로 조정
    resized_surface = pygame.transform.scale(surface, (1024, 600))

    while True:
        img_io = io.BytesIO()
        
        pil_image = pygame_surface_to_pil(resized_surface)
        pil_image.save(img_io, format="PNG", quality=quality)
        img_io.seek(0)

        compressed_img = base64.b64encode(img_io.getvalue()).decode("utf-8")

        if len(compressed_img) <= MAX_IMAGE_SIZE:
            print(f"✅ [Utils] 변환된 이미지 크기: {len(compressed_img)} bytes (품질 {quality}%)")
            print(compressed_img)
            return compressed_img  # 🔥 JSON 없이 문자열만 반환
        # 🔥 1MB를 초과하면 품질을 낮춰서 다시 저장
        quality -= 10
        if quality < 30:
            print("❌ [Utils] 품질을 줄여도 1MB 이하로 만들 수 없음. 전송 불가.")
            return None




def pygame_surface_to_pil(surface):
    """Pygame Surface를 PIL 이미지로 변환"""
    raw_str = pygame.image.tostring(surface, "RGBA")
    pil_image = Image.frombytes("RGBA", surface.get_size(), raw_str)
    return pil_image




def convert_string_to_surface(img_str):
    """Base64 문자열을 Pygame Surface로 변환 (크기 유지)"""
    try:
        # ✅ Base64 디코딩
        img_data = base64.b64decode(img_str)

        # ✅ PIL 이미지로 변환
        img_io = io.BytesIO(img_data)
        pil_image = Image.open(img_io).convert("RGBA")

        # ✅ 원본 크기 가져오기
        width, height = pil_image.size

        # ✅ Pygame Surface로 변환
        img_surface = pygame.image.fromstring(pil_image.tobytes(), (width, height), "RGBA")
        print(f"[Utils] 이미지 변환 완료 (원본 크기 유지: {width}x{height})")

        return img_surface
    except Exception as e:
        print(f"❌ [Utils] 이미지 변환 오류: {e}")
        return None