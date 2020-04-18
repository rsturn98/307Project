

class Character:
    def __init__(self, Name, HP, Attack, Dodge, Speed):
        self.Name = Name
        self.HP = HP
        self.Attack = Attack
        self.Dodge = Dodge
        self.Speed = Speed

CharacterDict = {
        'Brutus': Character('Brutus',100,20,20,10),
        'Terminator': Character('Terminator',500,100,0,0),
        'Wizard': Character('Wizard',20,250,60,50)
        }


def get(Name):
    return CharacterDict.get(Name)
def getAll():
    CharList = [c for c in CharacterDict.values()]
    return CharList
def nameList():
    namelist = [c.Name for c in CharacterDict.values()]
    return namelist
