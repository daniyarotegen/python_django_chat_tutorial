import json
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import logging
from .models import ChatMessage, ChatRoom, ChatType
from django.db.models import Count, Q

logger = logging.getLogger(__name__)
User = get_user_model()


def index(request):
    return render(request, 'chat/index.html')


class RoomView(LoginRequiredMixin, View):
    def get(self, request, room_uuid):
        room = ChatRoom.objects.filter(id=room_uuid).first()
        if room is None:
            return HttpResponse("Room not found", status=404)

        old_messages = ChatMessage.objects.filter(room_name=room).order_by('-timestamp')
        return render(request, 'chat/room.html',
                      {'room_name': room.name, 'room_uuid': str(room.id), 'old_messages': old_messages, 'room': room})


class StartChatView(LoginRequiredMixin, View):
    def get(self, request, username):
        other_user = get_object_or_404(User, username=username)
        logger.debug(f"Other user: {other_user.username if other_user else 'Not found'}")

        rooms = ChatRoom.objects.filter(users=request.user, chat_type=ChatType.PRIVATE.name)
        room = None
        for potential_room in rooms:
            if set(potential_room.users.all()) == set([request.user, other_user]):
                room = potential_room
                break

        logger.debug(f"Rooms: {rooms}")
        logger.debug(f"First room: {room}")

        if room is None:
            room = ChatRoom.objects.create(
                name=f'Chat with {other_user.username}',
                chat_type=ChatType.PRIVATE.name
            )
            room.users.add(request.user, other_user)
            room.save()
            logger.debug(f"New room created: {room}")
        else:
            logger.debug(f"Room already exists: {room}")

        logger.debug(f"Redirecting to room with ID: {str(room.id)}")
        return redirect(reverse('room_view', args=[str(room.id)]))



class ChatsView(LoginRequiredMixin, View):
    def get(self, request):
        chatrooms = ChatRoom.objects.filter(users=request.user).distinct()
        print(f"Chatrooms are {chatrooms}")
        chats_with_recipients = []
        for room in chatrooms:
            chat = ChatMessage.objects.filter(room_name=room).order_by('-timestamp').first()
            if room.is_group:
                chat_name = room.name
                avatar_url = room.avatar.url if room.avatar else None
                if chat:
                    chats_with_recipients.append({'chat': chat, 'chat_name': chat_name,
                                                  'room_id': str(room.id), 'avatar_url': avatar_url})
                else:
                    chats_with_recipients.append({'chat': None, 'chat_name': chat_name,
                                                  'room_id': str(room.id), 'avatar_url': avatar_url})
            else:
                if chat:
                    recipient = room.users.exclude(id=request.user.id).first()
                    chat_name = recipient.first_name + " " + recipient.last_name
                    avatar_url = recipient.avatar.url if recipient.avatar else None
                    chats_with_recipients.append({'chat': chat, 'chat_name': chat_name,
                                                  'room_id': str(room.id), 'avatar_url': avatar_url})

        chats_with_recipients.sort(key=lambda x: x['chat'].timestamp if x['chat'] else timezone.now(), reverse=True)
        return render(request, 'chat/chat_list.html', {'chats_with_recipients': chats_with_recipients})


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
    print(f'Data {data}')
    message = data.get("data", {}).get("message")
    channel = data.get("channel")
    if channel and message:
        room_uuid_str = channel.split(":")[-1]
        try:
            room_uuid = uuid.UUID(room_uuid_str)
        except ValueError:
            print(f"Invalid UUID: {room_uuid_str}")
            return JsonResponse({'error': 'Invalid UUID'}, status=400)

        try:
            room = ChatRoom.objects.get(id=room_uuid)
        except ChatRoom.DoesNotExist:
            print(f"Room with UUID {room_uuid} does not exist")
            return JsonResponse({'error': 'Room does not exist'}, status=404)

        chat_message = ChatMessage(room_name=room, message=message, user=request.user)
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
