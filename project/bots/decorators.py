from django.http import HttpResponse


def vk_success_response(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        return HttpResponse("ok")

    return wrapper
