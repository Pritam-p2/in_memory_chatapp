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

1. First run fastapi server using uvicorn main:app --reload
2. We will use multiple terminals as clients to connect to the server
3. In each terminal command 'python client_example.py'
4. In each terminal we will be prompted with "username" and "topic".
   One can choose to keep it empty then default username as 'alice' and topic 'sports' will be used as initial payload
5. Using '/list' we will get all the active topics
