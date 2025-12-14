# Chatapp

A lightweight real-time in-memory chat server using FastAPI WebSockets that allows users to
join topic-based chat rooms, send messages to users within the same topic, and automatically
remove messages after a set time period.

## RUN

```bash
git clone https://github.com/username/repo-name.git
cd repo-name
pip install -r requirements.txt
```

## TEST

1.  Start the FastAPI WebSocket server by running:

    uvicorn main:app --reload

2.  Open multiple terminal windows to simulate multiple clients.
    In each terminal, run the client using:

    python client_example.py

3.  Each client will be prompted to enter a username and a topic.
    If left empty, the default values will be used:

    Username: alice
    Topic: sports

4.  Clients connected to the same topic can exchange messages in real time.

5.  To view all active topics and their user counts, type:

    /list

    The list will be returned only to the requesting client.
