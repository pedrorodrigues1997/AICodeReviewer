import requests

def get_pr_files(url: str, github_token: str) -> str:

    headers = {
        "Authorization" : f"Bearer {github_token}",
        "Accept" : "application/vnd.github+json"
    }

    response = requests.get(f"{url}/files", headers=headers)
    response.raise_for_status()
    return response.json()