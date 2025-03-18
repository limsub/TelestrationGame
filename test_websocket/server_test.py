import asyncio
import websockets
import datetime

async def handler(websocket, path):  # ✅ 'path' 추가
    print(f"[*] 클라이언트 연결됨: {websocket.remote_address}")
    
    try:
        while True:
            message = f"[*] M1 from SERVER 1 {datetime.datetime.now()}"
            await websocket.send(message)  # ✅ 서버 메시지 전송
            await asyncio.sleep(0.1)  # ✅ time.sleep() 대신 비동기 처리
    except websockets.exceptions.ConnectionClosed:
        print("[*] 클라이언트 연결 종료됨.")

async def main():
    async with websockets.serve(handler, "localhost", 8050):
        print("[*] WebSocket 서버가 ws://localhost:8050 에서 실행 중...")
        await asyncio.Future()  # 서버가 계속 실행되도록 유지

if __name__ == "__main__":
    asyncio.run(main())  # ✅ asyncio.run()으로 실행
