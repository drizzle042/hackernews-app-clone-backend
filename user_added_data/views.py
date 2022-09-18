import json
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .db_controller import Queries 


payload = {
    "totalDocs" : 0,
    "totalPages" : 0,
    "page": 1,
    "data": None
}

user_signup_data = {
    "name": "",
    "email": "",
    "password": ""
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
            response = JsonResponse({
                "status": "Error", 
                "message": "The comment ID is a required field"
                })
            response.status_code = 400
            response.reason_phrase = "comment ID is a required field to see comment"

            return response

        # Query 
        try:
            query = Queries.comments(id = id)

        except ConnectionError:
            response = JsonResponse({
                    "status": "Server Down", 
                    "message": "The News server is down at the moment"
                    })
            response.status_code = 500
            response.reason_phrase = "The News server is down at the moment"

            return response

        # Payload
        payload["totalDocs"] = len(query[1])
        payload["data"] = {
            "parent": query[0],
            "comments": query[1]
            }

        return JsonResponse(payload, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class Account(View):
    
    def post(self, request):

        request = json.loads(request.body)
        # Params
        firstName = request["firstName"] if "firstName" in request else ""
        lastName = request["lastName"] if "lastName" in request else ""
        fullName = f"{firstName} {lastName}"

        try:
            email = request["email"]
            password = request["password"]
        except KeyError:
            response = JsonResponse({
                    "status": "Bad request. Missing fields are required!", 
                    "message": "The user's email and password are required. If you missed any of these, please provide. This might be a mistake, it happens, lol."
                    })
            response.status_code = 400
            response.reason_phrase = "Bad request. Missing fields are required!"

            return response

        user_signup_data["name"] = str(fullName).strip()
        user_signup_data["email"] = email
        user_signup_data["password"] = password

        return HttpResponse("request received")
        