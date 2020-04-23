from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models, forms, characters
# Create your views here.


@login_required(redirect_field_name='')
def index(request):
    roomList = models.Game.objects.all()
    print(roomList)
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'chat/index.html', {'error': False,
                                               'rooms': roomList
                                               })


@login_required(redirect_field_name='')
def room(request, room_name):
    name = str(request.user.get_username())
    if request.method == 'POST':
        # character selection
        char_name = request.POST.get('char_name')
        if char_name in characters.nameList():
            gameObject = models.Game.objects.get(gameRoom=room_name)
            if name == gameObject.player1User and not gameObject.player1Char:
                gameObject.player1Char = char_name
                character = characters.get(char_name)
                gameObject.player1HP = character.HP
                gameObject.player1Attack = character.Attack
                gameObject.player1Dodge = character.Dodge

            elif name == gameObject.player2User and not gameObject.player2Char:
                gameObject.player2Char = char_name
                character = characters.get(char_name)
                gameObject.player2HP = character.HP
                gameObject.player2Attack = character.Attack
                gameObject.player2Dodge = character.Dodge
            gameObject.save()
    if not room_name.isalnum():
        # error if the name is wrong
        return render(request, 'chat/index.html', {'error': True})
    if len(room_name) < 1:
        request.path += '-'
        return render(request, 'chat/index.html', {'error': True})
    if not (models.Rooms.objects.filter(roomname=room_name).exists()):
        # create new room if it doesn't exist
        newroom = models.Rooms(roomname=room_name)
        newroom.save()
        roomObject = models.Rooms.objects.get(roomname=room_name)
        newGame = models.Game(gameRoom=roomObject, player1User=name)
        newGame.save()
    charForm = forms.CharForm()
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': models.ChatMessage.objects.filter(room=room_name),
        'user': name,
        'game': models.Game.objects.get(gameRoom=room_name),
        'charForm': charForm,
        'character': request.session['character']
    })
