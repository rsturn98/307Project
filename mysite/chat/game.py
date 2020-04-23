from . import models, characters
from channels.db import database_sync_to_async
import random

# Defines a temporary player to store stats for this match


class Player:
    def __init__(self, Name, HP, Attack, Dodge):
        self.Name = Name
        self.HP = HP
        self.Attack = Attack
        self.Dodge = Dodge


@database_sync_to_async
def addChat(room_name, message, name):
    # Store message in model
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


@database_sync_to_async
def actionHandler(room_name, action, name):
    # Take an action, apply it to the game associated with the room
    gameObject = models.Game.objects.get(gameRoom=room_name)
    if name == gameObject.player1User and not gameObject.player1Action:
        gameObject.player1Action = action
    elif name == gameObject.player2User and not gameObject.player2Action:
        gameObject.player2Action = action
    gameObject.save()


@database_sync_to_async
def actionChecker(room_name, checker):
    # Check if both actions have been assigned, return t/f
    gameObject = models.Game.objects.get(gameRoom=room_name)
    if gameObject.player1Action != None and gameObject.player2Action != None:
        checker[0] = True
        return
    checker[0] = False
    return


def checkWin(gameObject):
    # Check if someone lost, assign winner
    if gameObject.player1HP <= 0 or gameObject.player2HP <= 0:
        gameObject.gameOver = True
        if gameObject.player1HP <= 0:
            gameObject.winner = gameObject.player2User
        else:
            gameObject.winner = gameObject.player1User
        gameObject.save()
        return True
    return False


def special(player1, char1, player2, char2, turnRecord):
    # Define a special attack for each character
    if char1.Name == "Fortune Teller":
        player2.HP = player2.HP - 20
        turnRecord[0] = turnRecord[0] + \
            "%s throws a crystal ball!\n" % (char1.Name)
    elif char1.Name == "Guru":
        player1.HP = player1.HP + 50
        turnRecord[0] = turnRecord[0] + \
            "%s heals from cosmic vibrations!\n" % (char1.Name)
    elif char1.Name == "Medium":
        player2.Dodge = -100
        turnRecord[0] = turnRecord[0] + \
            "%s surrounds foe with spirits!\n" % (char1.Name)


def saveGame(player1, player2, gameObject):
    # Save the game state, should happen every time it changes
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


def resolve(player1, act1, player2, act2, char1, char2, gameObject):
    # Just apply to game in order act1 and act2 based on the character stats
    turnRecord = [""]
    if checkWin(gameObject) == True:
        turnRecord = "The game is over!"
        return turnRecord

    # PLAYER 1 ACTION

    if act1 == "Attack":
        if random.randint(1, 100) > player2.Dodge:
            player2.HP = player2.HP - player1.Attack
            turnRecord[0] = turnRecord[0]+"%s attacks %s, dealing %d damage!\n" % (
                char1.Name, char2.Name, player1.Attack)
        else:
            turnRecord[0] = turnRecord[0] + \
                "%s's attack misses %s!\n" % (char1.Name, char2.Name)
        player1.Attack = char1.Attack  # reset any attack bonuses
        player2.Dodge = char2.Dodge  # reset dodge bonuses
        saveGame(player1, player2, gameObject)
        if checkWin(gameObject):
            turnRecord[0] = turnRecord[0] + "And the game is over!"
            return turnRecord[0]

    elif act1 == "Dodge":
        player1.Dodge = char1.Dodge + 50
        turnRecord[0] = turnRecord[0]+"%s is ready to dodge!\n" % (char1.Name)
        saveGame(player1, player2, gameObject)

    elif act1 == "Power":
        player1.Attack = char1.Attack*2
        turnRecord[0] = turnRecord[0]+"%s readies to strike!\n" % (char1.Name)
        saveGame(player1, player2, gameObject)

    elif act1 == "Special":
        a = 1  # aka do nothing yet
        special(player1, char1, player2, char2, turnRecord)
        saveGame(player1, player2, gameObject)
        if checkWin(gameObject):
            turnRecord[0] = turnRecord[0] + "And the game is over!"
            return turnRecord[0]

    # PLAYER 2 ACTION

    if act2 == "Attack":
        if random.randint(1, 100) > player1.Dodge:
            player1.HP = player1.HP - player2.Attack
            turnRecord[0] = turnRecord[0]+"%s attacks %s, dealing %s damage!\n" % (
                char2.Name, char1.Name, player2.Attack)
        else:
            turnRecord[0] = turnRecord[0] + \
                "%s's attack misses %s!\n" % (char2.Name, char1.Name)
        player2.Attack = char2.Attack  # reset any attack bonuses
        player1.Dodge = char1.Dodge  # reset dodge bonuses
        saveGame(player1, player2, gameObject)
        if checkWin(gameObject):
            turnRecord[0] = turnRecord[0] + "And the game is over!"
            return turnRecord[0]

    elif act2 == "Dodge":
        player2.Dodge = char2.Dodge + 50
        turnRecord[0] = turnRecord[0]+"%s is ready to dodge!\n" % (char2.Name)
        saveGame(player1, player2, gameObject)

    elif act2 == "Power":
        player2.Attack = char2.Attack*2
        turnRecord[0] = turnRecord[0]+"%s readies to strike!\n" % (char2.Name)
        saveGame(player1, player2, gameObject)

    elif act2 == "Special":
        special(player2, char2, player1, char1, turnRecord)
        saveGame(player1, player2, gameObject)
        if checkWin(gameObject):
            turnRecord[0] = turnRecord[0] + "And the game is over!"
            return turnRecord[0]

    # Reset actions
    gameObject.player1Action = None
    gameObject.player2Action = None
    gameObject.save()
    saveGame(player1, player2, gameObject)
    return turnRecord[0]


@database_sync_to_async
def turn(room_name, turnRecord):
    # Get set up to resolve a turn, grab all the relevant stats and game info
    # Get game object
    gameObject = models.Game.objects.get(gameRoom=room_name)
    char1 = characters.get(gameObject.player1Char)
    char2 = characters.get(gameObject.player2Char)
    act1 = gameObject.player1Action
    act2 = gameObject.player2Action

    # Check speed, then resolve with either player1 or player 2 going first
    if char1.Speed >= char2.Speed:
        player1 = Player(gameObject.player1User, gameObject.player1HP,
                         gameObject.player1Attack, gameObject.player1Dodge)
        player2 = Player(gameObject.player2User, gameObject.player2HP,
                         gameObject.player2Attack, gameObject.player2Dodge)
        turnRecord[0] = resolve(player1, act1, player2,
                                act2, char1, char2, gameObject)
    else:
        player1 = Player(gameObject.player2User, gameObject.player2HP,
                         gameObject.player2Attack, gameObject.player2Dodge)
        player2 = Player(gameObject.player1User, gameObject.player1HP,
                         gameObject.player1Attack, gameObject.player1Dodge)
        turnRecord[0] = resolve(player1, act2, player2,
                                act1, char2, char1, gameObject)


@database_sync_to_async
def joinGame(room_name, name):
    # Join as p2 if possible
    gameObject = models.Game.objects.get(gameRoom=room_name)
    if not gameObject.player2User and name != gameObject.player1User:
        gameObject.player2User = name
        gameObject.save()
