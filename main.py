import json
import time
import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
logging.basicConfig(level=logging.INFO)


topics = {}  # {topic: {"users": {username: websocket}, "messages": []}}


def get_username(topic, username):
    if username not in topics[topic]["users"]:
        return username

    i = 2
    while f"{username}#{i}" in topics[topic]["users"]:
        i += 1
    return f"{username}#{i}"


async def expire_message(topic: str, message: dict):
    # expire message after 30 secs

    await asyncio.sleep(30)
    if topic in topics and message in topics[topic]["messages"]:
        topics[topic]["messages"].remove(message)
        logging.info("Message expired in topic %s", topic)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        # Initial join payload
        raw = await websocket.receive_text()
        try:
            data = json.loads(raw)
            # print(data)
            username = data.get("username",'')
            topic = data.get("topic",'')
        except Exception:
            await websocket.send_json({"error": "Invalid join payload"})
            await websocket.close()
            return
        
        if username == '':
            username = 'alice'
        if topic == '':
            topic = 'sports'

        #logging.info("%s joined topic %s", username, topic)
        # Create topic if missing
        if topic not in topics:
            topics[topic] = {"users": {}, "messages": []}

        username = get_username(topic, username)
        topics[topic]["users"][username] = websocket

        logging.info("%s joined topic %s", username, topic)

        await websocket.send_json({
            "system": f"Joined topic '{topic}' as {username}"
        })

        # Listen for messages
        while True:
            raw_msg = await websocket.receive_text()

            try:
                msg = json.loads(raw_msg)
                #print(msg)
            except Exception as e:
                await websocket.send_json({"error": str(e)})
                continue

            # Handle /list command
            if msg.get("message") == "/list":
                response = ["Active Topics:"]
                for t, info in topics.items():
                    response.append(f"{t} ({len(info['users'])} users)")
                await websocket.send_text("\n".join(response))
                continue

            # if msg.get("username") or msg.get("topic"):
            #     topic = msg.get("topic")
            #     username = msg.get("username")
            #     if topic:

            # if msg.get("message")=="create topic":
            #     await websocket.send_json(
            #         {"system": "Type new Topic --"}
            #     )
            #     continue

            message_data = {
                "username": username,
                "message": msg.get("message"),
                "timestamp": int(time.time())
            }

            topics[topic]["messages"].append(message_data)
            asyncio.create_task(expire_message(topic, message_data))

            # send message to others
            for user, ws in topics[topic]["users"].items():
                if user != username:
                    await ws.send_json(message_data)

            # Acknowledge to sender
            await websocket.send_json({"status": "delivered"})

    except WebSocketDisconnect:
        logging.info(f"{username} disconnected from {topic}")

        if topic in topics:
            users = topics[topic]["users"]

            if username in users:
                del users[username]
                logging.info(f"{username} removed from {topic}")

            if not users:
                del topics[topic]
                logging.info(f"topic {topic} deleted")
        

    finally:
        # Cleanup
        if topic in topics and username in topics[topic]["users"]:
            del topics[topic]["users"][username]

            if not topics[topic]["users"]:
                del topics[topic]
                logging.info("Topic %s removed (empty)", topic)
