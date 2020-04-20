
from . import models, characters
from channels.db import database_sync_to_async
import random



class Player:
    def __init__(self, Name, HP, Attack, Dodge):
        self.Name = Name
        self.HP = HP
        self.Attack = Attack
        self.Dodge = Dodge



@database_sync_to_async
def addChat(room_name, message, name):
    #store message in model?
    roomObject = models.Rooms.objects.get(roomname=room_name)
    store = models.ChatMessage(room=roomObject, content=message, author=name)
    store.save()

@database_sync_to_async
def getGame(room_name, gameState):
    gameObject = models.Game.objects.get(gameRoom=room_name)
    gameState.append(gameObject.player1HP)
    gameState.append(gameObject.player1Attack)
    gameState.append(gameObject.player1Dodge)
    
    gameState.append(gameObject.player2HP)
    gameState.append(gameObject.player2Attack)
    gameState.append(gameObject.player2Dodge)
    #print(gameState)

@database_sync_to_async
def actionHandler(room_name, action, name):
    #take an action, apply it to the game associated with the room
    gameObject = models.Game.objects.get(gameRoom=room_name)
    if name == gameObject.player1User and not gameObject.player1Action:
        gameObject.player1Action = action
    elif name == gameObject.player2User and not gameObject.player2Action:
        gameObject.player2Action = action
    gameObject.save()

@database_sync_to_async
def actionChecker(room_name, checker):
    print("we are checking")
    #Check if both actions have been assigned, return t/f
    gameObject = models.Game.objects.get(gameRoom=room_name)
    print(gameObject.player1Action, gameObject.player2Action)
    if gameObject.player1Action != None and gameObject.player2Action != None:
        checker[0] = True
        print("Actions good")
        return
    print("actions not good")
    checker[0] = False
    return

def checkWin(gameObject):
    print(gameObject.player1HP, gameObject.player2HP)
    if gameObject.player1HP <= 0 or gameObject.player2HP <= 0:
        gameObject.gameOver = True
        gameObject.save()
        return True
    return False

def saveGame(player1,player2,gameObject):
    if player1.Name == gameObject.player1User:
        gameObject.player1HP = player1.HP
        gameObject.player1Attack = player1.Attack
        gameObject.player1Dodge = player1.Dodge

        gameObject.player2HP = player2.HP
        gameObject.player2Attack = player2.Attack
        gameObject.player2Dodge = player2.Dodge
    else:
        gameObject.player1HP = player2.HP
        gameObject.player1Attack = player2.Attack
        gameObject.player1Dodge = player2.Dodge

        gameObject.player2HP = player1.HP
        gameObject.player2Attack = player1.Attack
        gameObject.player2Dodge = player1.Dodge
    gameObject.save()
    #print(gameObject)


def resolve(player1, act1, player2, act2, char1, char2, gameObject):
    #just apply to game in order act1 and act2 based on the character stats
    #ok now change the gamestate so this works
    #let's just add more shit to the model, why not
    #yeah it's gross
    print("do we get to resolve?")
    turnRecord = ""
    
    print(checkWin(gameObject))
    if checkWin(gameObject)==True:
        turnRecord = "The game is over!"
        return turnRecord
    if act1 == "Attack":
        if random.randint(1,100) > player2.Dodge:
            player2.HP = player2.HP - player1.Attack
            turnRecord = turnRecord+"%s attacks %s, dealing %d damage!\n"%(char1.Name,char2.Name, player1.Attack)
        else:
            turnRecord = turnRecord+"%s's attack misses %s!\n"%(char1.Name,char2.Name)
        player1.Attack = char1.Attack #reset any attack bonuses
        player2.Dodge = char2.Dodge #reset dodge bonuses
        saveGame(player1,player2,gameObject)
        if checkWin(gameObject):
            turnRecord = turnRecord + "And the game is over!"
            return turnRecord
    elif act1 == "Dodge":
        player1.Dodge = char1.Dodge + 50
        turnRecord = turnRecord+"%s is ready to dodge!\n"%(char1.Name)
        saveGame(player1,player2,gameObject)
    elif act1 == "Power Up":
        player1.Attack = char1.Attack*2
        turnRecord = turnRecord+"%s readies to strike!\n"%(char1.Name)
        print(player1.Attack)
        saveGame(player1,player2,gameObject)
    elif act1 == "Special":
        a = 1 #aka do nothing yet
    #now for player2
    if act2 == "Attack":
        if random.randint(1,100) > player1.Dodge:
            player1.HP = player1.HP - player2.Attack
            turnRecord = turnRecord+"%s attacks %s, dealing %s damage!\n"%(char2.Name,char1.Name, player2.Attack)
        else:
            turnRecord = turnRecord+"%s's attack misses %s!\n"%(char2.Name,char1.Name)
        player2.Attack = char2.Attack #reset any attack bonuses
        player1.Dodge = char1.Dodge #reset dodge bonuses
        saveGame(player1,player2,gameObject)
        if checkWin(gameObject):
            turnRecord = turnRecord + "And the game is over!"
            return turnRecord
    elif act2 == "Dodge":
        player2.Dodge = char2.Dodge + 50
        turnRecord = turnRecord+"%s is ready to dodge!\n"%(char2.Name)
        saveGame(player1,player2,gameObject)
    elif act2 == "Power Up":
        player2.Attack = char2.Attack*2
        turnRecord = turnRecord+"%s readies to strike!\n"%(char2.Name)
        saveGame(player1,player2,gameObject)
    elif act2 == "Special":
        a = 1 #aka do nothing yet
    print(gameObject.player1Action, gameObject.player2Action)
    gameObject.player1Action = None
    gameObject.player2Action = None
    gameObject.save()
    print(gameObject.player1Action, gameObject.player2Action)
    print(turnRecord)
    saveGame(player1,player2,gameObject)
    return turnRecord


@database_sync_to_async
def turn(room_name):
    #apply the actions, based on the characters, then set the current actions to null so we can do the next turn
    #-2: normal moves, resolved in order of character speed
    #we should also record the turn so we can send it to the game and have it play out in the right order in the browser
    #priority moves removed because I'm lazy. Now dodging etc will just apply to your next turn
    print("trying a turn")

    #get game object
    gameObject = models.Game.objects.get(gameRoom=room_name)
    char1 = characters.get(gameObject.player1Char)
    print(char1)
    char2 = characters.get(gameObject.player2Char)
    act1 = gameObject.player1Action
    act2 = gameObject.player2Action

    #we check speed, then resolve with either player1 or player 2 going first
    if char1.Speed >= char2.Speed:
        print("P1 goes first")
        player1 = Player(gameObject.player1User,gameObject.player1HP, gameObject.player1Attack, gameObject.player1Dodge)        
        player2 = Player(gameObject.player2User,gameObject.player2HP, gameObject.player2Attack, gameObject.player2Dodge)
        print(resolve(player1, act1, player2, act2, char1, char2, gameObject))
    else:
        print("P2 goes first")
        player1 = Player(gameObject.player2User,gameObject.player2HP, gameObject.player2Attack, gameObject.player2Dodge)        
        player2 = Player(gameObject.player1User,gameObject.player1HP, gameObject.player1Attack, gameObject.player1Dodge)
        print(resolve(player1, act2, player2, act1, char2, char1, gameObject))
    


@database_sync_to_async
def joinGame(room_name, name):
    #join as p2 if possible
    gameObject = models.Game.objects.get(gameRoom=room_name)
    if not gameObject.player2User and name != gameObject.player1User:
        gameObject.player2User = name
        gameObject.save()