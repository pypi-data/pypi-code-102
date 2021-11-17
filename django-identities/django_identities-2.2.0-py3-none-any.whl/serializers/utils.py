from django.contrib.auth.models import AbstractUser


def get_request_username(serializer) -> AbstractUser:
    return serializer.context["request"].user
