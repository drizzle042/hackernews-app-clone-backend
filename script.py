from json import loads as loadToDict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from requests import get
from hacker_news_generated_data.models import News

HN_URL = "https://hacker-news.firebaseio.com"

endpoints = [
    "/v0/newstories.json",
    "/v0/topstories.json",
    "/v0/beststories.json",
    "/v0/askstories.json",
    "/v0/showstories.json",
    "/v0/jobstories.json",
]

def sync_to_DB(story, getStories):
    for i in getStories:
        data = story(i)
        data["time"] = datetime.fromtimestamp(data["time"])
        try:
            news = News(**data)
            news.save()
        except Exception as e:
            pass

def story(id) -> dict:
    response = get(f"{HN_URL}/v0/item/{id}.json")
    data = loadToDict(response.text)
    return data

def getStories(endpoint: str) -> list:
    response = get(f"{HN_URL}{endpoint}")
    data = str(response.text)[1:-2].split(",")
    return data

def runFunc():
    with ThreadPoolExecutor(max_workers=20) as executor:
        for endpoint in endpoints:
            executor.submit(sync_to_DB, story, getStories(endpoint))

runFunc()