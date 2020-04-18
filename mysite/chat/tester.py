import os
import sys

sys.path.append("home/mysite")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# your imports, e.g. Django models

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import models
# Create your views here.

@login_required(redirect_field_name='')
def index(request):
    return render(request, 'chat/index.html', {})

@login_required(redirect_field_name='')
def room(request, room_name):
    name = str(room_name)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': models.ChatMessage.objects.all()
        })


for item in models.ChatMessage.objects.all():
    print(item.content, item.room)
