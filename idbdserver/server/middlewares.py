from django.utils.deprecation import MiddlewareMixin


class MiddleWare(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Methods'] = "POST, GET, DELETE, OPTIONS, DELETE"
            response['Access-Control-Max-Age'] = 1728000
            response["Access-Control-Allow-Headers"] = "Content-Type, x-requested-with, x-token"
            return response

        return response