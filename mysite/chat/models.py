from django.db import models

# Create your models here.

class Rooms(models.Model):
    roomname = models.CharField(primary_key=True,max_length=30)

class ChatMessage(models.Model):
    room = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    content = models.TextField()
    author = models.TextField()

class Game(models.Model):
    gameRoom = models.ForeignKey(Rooms,on_delete=models.CASCADE)
    player1User = models.TextField() #creator username
    player2User = models.TextField(blank=True, null=True) #join username
    
    #gamestats that are relevant
    player1Char = models.TextField(blank=True, null=True) #character name
    player1HP = models.IntegerField(blank=True, null=True) #hitpints
    player1Attack = models.IntegerField(blank=True, null=True)
    player1Dodge = models.IntegerField(blank=True, null=True)

    player2Char = models.TextField(blank=True, null=True) #character name
    player2HP = models.IntegerField(blank=True, null=True) #hitpints
    player2Attack = models.IntegerField(blank=True, null=True)
    player2Dodge = models.IntegerField(blank=True, null=True)
    
    player1Action = models.TextField(blank=True, null=True) #next action
    player2Action = models.TextField(blank=True, null=True) #next action
    
    gameOver = models.BooleanField(default=False)
