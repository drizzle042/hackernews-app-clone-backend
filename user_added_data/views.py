from ast import Raise
import json
from django.views import View
from django.http import JsonResponse
from .queries import Queries 


payload = {
    "totalDocs" : 0,
    "totalPages" : 0,
    "page": 1,
    "data": None
}


class AllArticles(View):

    def get(self, request):
        # Query params
        params = request.GET
        page = params.get("page") if params.get("page") else  1
        paginate = params.get("limit") if params.get("limit") else  10
        type = params.get("type") if params.get("type") else  "all"
        keyword = params.get("keyword") if params.get("keyword") else "null"

        # Query
        query = Queries.allArticles(paginate = paginate, page = page, type = type, keyword = keyword)
        
        # Payload
        payload["totalDocs"] = query[1].count
        payload["totalPages"] = query[1].num_pages
        payload["page"] = page
        payload["data"] = json.loads(query[0])

        return JsonResponse(payload, safe=False)


class Comments(View):

    def get(self, request):
        # Query params
        params = request.GET

        if params.get("commentid"):
            id = params.get("commentid")  
        else:
            raise ValueError("The comment id is a required field.")

        # Query 
        query = Queries.comments(id = id)

        # Payload
        payload["totalDocs"] = len(query[1])
        payload["data"] = {
            "parent": query[0],
            "comments": query[1]
            }

        return JsonResponse(payload, safe=False)