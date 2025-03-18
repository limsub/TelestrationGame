import asyncio
import websockets
import json

SERVER_URL = "ws://hzzz.site:8000/game"
# SERVER_URL = "ws://localhost:8000/game"

class WebSocketClient:
    def __init__(self):
        self.websocket = None

    async def connect(self):
        """서버에 WebSocket 연결"""
        try:
            print("[WebSocket] 서버에 연결 시도 중...")
            self.websocket = await websockets.connect(
                SERVER_URL, 
                ping_interval=10,
                ping_timeout=1200,
                max_size=None
            )




            print(f"[WebSocket] 서버 연결 성공: {SERVER_URL}")
        except Exception as e:
            print(f"[WebSocket] 서버 연결 실패: {e}")

    async def send_message(self, message: dict):
        """서버로 JSON 메시지를 전송"""
        try:
            if self.websocket:
                json_message = json.dumps(message)
                # print(f"[WebSocket] 서버로 전송: {json_message}")  # ✅ 전송 메시지 출력
                await self.websocket.send(json_message)
            else:
                print("[WebSocket] 연결되지 않음. 메시지 전송 실패")
        except Exception as e:
            print(f"[WebSocket] 메시지 전송 오류: {e}")

    async def receive_message(self):
        """서버로부터 JSON 메시지를 수신"""
        try:
            if self.websocket:
                message = await self.websocket.recv()
                # print(f"[WebSocket] 서버로부터 수신: {message}")  # ✅ 수신 메시지 출력
                return json.loads(message)
            else:
                print("[WebSocket] 연결되지 않음. 메시지 수신 실패")
                return None
        except Exception as e:
            print(f"[WebSocket] 메시지 수신 오류: {e}")
            # return None
            return e


    async def wait_for_message_with_key(self, key: str):
        """
        특정 키(key)가 포함된 메시지가 올 때까지 대기

        :param key: 메시지에서 기다릴 키 (예: "image", "word", "status")
        """
        try:
            if not self.websocket:
                print("[WebSocket] 연결되지 않음. 메시지 대기 실패")
                return None

            while True:
                message = await self.receive_message()
                if "sent 1011" in message:
                    break
                if message is None:
                    continue
                    # break

                if key in message:
                    # print(f"[WebSocket] '{key}' 포함된 메시지 수신: {message}")
                    return message
        except asyncio.TimeoutError:
            print(f"[WebSocket] '{key}' 메시지 대기 시간 초과")
            return None


    async def close(self):
        """WebSocket 연결 종료"""
        try:
            if self.websocket:
                print("[WebSocket] 서버 연결 종료 요청")
                await self.websocket.close()
                print("[WebSocket] 서버 연결 종료됨")
        except Exception as e:
            print(f"[WebSocket] 연결 종료 오류: {e}")


    
    async def wait_for_game_end(self):
        """
        게임 종료 메시지가 올 때까지 대기
        - 서버로부터 {"type": "game_end", "images": [...], "first_words": [...], "result_words": [...]} 형식의 데이터를 수신할 때까지 대기
        """
        try:
            if not self.websocket:
                print("[WebSocket] 연결되지 않음. 메시지 대기 실패")
                return None

            while True:
                message = await self.receive_message()
                if message is None:
                    continue  # 메시지를 받지 못하면 다시 대기

                if message.get("type") == "game_end":  # ✅ "type"이 "game_end"인지 확인
                    # print(f"[WebSocket] 게임 종료 메시지 수신: {message}")
                    return message  # 게임 종료 메시지를 반환
        except asyncio.TimeoutError:
            print("[WebSocket] 게임 종료 메시지 대기 시간 초과")
            return None



