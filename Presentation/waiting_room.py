import pygame
import json
import asyncio
from Utils import font_manager, image_manager

title_font = font_manager.get_font(48, "bold")  
status_font = font_manager.get_font(60, "bold")  
player_count_font = font_manager.get_font(36, "regular") 
info_font = font_manager.get_font(30, "light")

empty_screen = image_manager.empty_screen_image

async def run(screen, ws_client):
    game_start = False
    player_count = 0

    while not game_start:
        # screen.fill((255, 255, 255))  # 🔥 배경색: 흰색
        screen.blit(empty_screen, (0, 0))

        status_text = status_font.render("다른 유저들을 기다리는 중...", True, (0, 0, 0))
        status_rect = status_text.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(status_text, status_rect)

        player_count_text = player_count_font.render(f"현재 접속한 플레이어: {player_count}명 / 총 4명", True, (0, 0, 0))
        player_count_rect = player_count_text.get_rect(center=(screen.get_width() // 2, 300))
        screen.blit(player_count_text, player_count_rect)

        info_text = info_font.render("곧 게임이 시작됩니다...", True, (0, 0, 0))
        info_rect = info_text.get_rect(center=(screen.get_width() // 2, 400))
        screen.blit(info_text, info_rect)

        pygame.display.update()

        # 서버로부터 메시지 수신
        data = await ws_client.receive_message()

        print(f"[waiting_room.py] received data : {data}")

        if data is not None:
            if "ready" in data:
                player_count = sum(data["ready"])  # ✅ 준비된 플레이어 수 업데이트

            if "game_started" in data and data["game_started"]:
                game_start = True  # ✅ 게임 시작 신호 받으면 종료

    return game_start
