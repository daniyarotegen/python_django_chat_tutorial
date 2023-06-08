import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from .models import ChatMessage

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    old_messages = ChatMessage.objects.filter(room_name=room_name)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'old_messages': old_messages
    })


@csrf_exempt
def connect(request):
    logger.debug(request.body)
    user = request.user.username if request.user.is_authenticated else 'Anonymous'
    response = {
        'result': {
            'user': user
        }
    }
    return JsonResponse(response)


@csrf_exempt
def publish(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authorized'}, status=403)

    logger.debug(request.body)
    data = json.loads(request.body.decode("utf-8"))
    message = data.get("data", {}).get("message")
    channel = data.get("channel")
    if channel and message:
        room_name = channel.split(":")[-1]
        chat_message = ChatMessage(room_name=room_name, message=message, user=request.user)
        chat_message.save()
    response = {
        'result': {
            'message': message,
            'user': request.user.username
        }
    }
    return JsonResponse(response)


@csrf_exempt
def subscribe(request):
    logger.debug(request.body)
    response = {
        'result': {}
    }
    return JsonResponse(response)
