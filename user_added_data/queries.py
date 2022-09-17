import json
from concurrent.futures import ThreadPoolExecutor
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.serializers import serialize
from requests import get
from hacker_news_generated_data.models import News

HN_URL = "https://hacker-news.firebaseio.com"

class Queries():

    def allArticles(paginate=10, page=1, **kwargs):

        def queryset(type, keyword):
            if type != "all" and keyword != "null":
                queryset = News.objects.order_by("-time").exclude(type__icontains="comment").filter(Q(type__icontains = type), Q(title__icontains = keyword) | Q(text__icontains = keyword) | Q(by__icontains = keyword))
                return queryset
            elif type == "all" and keyword != "null":
                queryset = News.objects.order_by("-time").exclude(type__icontains="comment").filter(Q(title__icontains = keyword) | Q(text__icontains = keyword) | Q(by__icontains = keyword))
                return queryset
            elif type != "all" and keyword == "null":
                queryset = News.objects.order_by("-time").exclude(type__icontains="comment").filter(Q(type__icontains = type))
                return queryset
            elif type == "all" and keyword == "null":
                queryset = News.objects.order_by("-time").exclude(type__icontains="comment")
                return queryset

        article_type = str(kwargs["type"]).lower()
        search_keyword = str(kwargs["keyword"]).lower()

        paginator = Paginator(queryset(type=article_type, keyword=search_keyword), paginate)
        data = serialize(
            "json",
            paginator.page(page).object_list, 
            fields=(
                "title", 
                "type", 
                "by", 
                "time", 
                "text", 
                "parent", 
                "poll",
                "url",
                "score",
                "kids"
            ))

        return data, paginator

    def comments(id):

        def story(commentID) -> dict:
            response = get(f"{HN_URL}/v0/item/{commentID}.json")
            data = json.loads(response.text)
            return data

        parentComment = story(id)

        data = []
        def getComments(commentID):
            data.append(story(commentID))

        with ThreadPoolExecutor(max_workers=20) as executor:
            for commentID in parentComment["kids"]:
                executor.submit(getComments, commentID)

        return parentComment, data