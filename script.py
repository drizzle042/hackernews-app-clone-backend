import json
from datetime import datetime
from requests import get
from hacker_news_generated_data.models import News

HN_URL = "https://hacker-news.firebaseio.com"

endpoints = [
    "/v0/newstories.json",
    # "/v0/topstories.json",
    # "/v0/beststories.json",
    # "/v0/askstories.json",
    # "/v0/showstories.json",
    # "/v0/jobstories.json",
]

def sync_to_DB(data: dict):
    data["time"] = datetime.fromtimestamp(data["time"])
    news = News(*data)
    news.save()

def story(id: int) -> dict:
    response = get(f"{HN_URL}/v0/item/{id}.json")
    data = json.loads(response.text)
    return data

def getStories(endpoint: str) -> list:
    response = get(f"{HN_URL}{endpoint}")
    data = str(response.text)[1:-2].split(",")
    return data

for i in getStories("/v0/newstories.json")[0:1]:
    sync_to_DB(story(int(i)))