# OG from AbelGoodwin https://github.com/hampgoodwin/razorenhancedscripts
# Modified by Matsamilla
#
# Last updated: 12/2/21

from Scripts.EnhancedRazorScripts.misc_Discord import *
from System.Collections.Generic import List
from System import Byte, Int32
import sys

setX = 125 
setY = 125
offsetLabelY = 20
offsetRadioY = 45
offsetButtonY = 170
runDrection = "Left"

multiMode = False
silentMode = False
dropLogs = False
scanRadius = 40


isMeranti = False

STATICTREES = {
    "Wszystkie": 11,
    "Wszystkie bez zwyklych": 12,
    "Ohii": 13,
    "Wierzba": 14,
    "Orzech": 15,
    "Dab": 16,
    "Cyprys": 17,
    "Cis": 18,
    "Cedr": 19,
    "Meranti": 20,
    "Zwykle": 21,
    "Zwykle i Ohii": 22
}

def isInTable(value, table):
    for item in table:
        if item == value:
            return True
    return False




def sendgump():
    gd = Gumps.CreateGump(movable=True) 
    
    Gumps.AddPage(gd, 0)
    Gumps.AddBackground(gd, 0, 0, 200, (STATICTREES.Count + 5) * 20 + offsetRadioY, 2620) 

    iY = 0
    Gumps.AddLabel(gd,15,iY + offsetLabelY,2407,'Wybierz drzewa do ciecia:')
    for i, item in enumerate(STATICTREES):
        defaultVal = False 
        if i == 0:
            defaultVal = True
        Gumps.AddRadio(gd,15,iY + offsetRadioY,209,208,defaultVal,STATICTREES[item])
        Gumps.AddLabel(gd,35,iY + offsetRadioY,2407,item)
        iY = iY + 20

    iY = iY + 20
    
    Gumps.AddCheck(gd,40,iY + offsetRadioY,210, 211,multiMode,9)
    Gumps.AddLabel(gd,65,iY + offsetRadioY,2407,"Multi/Runic")
    
    iY = iY + 30
    
    iX = 10
    Gumps.AddButton(gd,iX + 145,iY + offsetRadioY,9702,9703,456,1,0)
    Gumps.AddButton(gd,iX + 15,iY + offsetRadioY,9706,9707,455,1,0)
    Gumps.AddButton(gd,iX + 85,iY + offsetRadioY + 18,9704,9705,457,1,0)
    
    Gumps.AddLabel(gd,iX + 40,iY + offsetRadioY,2407,'Kirunek ucieczki')
    Gumps.SendGump(696969, Player.Serial, setX, setY, gd.gumpDefinition, gd.gumpStrings)
    buttoncheck()

#wszystkie drzewa
treeStaticIDs = [ 0x0C95, 0x0C96, 0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0CA6,
    0x0CA8, 0x0CAA, 0x0CAB, 0x0CC3, 0x0CC4, 0x0CC8, 0x0CCA, 0x0CCB,
    0x0CCC, 0x0CCD, 0x0CD0, 0x0CD3, 0x0CD6, 0x0CD8, 0x0CDA, 0x0CDD, 0x0CE0,
    0x0CE3, 0x0CE6, 0x0CF8, 0x0CFB, 0x0CFE, 0x0D01, 0x0D25, 0x0D27, 0x0D35,
    0x0D37, 0x0D38, 0x0D42, 0x0D43, 0x0D59, 0x0D70, 0x0D85, 0x0D94, 0x0D96,
    0x0D98, 0x0D9A, 0x0DA0, 0x0DA2, 0x0DA8, 0x12B9,
    0x0C9E, ]


def buttoncheck():
    global isMeranti
    global treeStaticIDs
    global runDrection
    global multiMode
    Gumps.WaitForGump(696969, 60000)
    Gumps.CloseGump(696969)
    gdata = Gumps.GetGumpData(696969)
    if gdata.buttonid == 456:
        runDrection = "Right"
    elif gdata.buttonid == 455:
        runDrection = "Left"
    else:
        runDrection = "Dont"
    print(f"Will run: {runDrection}")
    switchList = gdata.switches
    if switchList.Count >= 1:
        if switchList[0] == STATICTREES['Wszystkie']:
            treeStaticIDs = [ 0x0C95, 0x0C96, 0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0CA6,
                0x0CA8, 0x0CAA, 0x0CAB, 0x0CC3, 0x0CC4, 0x0CC8, 0x0CCA, 0x0CCB,
                0x0CCC, 0x0CCD, 0x0CD0, 0x0CD3, 0x0CD6, 0x0CD8, 0x0CDA, 0x0CDD, 0x0CE0,
                0x0CE3, 0x0CE6, 0x0CF8, 0x0CFB, 0x0CFE, 0x0D01, 0x0D25, 0x0D27, 0x0D35,
                0x0D37, 0x0D38, 0x0D42, 0x0D43, 0x0D59, 0x0D70, 0x0D85, 0x0D94, 0x0D96,
                0x0D98, 0x0D9A, 0x0DA0, 0x0DA2, 0x0DA8, 0x12B9,
                0x0C9E, ]
            print("Wszystkie")
        elif switchList[0] == STATICTREES['Wszystkie bez zwyklych']:
            treeStaticIDs = [ 0x0C95, 0x0C96, 0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0CA6,
                0x0CA8, 0x0CAA, 0x0CAB, 0x0CC3, 0x0CC4, 0x0CC8, 0x0CCA, 0x0CCB,
                0x0CCC, 0x0CD6, 0x0CD8, 0x0CDA, 0x0CDD, 0x0CE0,
                0x0CE3, 0x0CE6, 0x0CF8, 0x0CFB, 0x0CFE, 0x0D01, 0x0D25, 0x0D27, 0x0D35,
                0x0D37, 0x0D38, 0x0D42, 0x0D43, 0x0D59, 0x0D70, 0x0D85, 0x0D94, 0x0D96,
                0x0D98, 0x0D9A, 0x0DA0, 0x0DA2, 0x0DA8, 0x12B9,
                0x0C9E, ]
            print("Wszystkie bez zwyklych")
        elif switchList[0] == STATICTREES['Ohii']:
            treeStaticIDs = [ 0x0C9E,0x0D3F ]
            print("Ohii")
        elif switchList[0] == STATICTREES['Wierzba']:
            treeStaticIDs = [ 0x0CE6 ]
            print("Wierzba")
        elif switchList[0] == STATICTREES['Orzech']:
            treeStaticIDs = [ 0x0CE3, 0x0CE0 ]
            print("Orzech")
        elif switchList[0] == STATICTREES['Dab']:
            treeStaticIDs = [ 0x0CDD, 0x0CDA ]
            print("Dab")
        elif switchList[0] == STATICTREES['Cyprys']:
            treeStaticIDs = [ 0x0D01, 0x0CFE ]
            print("Cyprys")
        elif switchList[0] == STATICTREES['Cis']:
            treeStaticIDs = [ 0x12B9 ]
            print("Cis")
        elif switchList[0] == STATICTREES['Cedr']:
            treeStaticIDs = [ 0x0CD6, 0x0CD8 ]
            print("Cedr")
        elif switchList[0] == STATICTREES['Meranti']:
            treeStaticIDs = [ 0x0D43, 0x0D85, 0x0D59, 0x0D70 ]
            isMeranti = True
            print("Meranti")
        elif switchList[0] == STATICTREES['Zwykle']:
            treeStaticIDs = [ 0x0CCD, 0x0CD0, 0x0CD3 ]
            print("Zwykle")
        elif switchList[0] == STATICTREES['Zwykle i Ohii']:
            treeStaticIDs = [ 0x0CCD, 0x0CD0, 0x0CD3, 0x0C9E ]
            print("Zwykle i Ohii")
        else:
            print("Default value")
        if isInTable(9, switchList):
            print("using MultiMode")
            multiMode = True
        else:
            print("using SingleMode")
            multiMode = False
    else:
        print("error nie zaznaczyles nic uzwyam domyslnego")


        
sendgump()
Misc.Pause(2000)       
        
lumberThumb = "https://i.imgur.com/FAb0xg0.png"
deadThumb = "https://i.imgur.com/QjVeOoA.png"
foodThumb = "https://i.imgur.com/uB0tTVj.png"
enemyThumb = "https://i.imgur.com/YvbQw56.png"
lvlupThumb = "https://i.imgur.com/j5rUy80.png"

# you want boards or logs?
logsToBoards = False



#********************
# serial of your beetle, logs go here when full
if dropLogs == False and logsToBoards == False:
    beetle = Target.PromptTarget( 'Wybierz konia beetle' )
    Player.ChatSay( 77, '.pojemnik' )
    Target.WaitForTarget( 25000 , True )
    Target.TargetExecute(beetle)

    newBeetle = Target.PromptTarget( 'Wybierz konia newBeetle' )
    Player.ChatSay( 77, '.pojemnik' )
    Target.WaitForTarget( 25000 , True )
    Target.TargetExecute(newBeetle)
else:
    beetle=0x51B04FF5
    newBeetle=0x51B04FF5

# Attack nearest grey script name (must be exact)
autoFightMacroName = 'pvm_AttackGrey.py'
sawId = 0x1035


# Trees where there is no longer enough wood to be harvested will not be revisited until this much time has passed
treeCooldown = 12000000 # 1,200,000 ms is 20 minutes

# Want this script to alert you for humaniods?
alert = False
#********************

chopCounter=0

# Parameters
#cyprys 0x0D01 0x0CFE 
# Parameters wszystkie bez zwyklych

# dab 0x0CDD
#treeStaticIDs = [ 0x0CCD, 0x0CD0, 0x0CD3]

'''
treeStaticIDs = [ 0x0C95, 0x0C96, 0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0CA6,
    0x0CA8, 0x0CAA, 0x0CAB, 0x0CC4, 0x0CC8, 0x0CCA, 0x0CCB,
    0x0CCC, 0x0CCD, 0x0CD0, 0x0CD3, 0x0CD6, 0x0CD8, 0x0CDA, 0x0CDD, 0x0CE0,
    0x0CE3, 0x0CE6, 0x0CF8, 0x0CFB, 0x0CFE, 0x0D01, 0x0D25, 0x0D27, 0x0D35,
    0x0D37, 0x0D38, 0x0D42, 0x0D43, 0x0D59, 0x0D70, 0x0D85, 0x0D94, 0x0D96,
    0x0D98, 0x0D9A, 0x0DA0, 0x0DA2, 0x0DA8, 0x12B9,
    0x0C9E, ]
'''
#wierzby
#treeStaticIDs = [ 0x0CD6, 0x0CD8 ]
EquipAxeDelay = 1000
TimeoutOnWaitAction = 4000
ChopDelay = 1000
runebookBank = 0x41EA8DEE # Runebook for bank
runebookTrees = 0x41EA8DEE # Runebook for tree spots
recallPause = 3000
dragDelay = 700
hideDelay = 300
logID = 0x1BDD
boardID = 0x1BD7
otherResourceID = [ 0x318F, 0x3199, 0x2F5F, 0x3190, 0x3191, ]
logBag = 0x401FA597 # Serial of log bag in bank
otherResourceBag = 0x40191C19 # Serial of other resource in bank
weightLimit = Player.MaxWeight - 10
bankX = 2051
bankY = 1343
axeList = [ 0x0F43 ]
rightHand = Player.CheckLayer( 'RightHand' )
leftHand = Player.CheckLayer( 'LeftHand' )

beetleGood = True


# Helper Functions
###################################
def getByItemID(itemid, source):
    #find an item id in container serial
    searchItem = Items.FindBySerial(source)
    if hasattr(searchItem,'Contains'):
        for item in searchItem.Contains:
            if item.ItemID == itemid:
                return item
            else:
                Misc.NoOperation()
    else:
        Misc.NoOperation()
###################################

# System Variables
from math import sqrt
import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer
tileinfo = List[Statics.TileInfo]
trees = []
treeCoords = None
blockCount = 0
lastRune = 5
onLoop = True

class Tree:
    x = None
    y = None
    z = None
    id = None
    
    def __init__ ( self, x, y, z, id ):
        self.x = x
        self.y = y
        self.z = z
        self.id = id

def hide():
    if  Player.BuffsExist('Ukrywanie') == False and Timer.Check('hideTimer') == False:
        Misc.Pause( hideDelay )
        Player.UseSkill('Ukrywanie')
        Timer.Create('hideTimer',10000)
        Misc.Pause( 1000 )
        
def RecallNextSpot():
    global lastRune

    Gumps.ResetGump()

    Misc.SendMessage('--> Recall to Spot', 77)

    Items.UseItem( runebookTrees )
    Gumps.WaitForGump( 1431013363, TimeoutOnWaitAction )
    Gumps.SendAction( 1431013363, lastRune )

    Misc.Pause( recallPause )

    lastRune = lastRune + 6
    if lastRune > 95:
        lastRune = 5

    EquipAxe()


def RecallBack():
    global lastRune

    Items.UseItem( runebookTrees )
    Gumps.WaitForGump( 1431013363, TimeoutOnWaitAction )
    Gumps.SendAction( 1431013363, lastRune )

    Misc.Pause( recallPause )

    EquipAxe()


def DepositInBank():
    global bankX
    global bankY
    while Player.Weight >= 140:
        Gumps.ResetGump()
        Items.UseItem( runebookBank )
        Gumps.WaitForGump( 1431013363, 10000 )
        Gumps.SendAction( 1431013363, 71 )
        Misc.Pause( recallPause )

        Player.ChatSay( 77, 'bank' )
        Misc.Pause( 300 )

        if Items.BackpackCount( logID, -1 ) > 0:
            while Items.BackpackCount( logID, -1 ) > 0:
                Misc.SendMessage( '--> Moving Log', 77 )
                Items.Move( item, logBag, 0 )
                Misc.Pause( dragDelay )

        if Items.BackpackCount( boardID, -1 ) > 0:
            while Items.BackpackCount( boardID, -1 ) > 0:
                Misc.SendMessage( '--> Moving Log', 77 )
                Items.Move( item, logBag, 0 )
                Misc.Pause( dragDelay )

        for otherid in otherResourceID:
            if item.ItemID == otherid:
                Misc.SendMessage( '--> Moving Other', 77 )
                Items.Move( item, otherResourceBag, 0 )
                Misc.Pause( dragDelay )
            else:
                Misc.NoOperation()


def ScanStatic():
    global treenumber
    global trees
    Misc.SendMessage('--> Scan Tile Started', 77)
    minX = Player.Position.X - scanRadius
    maxX = Player.Position.X + scanRadius
    minY = Player.Position.Y - scanRadius
    maxY = Player.Position.Y + scanRadius

    x = minX
    y = minY

    while x <= maxX:
        while y <= maxY:
            staticsTileInfo = Statics.GetStaticsTileInfo( x, y, Player.Map )
            if staticsTileInfo.Count > 0:
                for tile in staticsTileInfo:
                    for staticid in treeStaticIDs:
                        if staticid == tile.StaticID and not Timer.Check( '%i,%i' % ( x, y ) ):
                            #Misc.SendMessage( '--> Tree X: %i - Y: %i - Z: %i' % ( minX, minY, tile.StaticZ ), 66 )
                            trees.Add( Tree( x, y, tile.StaticZ, tile.StaticID ) )
            y = y + 1
        y = minY
        x = x + 1

    trees = sorted( trees, key = lambda tree: sqrt( pow( ( tree.x - Player.Position.X ), 2 ) + pow( ( tree.y - Player.Position.Y ), 2 ) ) )
    Misc.SendMessage( '--> Total Trees: %i' % ( trees.Count ), 77 )


def RangeTree():
    playerX = Player.Position.X
    playerY = Player.Position.Y
    treeX = trees[ 0 ].x
    treeY = trees[ 0 ].y
    if ( ( treeX >= playerX - 1 and treeX <= playerX + 1 ) and ( treeY >= playerY - 1 and treeY <= playerY + 1 )  ):
        return True
    else:
        return False

def MoveToTree():
    global chopCounter
    global trees
    global treeCoords
    global silentMode
    pathlock = 0
    if silentMode == False:
        Player.ChatSay( 77, 'Za mna!' )
        Misc.Pause(2000)
        Player.ChatSay( 77, 'za mna' )
        Misc.Pause(2000)
    Misc.SendMessage( '--> Moving to TreeSpot: %i, %i' % ( trees[ 0 ].x, trees[ 0 ].y ), 77 )
    Misc.Resync()
    treeCoords = PathFinding.Route()
    treeCoords.MaxRetry = 5
    treeCoords.Run = False
    treeCoords.StopIfStuck = False
    treeCoords.X = trees[ 0 ].x
    treeCoords.Y = trees[ 0 ].y + 1
    #Items.Message(trees[0], 1, "Here")

    if isMeranti == True:
        
        if sqrt( pow( ( treeCoords.X - Player.Position.X ), 2 ) + pow( ( treeCoords.Y - Player.Position.Y ), 2 ) ) > 20:
            print("ERROR point to far away")
            sys.exit()
        prevPosX = Player.Position.X
        prevPosY = Player.Position.Y    
        Player.PathFindTo(treeCoords.X,treeCoords.Y ,trees[ 0 ].z)
        
        while sqrt( pow( ( treeCoords.X - Player.Position.X ), 2 ) + pow( ( treeCoords.Y - Player.Position.Y ), 2 ) )  >= 1:
            print(f"odleglosc: {sqrt( pow( ( trees[0].x - Player.Position.X ), 2 ) + pow( ( trees[0].y - Player.Position.Y ), 2 ) )}")
            Misc.Pause(500)
            if prevPosX == Player.Position.X and prevPosY == Player.Position.Y:
                Player.PathFindTo(treeCoords.X,treeCoords.Y ,trees[ 0 ].z)
            prevPosX = Player.Position.X
            prevPosY = Player.Position.Y
            
    else:
    
    #Player.PathFindTo(treeCoords.X,treeCoords.Y,trees[ 0 ].z )
    #while sqrt( pow( ( treeCoords.X - Player.Position.X ), 2 ) + pow( ( treeCoords.Y - Player.Position.Y ), 2 ) )  >= 1:
    #    print(sqrt( pow( ( treeCoords.X - Player.Position.X ), 2 ) + pow( ( treeCoords.Y - Player.Position.Y ), 2 ) ))
    #    Player.PathFindTo(treeCoords.X,treeCoords.Y,trees[ 0 ].z )
    #    Misc.Pause(500)

        if PathFinding.Go( treeCoords ):
            Misc.SendMessage('First Try')
            Misc.Pause( 1000 )
        else:
            Misc.Resync()
            treeCoords.X = trees[ 0 ].x + 1
            treeCoords.Y = trees[ 0 ].y
            if PathFinding.Go( treeCoords ):
                Misc.SendMessage( 'Second Try' )
            else:
                treeCoords.X = trees[ 0 ].x - 1
                treeCoords.Y = trees[ 0 ].y
                if PathFinding.Go( treeCoords ):
                    Misc.SendMessage( 'Third Try' )
                else:
                    treeCoords.X = trees[ 0 ].x
                    treeCoords.Y = trees[ 0 ].y - 1
                    Misc.SendMessage( 'Final Try' )
                    if PathFinding.Go( treeCoords ):
                        Misc.NoOperation()
                    else:
                        return
                    

        Misc.Resync()

        while not RangeTree():
            CheckEnemy()
            Misc.Pause( 100 )
            pathlock = pathlock + 1
            if pathlock > 350:
                Misc.Resync()
                treeCoords = PathFinding.Route()
                treeCoords.MaxRetry = 5
                treeCoords.Run = False
                treeCoords.StopIfStuck = False
                treeCoords.X = trees[ 0 ].x
                treeCoords.Y = trees[ 0 ].y + 1
                
                if PathFinding.Go( treeCoords ):
                    #Misc.SendMessage('First Try')
                    Misc.Pause( 1000 )
                else:
                    treeCoords.X = trees[ 0 ].x + 1
                    treeCoords.Y = trees[ 0 ].y
                    if PathFinding.Go( treeCoords ):
                        Misc.SendMessage( 'Second Try' )
                    else:
                        treeCoords.X = trees[ 0 ].x - 1
                        treeCoords.Y = trees[ 0 ].y
                        if PathFinding.Go( treeCoords ):
                            Misc.SendMessage( 'Third Try' )
                        else:
                            treeCoords.X = trees[ 0 ].x
                            treeCoords.Y = trees[ 0 ].y - 1
                            Misc.SendMessage( 'Final Try' )
                            PathFinding.Go( treeCoords )

                pathlock = 0
                return

    Misc.SendMessage( '--> Reached TreeSpot: %i, %i' % ( trees[ 0 ].x, trees[ 0 ].y ), 77 )
    if silentMode == False:
        Player.ChatSay( 77, 'Podejdzcie!' )
        Misc.Pause(2000)
        Player.ChatSay( 77, 'Podejdzcie!' )
        Misc.Pause(2000)

def EquipAxe():
    global axeSerial
    if not leftHand:
        for item in Player.Backpack.Contains:
            if item.ItemID in axeList:
                Player.EquipItem( item.Serial )
                Misc.Pause( 600 )
                axeSerial = Player.GetItemOnLayer( 'LeftHand' ).Serial
    elif Player.GetItemOnLayer( 'LeftHand' ).ItemID in axeList:
        axeSerial = Player.GetItemOnLayer( 'LeftHand' ).Serial
    else:
        Player.HeadMessage( 35, 'You must have an axe to chop trees!' )
        Misc.Pause( 1000 )

def depositLogs():
    if dropLogs == True:
        MoveToGround()
    else:
        MoveToBeetle()

def CutTree():
    global runDrection
    global beetleGood
    global chopCounter
    global blockCount
    global trees
    global isMeranti
    chopCounter = 0
    hide()
    if Target.HasTarget():
        Misc.SendMessage( '--> Detected block, canceling target!', 77 )
        Target.Cancel()
        Misc.Pause( 500 )

        
    if Player.Weight >= 140 or Journal.Search( 'Nie masz miejsca w Twoim plecaku' ):
        depositLogs()
        Misc.SendMessage( '--> PRZESUWAMY rzeczy!', 77 )
    #if chopCounter >= 100:
     #   MoveToTree()

    if beetleGood == True and Journal.Search( 'Sapie' ):
        sapanie = Journal.GetLineText('Sapie',True)
        beetleGood = False
        sendDiscord("Uwaga zwierze zmeczone:\n" + sapanie, 15291726, lumberThumb);
        Misc.Pause(2000)
    Journal.Clear()
    Gumps.ResetGump()
    Items.UseItem( Player.GetItemOnLayer( 'LeftHand' ) )
    Target.WaitForTarget( TimeoutOnWaitAction , True )
    Target.TargetExecute( trees[ 0 ].x, trees[ 0 ].y, trees[ 0 ].z, trees[ 0 ].id )
    
    choppingTime = 8000
    if multiMode == False:
        choppingTime = 8000
    
    Misc.Pause(1200)
    gumpId = Gumps.CurrentGump()
    gData = Gumps.GetGumpData(gumpId)
    Timer.Create('choppingTimer',choppingTime)
    Misc.SendMessage( '--> GumpStarID: %i' % ( gumpId), 11 )
    enemeyMessage = False
    while ( Timer.Check('choppingTimer') == True ):
        if runDrection != "Dont":
            if enemeyMessage == False:
                enemy = Target.GetTargetFromList( 'enemywar' )
                if enemy != None:
                    enemeyMessage = True
                    sendDiscord("Uwaga wrog w popblizu!", 15291726, enemyThumb);
                    Player.ChatSay("STRAZE POMOCY BIJA MNIE")
                    Player.ChatSay("Za mna!")
                    Player.ChatSay("Za mna")
                    if isMeranti == True:
                        Timer.Create("runTimer",4000)
                    else:
                        Timer.Create("runTimer",7000)
                    while Timer.Check("runTimer") == True:
                        Player.Run(runDrection)
                    if Player.Name == "Vaekin":
                        Player.ChatSay("Golus strzez zwloki")
                    Misc.Pause(2000)
                    Player.ChatSay("STRAZE POMOCY BIJA MNIE!")
        if (Journal.Search( 'Zniszczyles klody' ) or
            Journal.Search( 'Sciales' ) or
            Journal.Search( 'Obciales' ) or
            Journal.Search( 'Nie masz miejsca w Twoim plecaku' ) or
            Journal.Search( 'martwego' ) or
            Journal.Search( 'Znalazles troche' ) or
            (multiMode == True and Journal.Search( 'To drzewo' )) or
            (multiMode == True and Journal.Search( 'Jesienia' )) or
            (multiMode == True and Journal.Search( 'Zima' ))):
                Journal.Clear()
                Timer.Create('choppingTimer',choppingTime)
                Misc.SendMessage( '--> Timer: %i' % ( chopCounter+1), 17 )
                chopCounter=chopCounter+1
                depositLogs()
                if multiMode == False:
                    CutTree()
        if (multiMode == False) and (Journal.Search( 'To drzewo' ) or Journal.Search( 'Jesienia' ) or Journal.Search( 'Zima' )):
            return
        Misc.Pause( 100 )
        
        if dropLogs == False and Journal.Search( 'Nie masz juz miejsca' ):
            Player.HeadMessage(33, 'BEETLE FULL STOPPING4')
            say('Halo Halo! Kon jest FULL')
            if Gumps.HasGump(gumpId):
                Gumps.SendAction(gumpId, 1)
            sendDiscord("Konie sa przepelnione", 15291726, lumberThumb);
            Misc.Pause(6000)
            sys.exit()
    Misc.Pause( 2000 )
    Misc.SendMessage( '--> Spaduwa', 77 )
    Misc.Pause( 100 )
def CheckEnemy():
    enemy = Target.GetTargetFromList( 'enemywar' )
    if enemy != None:
        Misc.ScriptRun( autoFightMacroName )
        while enemy != None:
            Timer.Create('Fight', 2500)
            Misc.Pause( 1000 )
            enemy = Mobiles.FindBySerial( enemy.Serial )
            if enemy:
                if Player.DistanceTo( enemy ) > 1:
                    enemyPosition = enemy.Position
                    enemyCoords = PathFinding.Route()
                    enemyCoords.MaxRetry = 5
                    enemyCoords.StopIfStuck = False
                    enemyCoords.X = enemyPosition.X
                    enemyCoords.Y = enemyPosition.Y - 1
                    PathFinding.Go( enemyCoords )
                
                    Misc.ScriptRun( autoFightMacroName )
                elif Timer.Check('Fight') == False:
                    Misc.ScriptRun( autoFightMacroName )
                    Timer.Create('Fight', 2500)
            enemy = Target.GetTargetFromList( 'enemywar' )

        corpseFilter = Items.Filter()
        corpseFilter.Movable = False
        corpseFilter.RangeMax = 2
        corpseFilter.Graphics = List[Int32]( [ 0x2006 ] )
        corpses = Items.ApplyFilter( corpseFilter )
        corpse = None

        Misc.Pause( dragDelay )

        for corpse in corpses:
            for item in corpse.Contains:
                if item.ItemID == logID:
                    Items.Move( item.Serial, Player.Backpack.Serial, 0 )
                    Misc.Pause( dragDelay )
                    
        PathFinding.Go( treeCoords )


def GetNumberOfBoardsInBeetle():
    global beetle
    global boardID
    global dragDelay

    remount = False
    if not Mobiles.FindBySerial( beetle ):
        remount = True
        Mobiles.UseMobile( Player.Serial )
        Misc.Pause( dragDelay )

    numberOfBoards = 0
    for item in Mobiles.FindBySerial( beetle ).Backpack.Contains:
        if item.ItemID == boardID:
            numberOfBoards += item.Amount

    if remount:
        Mobiles.UseItem( beetle )
        Misc.Pause( dragDelay )

    return numberOfBoards


def GetNumberOfLogsInBeetle():
    global beetle
    global logID
    global dragDelay

    remount = False
    if not Mobiles.FindBySerial( beetle ):
        remount = True
        Mobiles.UseMobile( Player.Serial )
        Misc.Pause( dragDelay )

    numberOfBoards = 0
    beetleObject = Mobiles.FindBySerial( beetle )
    if beetleObject is not None:
        for item in beetleObject.Backpack.Contains:
            if item.ItemID == boardID:
                numberOfBoards += item.Amount
    else:
        sendDiscord("Cos sie popuslo - kon zaginal", 15291726, lumberThumb);
        Misc.Pause(6000)
        sys.exit()

    if remount:
        Mobiles.UseItem( beetle )
        Misc.Pause( dragDelay )

    return numberOfBoards

def filterItem(id,range=2, movable=True):
    fil = Items.Filter()
    fil.Movable = movable
    fil.RangeMax = range
    fil.Graphics = List[Int32](id)
    list = Items.ApplyFilter(fil)

    return list
def MoveToGround():
    for item in Player.Backpack.Contains:
        if item.ItemID == logID:
            Items.DropItemGroundSelf(item,0)
            Misc.Pause( dragDelay )
    

def MoveToBeetle():
    if Mobiles.FindBySerial( beetle ) is None:
        sendDiscord("Cos sie popuslo - kon zaginal", 15291726, lumberThumb);
        Misc.Pause(2000)
        sys.exit()
    
    fullCheck()
    
    if Player.Mount:
        Mobiles.UseMobile( Player.Serial )
        Misc.Pause( dragDelay )
    for item in Player.Backpack.Contains:
        if item.ItemID == logID:
            Items.Move( item, beetle, 0 )
            Misc.Pause( dragDelay )

    fullCheck()

    if not Player.Mount:
        Mobiles.UseMobile( beetle )
        Misc.Pause( dragDelay )
        
toonFilter = Mobiles.Filter()
toonFilter.Enabled = True
toonFilter.RangeMin = -1
toonFilter.RangeMax = -1
toonFilter.IsHuman = True 
toonFilter.Friend = False
toonFilter.Notorieties = List[Byte](bytes([1,2,3,4,5,6,7]))

invulFilter = Mobiles.Filter()
invulFilter.Enabled = True
invulFilter.RangeMin = -1
invulFilter.RangeMax = -1
invulFilter.Friend = False
invulFilter.Notorieties = List[Byte](bytes([7]))
def say(text):
    spk = SpeechSynthesizer()
    spk.Speak(text)
def fullCheck():
    global beetle
    global newBeetle
    if dropLogs == False and (Journal.Search( 'zwierze nie moze') or Journal.Search( 'too heavy')):
        if beetle == newBeetle:
            Player.HeadMessage(33, 'BEETLE FULL STOPPING2')
            say('Halo Halo! Kon jest FULL')
            sendDiscord("Przepelnienie koni trzeba je oproznic", 15291726, lumberThumb);
            Misc.Pause(6000)
            sys.exit()
        else:
            say('Ej! zmiana koni')
            beetle = newBeetle
        
def safteyNet():
    if alert:
        toon = Mobiles.ApplyFilter(toonFilter)
        invul = Mobiles.ApplyFilter(invulFilter)
        if toon:
            Misc.FocusUOWindow()
            say("Hey, someone is here. You should tab over and take a look")
            toonName = Mobiles.Select(toon, 'Nearest')
            if toonName:
                Misc.SendMessage('Toon Near: ' + toonName.Name, 33)
        elif invul:
            say("Hey, something invulnerable here. You should tab over and take a look")
            invulName = Mobiles.Select(invul, 'Nearest')
            if invulName:
                Misc.SendMessage('Uh Oh: Invul! Who the fuck is ' + invul.Name, 33)
        else:
            Misc.NoOperation()
##Friend.ChangeList('lj')
Misc.SendMessage('--> Start up Woods', 77)

Timer.Create('eatingLogTimer', 120000)
EquipAxe()
while onLoop:
    #RecallNextSpot()
    if Player.IsGhost == True:
        say('Uwaga ! Cos sie stalo ze sie zesralo!')
        sendDiscord("Postac umarla!", 15291726, deadThumb);
        Misc.Pause(3000)
        sys.exit()
    Misc.SendMessage('--> Starting Round', 87)
    ScanStatic()
    i = 0
    while trees.Count > 0 and Player.IsGhost == False :
        safteyNet()
        MoveToTree()
        CutTree()
        trees.pop( 0 )
        trees = sorted( trees, key = lambda tree: sqrt( pow( ( tree.x - Player.Position.X ), 2 ) + pow( ( tree.y - Player.Position.Y ), 2 ) ) )
    trees = []
    Misc.Pause( 100 )