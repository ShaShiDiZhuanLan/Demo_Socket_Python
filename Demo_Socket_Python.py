#! -*- coding: utf-8 -*-
"""
Author: ZhenYuSha
Create Time: 2019-1-14
Info: Websocket 的使用示例
"""
import asyncio
import websockets

websocket_users = set()


# 检测客户端权限，用户名密码通过才能退出循环
async def check_user_permit(websocket):
    print("new websocket_users:", websocket)
    websocket_users.add(websocket)
    print("websocket_users list:", websocket_users)
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "Congratulation, you have connect with server..."
            await websocket.send(response_str)
            print("Password is ok...")
            return True
        else:
            response_str = "Sorry, please input the username or password..."
            print("Password is wrong...")
            await websocket.send(response_str)


# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_user_msg(websocket):
    while True:
        recv_text = await websocket.recv()
        print("recv_text:", websocket.pong, recv_text)
        response_text = f"Server return: {recv_text}"
        print("response_text:", response_text)
        await websocket.send(response_text)


# 服务器端主逻辑
async def run(websocket, path):
    while True:
        try:
            await check_user_permit(websocket)
            await recv_user_msg(websocket)
        except websockets.ConnectionClosed:
            print("ConnectionClosed...", path)    # 链接断开
            print("websocket_users old:", websocket_users)
            websocket_users.remove(websocket)
            print("websocket_users new:", websocket_users)
            break
        except websockets.InvalidState:
            print("InvalidState...")    # 无效状态
            break
        except Exception as e:
            print("Exception:", e)


if __name__ == '__main__':
    print("127.0.0.1:8181 websocket...")
    asyncio.get_event_loop().run_until_complete(websockets.serve(run, "127.0.0.1", 8181))
    asyncio.get_event_loop().run_forever()
