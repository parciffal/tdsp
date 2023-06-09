from django.http import HttpResponse

import json


def data_status(data):
    response = HttpResponse(
        json.dumps({"data": data, "status": "ok"}),
        content_type="application/json"
    )
    response['Access-Control-Allow-Origin'] = '*'  # replace * with your desired origin
    response['Access-Control-Allow-Methods'] = 'GET, POST,DELETE, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

    return response


def ok_status():
    return HttpResponse(
        json.dumps({"status": "ok"}),
        status=200,
        content_type="application/json"
    )


def error_status(error, status):
    return HttpResponse(
        json.dumps({"error": f"{error}"}),
        status=status,
        content_type="application/json"
    )
