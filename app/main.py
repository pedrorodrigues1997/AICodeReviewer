import os
from fastapi import FastAPI, Request
from app.review import review_pull_request
from dotenv import load_dotenv
from app.diff_fetcher import get_pr_files


load_dotenv()

app = FastAPI()


@app.post("/webhook")
async def github_webhook(request: Request):
    data = await request.json()
    github_api_key = os.getenv("GITHUB_TOKEN")
    print(github_api_key)
    action = data.get("action")
    pull_request = data.get("pull_request", {})


    if action in ["opened", "reopened"]:   
        pr_self_url = pull_request["_links"]["self"]["href"]
        files = get_pr_files(pr_self_url, github_api_key)
       
        await review_pull_request(files)

    return {"status": "ok"}
    