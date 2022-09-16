from django.core.serializers import serialize
from hacker_news_generated_data.models import News


class SerializedData():
    def allData():
        data = News.objects.all().order_by("-time")
        return serialize(
            "json",
            data, 
            fields=(
                "pk", 
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
