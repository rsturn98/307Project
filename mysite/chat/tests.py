from django.test import TestCase
import asyncio
from . import models, game, characters
# Create your tests here.

class gameTestCase(TestCase):
    def setUp(self):
        models.Rooms.objects.create(roomname="TestRoom")
        models.Game.objects.create(gameRoom=models.Rooms.objects.get(roomname="TestRoom"),
                player1User="TestP1",
                player2User="TestP2", 
                player1Char="TestChar1",
                player2Char="TestChar2",
                )
    def test_checkWin(self):
        roomname = "TestRoom"
        gameObject = models.Game.objects.get(gameRoom=roomname)
        gameObject.player1HP = 0
        gameObject.player2HP = 100
        self.assertEqual(game.checkWin(gameObject), True)

    def test_saveGame(self):
        roomname = "TestRoom"
        gameObject = models.Game.objects.get(gameRoom=roomname)
        testplayer1 = game.Player("TestP1",1000,101,111)
        testplayer2 = game.Player("TestP2",2000,202,222)
        game.saveGame(testplayer1,testplayer2,gameObject)
        self.assertEqual(gameObject.player1HP,1000)
        self.assertEqual(gameObject.player1Attack,101)
        self.assertEqual(gameObject.player1Dodge,111)
        self.assertEqual(gameObject.player2HP,2000)
        self.assertEqual(gameObject.player2Attack,202)
        self.assertEqual(gameObject.player2Dodge,222)

    def test_resolve(self):
        roomname = "TestRoom"
        gameObject = models.Game.objects.get(gameRoom=roomname)
        gameObject.player1HP = 0
        turnRecord = ""
        testplayer1 = game.Player("TestP1",1000,101,111)
        testplayer2 = game.Player("TestP2",2000,202,222)
        testAct1 = "Dodge"
        testAct2 = "Dodge"
        testChar1 = "Tester the Mighty"
        testChar2 = "Testmaster the Wizard"
        turnRecord = game.resolve(testplayer1,testAct1,testplayer2,testAct2,testChar1,testChar2,gameObject)
        self.assertEqual(turnRecord,"The game is over!")
