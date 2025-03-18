import pygame
import asyncio
import websockets
import json
import atexit  # 🔥 종료 시 실행할 코드 등록

from Presentation import start_screen, waiting_room, countdown, initial_word_display, drawing, good_bye, received_image_display, result_display, buffering_screen

from websocket_client import WebSocketClient
from Utils.image_utils import convert_surface_to_string, convert_string_to_surface


import hand_tracking  # ✅ 모듈 불러오기

import config


pygame.init()   # 이건 여기서 딱 한 번만 실행해야 함.
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Hand Gesture Game")

ws_client = WebSocketClient()

async def main():

    print(pygame.font.get_fonts())

    
    await ws_client.connect()

    running = True
    current_screen = "start"

    try:
        while running:
            print("[main.py] current_screen : ", current_screen)

            # 0. 시작 화면
            if current_screen == "start":
                button_clicked = await start_screen.run(screen, ws_client)

                if button_clicked:
                    current_screen = "waiting"

                    # 임시
                    # initial_word = "하이"
                    # current_screen = "drawing_1"

                    # p = config.png_image
                    # images = [[p, p, p, p], [p, p, p, p], [p, p, p, p], [p, p, p, p]]
                    # first_words = ["바보", "바보", "바보", "바보"]
                    # result_words = ["바보", "바", "바", "바"]
                    # current_screen = "show_result"

                    # current_screen = "drawing_1"

                    # received_image = convert_string_to_surface(config.png_image)
                    # await received_image_display.run(screen, received_image, 20, 3)

                    # initial_word = "하이"
                    # current_screen = "drawing_1"




 
            # 0.5. 대기 화면
            elif current_screen == "waiting":
                game_start = await waiting_room.run(screen, ws_client)

                if game_start:
                    response = await ws_client.receive_message()
                    initial_word = response.get("word", "제시어 없음")
                    current_screen = "countdown"
                    print(f"[main.py] 초기 단어 : {initial_word}")
            

            # 0.7. 카운트다운 시작
            elif current_screen == "countdown":
                await countdown.run(screen)
                current_screen = "drawing_1"
            
            # 게임 시작
            elif current_screen == "drawing_1":
                for i in range(4):
                    print(f'[main.py] Round {i+1} 시작')

                    remaining_time = 70

                    # 제시어 or 그림 확인
                    if i == 0:
                        used_time = await initial_word_display.run(screen, initial_word, remaining_time)
                    else:
                        used_time = await received_image_display.run(screen, received_image, remaining_time, i+1)

                    remaining_time -= used_time

                    # 그림 그리기
                    drawing_result = await drawing.run(screen, remaining_time)

                    # 그림 이미지 -> String 
                    drawing_result_str = convert_surface_to_string(drawing_result)

                    # 서버로 이미지 전송
                    await ws_client.send_message({"type": "image", "data": drawing_result_str})
                    print(f"[main.py] [Round {i+1}] 이미지 전송 완료")

                    # 대기중 화면
                    await buffering_screen.run(screen)

                    # 서버에서 이미지 수신
                    if i != 3:
                        print(f"[main.py] [Round {i+1}] 이미지 수신 대기중")

                        image_message = await ws_client.wait_for_message_with_key("image")
                        received_image_str = image_message.get("image", None)
                        print(f"[main.py] [Round {i+1}] 이미지 수신 완료")

                        if received_image_str:
                            received_image = convert_string_to_surface(received_image_str)
                            # current_screen = "guessing_2"
                            continue

                    else:
                        print(f"[main.py] [Round {i+1}] 최종 결과 대기중")
                        game_end_message = await ws_client.wait_for_game_end()
                        

                        if game_end_message:
                            images = game_end_message["images"]  # 4명의 플레이어가 그린 그림 4개씩
                            first_words = game_end_message["first_words"]  # 원래 단어 4개
                            result_words = game_end_message["result_words"]  # 추론된 단어 4개

                            print(f"[main.py] [Round 4] 최종 이미지 수신 완료: {len(images)}명의 플레이어 데이터")
                            
                            # 다음 화면으로 이동
                            current_screen = "show_result"



            # 5. 최종 4개의 결과 확인하기
            elif current_screen == "show_result":    
                for i in range(4):                    
                    print(f"[main.py] 단어 {i+1} 결과 화면 표시 중...")
                    next_button_clicked = await result_display.run(screen, images[i], first_words[i], result_words[i])
                    
                    # ✅ "다음으로" 버튼이 클릭되면 다음 플레이어 결과 표시
                    if next_button_clicked:
                        continue

                # ✅ 모든 결과를 표시한 후, 다시 대기 화면으로 이동
                current_screen = "good_bye"

            elif current_screen == "good_bye":
                print("[main.py] 게임 끝~~~ ㅊㅊ")
                await good_bye.run(screen, ws_client)
                
                # break

  
    except asyncio.CancelledError:
        print("❌ [main.py] 프로그램 종료됨!")

    finally:
        await ws_client.close()  # ✅ 프로그램 종료 시 WebSocket 닫기


# ✅ 프로그램이 강제 종료될 때 WebSocket을 닫도록 설정
def cleanup():
    asyncio.run(ws_client.close())
    print("✅ WebSocket 연결 종료됨!")


atexit.register(cleanup)  # 종료 시 실행될 함수 등록


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("❌ 프로그램 강제 종료됨! WebSocket 닫기 실행...")