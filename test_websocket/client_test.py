import asyncio
import websockets

async def connect():
    uri = "ws://localhost:8050"  # ✅ WebSocket 프로토콜 사용
    async with websockets.connect(uri) as websocket:
        print(f"[*] 서버에 연결됨: {uri}")

        try:
            for i in range(5):
                message = f"안녕 서버! ({i})"
                await websocket.send(message)  # ✅ 서버로 메시지 전송
                response = await websocket.recv()  # ✅ 서버 응답 받기
                print(f"[*] 서버 응답: {response}")
                await asyncio.sleep(1)  # ✅ 1초 대기
        except websockets.exceptions.ConnectionClosed:
            print("[*] 서버 연결이 닫혔습니다.")

if __name__ == "__main__":
    asyncio.run(connect())  # ✅ asyncio.run()으로 실행
