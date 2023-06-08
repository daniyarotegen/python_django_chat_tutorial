import uuid
from django.db import models
from django.utils import timezone
from enum import Enum
from django.conf import settings


class ChatType(Enum):
    PRIVATE = "Private"
    GROUP = "Group"


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chat_type = models.CharField(
        max_length=7,
        choices=[(tag.name, tag.value) for tag in ChatType],
        default=ChatType.PRIVATE,
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ChatRoomMembership', related_name='chat_rooms')
    avatar = models.ImageField(upload_to='groupchats/', null=True, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups', null=True, blank=True)

    def is_group_chat(self):
        return self.chat_type == ChatType.GROUP.name

    def get_user_list(self):
        return [user.username for user in self.users.all()]


class ChatRoomMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_name = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']
