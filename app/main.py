from fastapi import FastAPI, Request
from app.review import review_pull_request

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    await review_pull_request(data)
    return {"status": "ok"}
    