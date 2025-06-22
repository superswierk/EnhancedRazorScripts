import sys
from System.Collections.Generic import List
from System import Byte, Int32
from math import sqrt
import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer
from Scripts.EnhancedRazorScripts.misc_Discord import *
import System.IO

pathToScript = Misc.ScriptCurrent()
directoryPath = pathToScript.rsplit("\\",1)[0]

fileList = System.IO.Directory.GetFiles(directoryPath, "mineSpots_*")
prefix = "mineSpots_"
suffix = ".txt"

mapTable = {}
print("test")
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

useMount = False
usePetStorage = False

rightHand = Player.CheckLayer( 'RightHand' )
leftHand = Player.CheckLayer( 'LeftHand' )

stringCodeToRun = ""

spots = []

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

def sendgump():
    global mapTable
    gd = Gumps.CreateGump(movable=True) 
    
    Gumps.AddPage(gd, 0)
    Gumps.AddBackground(gd, 0, 0, 240, (mapTable.Count + 3) * 20 + offsetRadioY, 2620) 

    iY = 0
    Gumps.AddLabel(gd,15,iY + offsetLabelY,2407,'Wybierz kopalnie w jakiej jestes:')

    for mapname in mapTable:
        defaultState = False
        if iY == 0:
            defaultState = True
        Gumps.AddRadio(gd,15,iY + offsetRadioY,209,208,defaultState,mapTable[mapname]['id'])
        Gumps.AddLabel(gd,35,iY + offsetRadioY,2407,mapname)
        iY = iY + 20

    iY = iY + 10
    Gumps.AddButton(gd,140,iY + offsetRadioY,247,248,456,1,0)

    Gumps.SendGump(767676, Player.Serial, setX, setY, gd.gumpDefinition, gd.gumpStrings)
    buttoncheck()

def buttoncheck():
    global mapTable
    global stringCodeToRun
    Gumps.WaitForGump(767676, 60000)
    Gumps.CloseGump(767676)
    gdata = Gumps.GetGumpData(767676)
    switchList = gdata.switches
    if switchList.Count >= 1:
        for mapname in mapTable:
            if mapTable[mapname]["id"] == switchList[0]:
                stringCodeToRun = mapTable[mapname]["code"]
        print("Mapa przeczytana")
    else:
        stringCodeToRun = "sys.exit()"
        print("error nie zaznaczyles nic ")
        sys.exit()

###UI code end

sendgump()
Misc.Pause(1000)

if silentMode == False:
    beetle = Target.PromptTarget( 'Wybierz konia beetle' )
    Player.ChatSay( 77, '.pojemnik' )
    Target.WaitForTarget( 5000 , True )
    Target.TargetExecute(beetle)

    newBeetle = Target.PromptTarget( 'Wybierz konia newBeetle' )
    Player.ChatSay( 77, '.pojemnik' )
    Target.WaitForTarget( 5000 , True )
    Target.TargetExecute(newBeetle)
        
def hide():
    if  Player.BuffsExist('Ukrywanie') == False and Timer.Check('hideTimer') == False:
        Misc.Pause( 700 )
        Player.UseSkill('Ukrywanie')
        Timer.Create('hideTimer',10000)
        Misc.Pause( 1000 )

    
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
    Player.PathFindTo(spots[0].x,spots[0].y,Player.Position.Z)
    while sqrt( pow( ( spots[0].x - Player.Position.X ), 2 ) + pow( ( spots[0].y - Player.Position.Y ), 2 ) )  >= 2:
        Misc.Pause(50)
    Misc.SendMessage( '--> Reached DigSpot: %i, %i' % ( spots[ 0 ].x, spots[ 0 ].y ), 77 )
    spots.pop( 0 )
    if silentMode == False:
        Player.ChatSay( 77, 'Podejdzcie!' )
        Misc.Pause(2000)
        Player.ChatSay( 77, 'Podejdzcie!' )
        Misc.Pause(2000)
    if spots.Count == 0:
        SetDigSpots()


def MoveToGround():
    Misc.SendMessage( 'MoveToGround', 90 )
    for item in Player.Backpack.Contains:
        if item.ItemID == 0x19B9:
            Items.DropItemGroundSelf(item,0)
            Misc.Pause( 700 )
def doMine():
    MoveToGround()
    Misc.SendMessage( 'doMine', 90 )
    if Player.IsGhost == True:
        sendDiscord("Nie zyjesz", 15291726, deadThumb);
        Misc.Pause(2000)
        sys.exit()
    hide()
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
Timer.Create('digTimer',8200)
print("poczatek pracy")
guards = False
Journal.Clear()
doMine()
while True:
    if Player.IsGhost == True:
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
        sendDiscord("Nie masz juz miejsca na rude", 15291726, miningThumb);
        Misc.Pause(2000)
        sys.exit()

    if Journal.Search('Wykopal') or Journal.Search('Nie udalo Ci sie wykopac') or Journal.Search('W tym miejscu')or Journal.Search('Moze sprobuje obok') or Journal.Search('Moze dalej') or Journal.Search('Znalazl'):
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
        #print("trzasnales kontynuuj")
        #doMine()
    Misc.Pause(400)


