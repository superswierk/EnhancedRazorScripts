import sys
from System.Collections.Generic import List
from System import Byte, Int32
from math import sqrt
import System.IO

pathToScript = Misc.ScriptCurrent()
directoryPath = pathToScript.rsplit("\\",1)[0]

fileList = System.IO.Directory.GetFiles(directoryPath, "mineSpots_*")
prefix = "mineSpots_"
suffix = ".txt"

mapTable = {}

if fileList.Count == 0:
    print("ERROR! brakuje pliku mineSpots_Tymczasowa.txt\nUzyj skryptu sys_MakeMineSpots.py aby stworzyc pierwsza mape")
    sys.exit()

idI = 0
for file in fileList:
    fileBody = System.IO.File.ReadAllText(file)
    mname = file.rsplit("\\",1)[1]
    mname = mname[len(prefix):]
    mname = mname[:-len(suffix)]
    mapTable[mname] = { "id" : idI, "code" : fileBody }
    idI = idI + 1
    
silentMode = False
lumberThumb = "https://i.imgur.com/FAb0xg0.png"
deadThumb = "https://i.imgur.com/QjVeOoA.png"
enemyThumb = "https://i.imgur.com/YvbQw56.png"
lvlupThumb = "https://i.imgur.com/j5rUy80.png"
foodThumb = "https://i.imgur.com/uB0tTVj.png"
miningThumb = "https://i.imgur.com/cEvazS3.png"

rightHand = Player.CheckLayer( 'RightHand' )
leftHand = Player.CheckLayer( 'LeftHand' )

oreOptions = {
    "silent_mode" : {"id" : 996, "state" : False},
    "send_discord" : {"id" : 997, "state" : False},
    "all" : {"id" : 101, "state" : True},
    "only_titan" : {"id" : 102, "state" : False},
    "no_iron" : {"id" : 100, "state" : False}
}

ORES = {
    "zelazo": 0x0000, #0x1BF2
    "zloto": 0x0461,
    "srebro": 0x0515,
    "veryt": 0x0590,
    "blackrock": 0x0455,
    "agapit": 0x0400,
    "valoryt": 0x07d1,
    "mytheril": 0x0528,
    "azuryt": 0x04df,
    "bloodrock": 0x051d,
    "royal": 0x04b9,
    "tytan": 0x0415,
    "grafit": 0x03e7,
    "zwykle": 0x0000, #0x1BD7
    "dab": 0x0096,
    "orzech": 0x0611,
    "cedr": 0x0094,
    "cis": 0x0220,
    "cyprys": 0x0091
}

sendDiscordMgs = False

stringCodeToRun = ""

spots = []

noIronMode = False

def isInTable(value, table):
    for item in table:
        if item == value:
            return True
    return False

getOnlyOre = []
def shoudGatherOre(oreId):
    global getOnlyOre
    if getOnlyOre.Count == 0:
        return True
    return isInTable(oreId, getOnlyOre)
        
     

class Spot:
    x = None
    y = None
    
    def __init__ ( self, x, y):
        self.x = x
        self.y = y

        
###UI code start 
setX = 125 
setY = 125
offsetLabelY = 20
offsetRadioY = 45
offsetButtonY = 170
oreID = 0x19B9 

def sendgump():
    global mapTable
    if  Misc.CheckSharedValue("miningGumpState") == True:
        miningGumpState = Misc.ReadSharedValue("miningGumpState")
    else:
        miningGumpState = None

    
    gd = Gumps.CreateGump(movable=True) 
    
    Gumps.AddPage(gd, 0)
    Gumps.AddBackground(gd, 0, 0, 310, (mapTable.Count + 4) * 20 + offsetRadioY, 2620) 

    iY = 0
    Gumps.AddLabel(gd,15,iY + offsetLabelY,2407,'Wybierz kopalnie i rude:')
    
    Gumps.AddGroup(gd,100)
    for mapname in mapTable:
        defaultState = False
        if miningGumpState is None:
            if iY == 0:
                defaultState = True
        else:
            defaultState = isInTable(mapTable[mapname]['id'], miningGumpState)
        Gumps.AddRadio(gd,15,iY + offsetRadioY,209,208,defaultState,mapTable[mapname]['id'])
        Gumps.AddLabel(gd,35,iY + offsetRadioY,2407,mapname)
        iY = iY + 20
        
        
        
    if miningGumpState is not None:
        oreOptions['all']['state'] = isInTable(oreOptions['all']['id'], miningGumpState)
        oreOptions['only_titan']['state'] = isInTable(oreOptions['only_titan']['id'], miningGumpState)
        oreOptions['no_iron']['state'] = isInTable(oreOptions['no_iron']['id'], miningGumpState)
        oreOptions['send_discord']['state'] = isInTable(oreOptions['send_discord']['id'], miningGumpState)
        oreOptions['silent_mode']['state'] = isInTable(oreOptions['silent_mode']['id'], miningGumpState)
    iY = 0
    Gumps.AddGroup(gd,200)
    Gumps.AddRadio(gd,110,iY + offsetRadioY,209,208,oreOptions['all']['state'],oreOptions['all']['id'])
    Gumps.AddLabel(gd,135,iY + offsetRadioY,2407,"Wszystko")
    iY = iY + 20
    Gumps.AddRadio(gd,110,iY + offsetRadioY,209,208,oreOptions['only_titan']['state'],oreOptions['only_titan']['id'])
    Gumps.AddLabel(gd,135,iY + offsetRadioY,2407,"Tylko Tytan")
    iY = iY + 20
    
    Gumps.AddRadio(gd,110,iY + offsetRadioY,209,208,oreOptions['no_iron']['state'],oreOptions['no_iron']['id'])
    Gumps.AddLabel(gd,135,iY + offsetRadioY,2407,"Bez Zelaza")
    iY = iY + 20
    
    iY = 0
    Gumps.AddCheck(gd,225,iY + offsetRadioY,210, 211,oreOptions['send_discord']['state'],oreOptions['send_discord']['id'])
    Gumps.AddLabel(gd,250,iY + offsetRadioY,2407,"Discord")
    iY = iY + 20

    Gumps.AddCheck(gd,225,iY + offsetRadioY,210, 211,oreOptions['silent_mode']['state'],oreOptions['silent_mode']['id'])
    Gumps.AddLabel(gd,250,iY + offsetRadioY,2407,"Wyrzucaj")
    
    
    
    iY = iY + 40
    Gumps.AddButton(gd,220,iY + offsetRadioY,247,248,456,1,0)

    Gumps.SendGump(767676, Player.Serial, setX, setY, gd.gumpDefinition, gd.gumpStrings)
    buttoncheck()

def buttoncheck():
    global mapTable
    global stringCodeToRun
    global getOnlyOre
    global sendDiscordMgs
    global silentMode
    global noIronMode
    Gumps.WaitForGump(767676, 60000)
    Gumps.CloseGump(767676)
    gdata = Gumps.GetGumpData(767676)
    miningGumpState = []
    if Misc.CheckSharedValue("miningGumpState") == True:
        Misc.RemoveSharedValue("miningGumpState")
    switchList = gdata.switches
    print(gdata.switches)
    if switchList.Count >= 2:
        for mapname in mapTable:
            if mapTable[mapname]["id"] == switchList[0]:
                miningGumpState.Add(mapTable[mapname]["id"])
                stringCodeToRun = mapTable[mapname]["code"]
        print("Mapa przeczytana")
        if switchList[1] == oreOptions['only_titan']['id']:
            getOnlyOre = []
            getOnlyOre.Add(ORES["tytan"])
            miningGumpState.Add(oreOptions['only_titan']['id'])
        elif switchList[1] == oreOptions['no_iron']['id']:
            getOnlyOre = []
            noIronMode = True
            miningGumpState.Add(oreOptions['no_iron']['id'])
        else:
            getOnlyOre = []
            miningGumpState.Add(oreOptions['all']['id'])
        if isInTable(oreOptions['send_discord']['id'], switchList) == True:
            sendDiscordMgs = True
            miningGumpState.Add(oreOptions['send_discord']['id'])
        if isInTable(oreOptions['silent_mode']['id'], switchList) == True:
            silentMode = True
            miningGumpState.Add(oreOptions['silent_mode']['id'])
    else:
        stringCodeToRun = "sys.exit()"
        print("error nie zaznaczyles nic ")
        sys.exit()
    Misc.SetSharedValue("miningGumpState",miningGumpState)       
###UI code end

sendgump()
print("Koniec Gumpa")
Misc.Pause(1000)
if sendDiscordMgs == True:
    print("wlazlo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    from Scripts.EnhancedRazorScripts.misc_Discord import *


if silentMode == False:
    petOne = Target.PromptTarget( 'Wybierz konia Nr1' )
    if getOnlyOre.Count == 0:
        Player.ChatSay( 77, '.pojemnik' )
        Target.WaitForTarget( 5000 , True )
        Target.TargetExecute(petOne)
        if noIronMode == False:
            petTwo = Target.PromptTarget( 'Wybierz konia Nr2' )
            Player.ChatSay( 77, '.pojemnik' )
            Target.WaitForTarget( 25000 , True )
            Target.TargetExecute(petTwo)
        else:
            Misc.Pause(1000)
            itemInPet = Target.PromptTarget( 'jakas rzecz w pojemnniku' )
    else:
        Player.ChatSay( 77, '.pojemnik' )
        Target.WaitForTarget( 25000 , True )
        Target.TargetExecute(Player.Backpack)

def SetDigSpots():
    global spots
    global stringCodeToRun
    spots = []
    exec(stringCodeToRun)

    
def MoveToSpot():
    global spots
    print("Move To Spot")
    if silentMode == False:
        Player.ChatSay( 77, 'Za mna!' )
        Misc.Pause(1500)
        Player.ChatSay( 77, 'za mna' )
        Misc.Pause(1500)
    if sqrt( pow( ( spots[0].x - Player.Position.X ), 2 ) + pow( ( spots[0].y - Player.Position.Y ), 2 ) ) > 20:
        print("ERROR point to far away")
        sys.exit()
    prevPosX = Player.Position.X
    prevPosY = Player.Position.Y 
    Player.PathFindTo(spots[0].x,spots[0].y,Player.Position.Z)
    while sqrt( pow( ( spots[0].x - Player.Position.X ), 2 ) + pow( ( spots[0].y - Player.Position.Y ), 2 ) )  >= 1:
        Misc.Pause(500)
        if prevPosX == Player.Position.X and prevPosY == Player.Position.Y:
            Player.PathFindTo(spots[0].x,spots[0].y,Player.Position.Z)
        prevPosX = Player.Position.X
        prevPosY = Player.Position.Y
    Misc.SendMessage( '--> Reached DigSpot: %i, %i' % ( spots[ 0 ].x, spots[ 0 ].y ), 77 )
    spots.pop( 0 )
    if silentMode == False:
        Player.ChatSay( 77, 'Podejdzcie!' )
        Misc.Pause(2000)
        Player.ChatSay( 77, 'Podejdzcie!' )
        Misc.Pause(2000)
    if spots.Count == 0:
        SetDigSpots()

def fullCheck():
    if Journal.Search( 'zwierze nie moze') or Journal.Search( 'too heavy'):
        Player.HeadMessage(33, 'KON JEST PELNY STOP!')
        if sendDiscordMgs == True:
            sendDiscord("Przepelnienie koni trzeba je oproznic", 15291726, lumberThumb);
        Misc.Pause(3000)
        sys.exit()

def GetNumberOfOresInPet():
    global petOne
    global oreID
    
    remount = False
    if not Mobiles.FindBySerial( petOne ):
        remount = True
        print("use3")
        Mobiles.UseMobile( Player.Serial )
        Misc.Pause( 700 )

    numberOfOres = 0
    petObject = Mobiles.FindBySerial( petOne )
    if petObject is not None:
        print(petObject)
        for item in petObject.Contains:
            if item.ItemID == oreID:
                numberOfOres += item.Amount
    else:
        if sendDiscordMgs == True:
            sendDiscord("Cos sie popuslo - kon zaginal", 15291726, lumberThumb);
        Misc.Pause("Cos sie popuslo - Kon za dalego")
        Misc.Pause(3000)
        #sendEmailMessage("Cos sie popuslo", "Nie znalazlem konia")
        sys.exit()

    if remount:
        print("use4")
        Mobiles.UseItem( petOne )
        Misc.Pause( 700 )

    return numberOfOres

def FromPetToGround():
    print("pet to ground!")
    itemFrom = Items.FindBySerial(itemInPet)
    if itemFrom is None or itemFrom.Container is None:
        Misc.SendMessage("ERROR upewnij sie ze za drugim razem wskazales item w juce",1100)
        sys.exit()
    Items.FindBySerial( itemFrom.Container )
    containerOne = Items.FindBySerial( itemFrom.Container )#Items.FindBySerial(1416815009) 
    #containerTwo = Mobiles.FindBySerial(petOne)
    for item in containerOne.Contains:
        if item.ItemID == oreID and item.Color == 0x0000:
            print("dropping")
            Items.DropItemGroundSelf(item,0)
            Misc.Pause( 700 )
    
def MoveToPet():
    if Player.Mount:
        print("use1")
        Mobiles.UseMobile( Player.Serial )
        Misc.Pause( 700 )
    for item in Player.Backpack.Contains:
        if item.ItemID == oreID and shoudGatherOre(item.Color) == True:
            numberOfOresInPet = GetNumberOfOresInPet()
            if numberOfOresInPet + item.Amount < 1900:
                Items.Move( item, petOne, 0 )
                Misc.Pause( 700 )
    fullCheck()
    if not Player.Mount:
        print("use2")
        Mobiles.UseMobile( petOne )
        Misc.Pause( 700 )

def MoveToGround(withPet = True):
    global silentMode
    Misc.SendMessage( 'MoveToGroundOrPet', 90 )
    if getOnlyOre.Count > 0 and withPet == True and silentMode == False:
        MoveToPet()
    if noIronMode == True and withPet == True and silentMode == False:
        FromPetToGround()
    for item in Player.Backpack.Contains:
        if item.ItemID == oreID and (silentMode == True or shoudGatherOre(item.Color) == False):
            Items.DropItemGroundSelf(item,0)
            Misc.Pause( 700 )
def doMine():
    MoveToGround(False)
    Misc.SendMessage( 'doMine', 90 )
    if Player.IsGhost == True:
        if sendDiscordMgs == True:
            sendDiscord("Nie zyjesz", 15291726, deadThumb);
        Misc.Pause(2000)
        sys.exit()
    Misc.Pause(1000)
    pickaxe = Player.GetItemOnLayer( 'RightHand' ).Serial
    if pickaxe == None:
        Player.HeadMessage( 1100, 'Youre out of pickaxes!' )
        return
    Items.UseItem( pickaxe )
    Target.WaitForTarget( 2000, True )
    Target.TargetExecuteRelative( Player.Serial, 1 )      

SetDigSpots()
# Start mining
Misc.SendMessage( 'Start', 90 )
MoveToGround()
MoveToSpot()
Timer.Create('eatingLogTimer', 120000)
Timer.Create('digTimer',9000)
print("poczatek pracy")
guards = False
Journal.Clear()
doMine()
while True:
    if Player.IsGhost == True:
        Misc.SendMessage("UMARLES!")
        if sendDiscordMgs == True:
            sendDiscord("Nie zyjesz", 15291726, deadThumb);
        Misc.Pause(2000)
        Misc.Pause(200)
        break
    if Journal.Search("Przyciagnales uwage",) or Journal.Search("podchodzi zobaczyc co ciekawego"):
        guards = True
        savedTime = 0
        if Timer.Check('digTimer'):
           savedTime = Timer.Remaining('digTimer')
        Misc.Pause(1000)
        Journal.Clear()
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        if sendDiscordMgs == True:
            sendDiscord("Jakas potwora sie pojawila", 15291726, enemyThumb);
        Misc.Pause(200)
        MoveToSpot()
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        Misc.Pause(1000)
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        if savedTime > 0:
            Timer.Create('digTimer',savedTime)

    if Timer.Check('digTimer') == False:
        if guards == True:
            guards = False
        else:
            MoveToSpot()
        print("koniec digTimer")
        Timer.Create('digTimer',9000)
        doMine()
    if Journal.Search('Nie masz miejsca'):
        if sendDiscordMgs == True:
            sendDiscord("Nie masz juz miejsca na rude", 15291726, miningThumb);
        Misc.Pause(2000)
        sys.exit()

    if Journal.Search('Zaczynasz kopac') or Journal.Search('Wykopal') or Journal.Search('Nie udalo Ci sie wykopac') or Journal.Search('W tym miejscu')or Journal.Search('Moze sprobuje obok') or Journal.Search('Moze dalej') or Journal.Search('Znalazl'):
        if noIronMode == True and Journal.Search('Zaczynasz kopac') and silentMode == False:
            Mobiles.UseMobile( petOne )
            Misc.Pause( 700 )
        Journal.Clear('Zaczynasz kopac')
        Journal.Clear('Wykopal')
        Journal.Clear('Nie udalo Ci sie wykopac')
        Journal.Clear('W tym miejscu')
        Journal.Clear('Moze sprobuje obok')
        Journal.Clear('Moze dalej')
        Journal.Clear('Znalazl')
        MoveToGround()
        Timer.Create('digTimer',9000)
    if Journal.Search('Trzasn'):
        Journal.Clear('Trzasn')
        MoveToGround()
        Misc.Pause(20000)
        Timer.Create('digTimer',9000)
    Misc.Pause(400)
