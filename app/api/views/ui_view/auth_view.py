from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.handlers.wsgi import WSGIRequest

import json
import jwt

from ...models import UserModel

from ...tools.http_tools import ok_status, data_status
from ...tools.jwt_tools import generate_jwt


class UserAuthView(View):

    @csrf_exempt
    @staticmethod
    def user_info(request):
        token = request.META.get("HTTP_AUTHORIZATION").split()[1]
        user_info = jwt.decode(token, "SECRET_KEY", algorithms=['HS256'])
        return data_status(user_info)

    @csrf_exempt
    @staticmethod
    def login(request: WSGIRequest):

        data = json.loads(request.body)
        print(data)
        try:
            username = data['username']
            password = data['password']
        except KeyError:
            return HttpResponse({"status": "Missing key error"})
        user = authenticate(username=username,
                            password=password)

        if user:
            if user.is_active:
                try:
                    user_model = UserModel.objects.get(user=user)
                except KeyError:
                    return HttpResponse({"status": "Missing key error"})

                login(request, user)

                jwt_token = generate_jwt(user_model)
                refresh_jwt_token = generate_jwt(user_model, True)

                dt = {"access_token": str(jwt_token), "refresh_token": str(refresh_jwt_token)}
                response = JsonResponse(dt)
                response['Access-Control-Allow-Origin'] = '*'  # replace * with your desired origin
                response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
                response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

                response.set_cookie("refresh_token", refresh_jwt_token, httponly=True)

                return response
            else:
                return HttpResponse({"status": "user not active"})
        else:

            try:
                user = User.objects.get(username=username)
            except KeyError:

                return HttpResponse({"status": "not register"})

            return HttpResponse({"status": "wrong password"})

    @csrf_exempt
    @staticmethod
    def register(request):
        data = json.loads(request.body)

        try:
            username = data['username']
            password = data['password']
            email = data['email']
            name = data['name']
            surname = data['surname']
        except KeyError:
            return HttpResponse({"status": "Missing key error"})

        if User.objects.filter(username=username).exists():
            return HttpResponse({"status": "User exist's"})
        else:

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email)

            user.first_name = name
            user.last_name = surname
            user.is_active = False
            user.save()

            user_model = UserModel.objects.create(user=user)
            user_model.save()
            return ok_status()

    
    @csrf_exempt
    @staticmethod
    def logout(request):
        logout(request)
        return ok_status()


   