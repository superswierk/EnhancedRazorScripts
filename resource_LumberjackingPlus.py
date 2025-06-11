# OG from AbelGoodwin https://github.com/hampgoodwin/razorenhancedscripts
# Modified by Matsamilla
#
# Last updated: 12/2/21

from Scripts.EnhancedRazorScripts.misc_Discord import *
from Scripts.EnhancedRazorScripts.misc_Email import *
import sys
Round = lambda x, n: eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n)))

lumberThumb = "https://i.imgur.com/FAb0xg0.png"
deadThumb = "https://i.imgur.com/QjVeOoA.png"
foodThumb = "https://i.imgur.com/uB0tTVj.png"
enemyThumb = "https://i.imgur.com/YvbQw56.png"
lvlupThumb = "https://i.imgur.com/j5rUy80.png"

# you want boards or logs?
logsToBoards = False

singleMode = True
silentMode = False
dropLogs = False
scanRadius = 40

lvlCarpSkill = Player.GetRealSkillValue('Drwalstwo')
#********************
# serial of your beetle, logs go here when full
if dropLogs == False and logsToBoards == False:
    beetle = Target.PromptTarget( 'Wybierz konia beetle' )
    Player.ChatSay( 77, '.pojemnik' )
    Target.WaitForTarget( 5000 , True )
    Target.TargetExecute(beetle)

    newBeetle = Target.PromptTarget( 'Wybierz konia newBeetle' )
    Player.ChatSay( 77, '.pojemnik' )
    Target.WaitForTarget( 5000 , True )
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
#treeStaticIDs = [ 0x0C95, 0x0C96, 0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0CA6,
#    0x0CA8, 0x0CAA, 0x0CAB, 0x0CC3, 0x0CC4, 0x0CC8, 0x0CCA, 0x0CCB,
#    0x0CCC, 0x0CCD, 0x0CD0, 0x0CD3, 0x0CD6, 0x0CD8, 0x0CDA, 0x0CDD, 0x0CE0,
#    0x0CE3, 0x0CE6, 0x0CF8, 0x0CFB, 0x0CFE, 0x0D01, 0x0D25, 0x0D27, 0x0D35,
#    0x0D37, 0x0D38, 0x0D42, 0x0D43, 0x0D59, 0x0D70, 0x0D85, 0x0D94, 0x0D96,
#    0x0D98, 0x0D9A, 0x0DA0, 0x0DA2, 0x0DA8, 0x12B9,
#    0x0C9E, ]
#treeStaticIDs = [ 0x0CCD, 0x0CD0, 0x0CD3]zwykle
#treeStaticIDs = [ 0x0CD6,] cedr
#cis 0x12B9
#cyprys 0x0D01 0x0CFE treeStaticIDs = [ 0x0D01, 0x0CFE ]
# Parameters wszystkie bez zwyklych
#treeStaticIDs = [ 0x0C95, 0x0C96, 0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0CA6,
#    0x0CA8, 0x0CAA, 0x0CAB, 0x0CC3, 0x0CC4, 0x0CC8, 0x0CCA, 0x0CCB,
#    0x0CCC, 0x0CD6, 0x0CD8, 0x0CDA, 0x0CDD, 0x0CE0,
#    0x0CE3, 0x0CE6, 0x0CF8, 0x0CFB, 0x0CFE, 0x0D01, 0x0D25, 0x0D27, 0x0D35,
#    0x0D37, 0x0D38, 0x0D42, 0x0D43, 0x0D59, 0x0D70, 0x0D85, 0x0D94, 0x0D96,
#    0x0D98, 0x0D9A, 0x0DA0, 0x0DA2, 0x0DA8, 0x12B9,
#    0x0C9E, ]
# dab 0x0CDD
#treeStaticIDs = [ 0x0CCD, 0x0CD0, 0x0CD3]

treeStaticIDs = [ 0x0C95, 0x0C96, 0x0C99, 0x0C9B, 0x0C9C, 0x0C9D, 0x0CA6,
    0x0CA8, 0x0CAA, 0x0CAB, 0x0CC4, 0x0CC8, 0x0CCA, 0x0CCB,
    0x0CCC, 0x0CCD, 0x0CD0, 0x0CD3, 0x0CD6, 0x0CD8, 0x0CDA, 0x0CDD, 0x0CE0,
    0x0CE3, 0x0CE6, 0x0CF8, 0x0CFB, 0x0CFE, 0x0D01, 0x0D25, 0x0D27, 0x0D35,
    0x0D37, 0x0D38, 0x0D42, 0x0D43, 0x0D59, 0x0D70, 0x0D85, 0x0D94, 0x0D96,
    0x0D98, 0x0D9A, 0x0DA0, 0x0DA2, 0x0DA8, 0x12B9,
    0x0C9E, ]

#treeStaticIDs = [ 0x0CE6 ] #wierzby
#treeStaticIDs = [ 0x0CD6, 0x0CD8 ]
#axeSerial = None
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
from System.Collections.Generic import List
from System import Byte, Int32
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

glod = ""
bialka = ""
witaminy = ""
weglowodany = ""

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
    global beetleGood
    global chopCounter
    global blockCount
    global trees
    global glod
    global bialka
    global witaminy
    global weglowodany
    global lvlCarpSkill
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
    if singleMode == True:
        choppingTime = 8000
    
    Misc.Pause(1200)
    gumpId = Gumps.CurrentGump()
    gData = Gumps.GetGumpData(gumpId)
    Timer.Create('choppingTimer',choppingTime)
    Misc.SendMessage( '--> GumpStarID: %i' % ( gumpId), 11 )
    enemeyMessage = False
    while ( Timer.Check('choppingTimer') == True ):
        if enemeyMessage == False:
            enemy = Target.GetTargetFromList( 'enemywar' )
            if enemy != None:
                enemeyMessage = True
                sendDiscord("Uwaga wrog w popblizu!", 15291726, enemyThumb);
                Player.ChatSay("STRAZE POMOCY BIJA MNIE")
                Player.ChatSay("Za mna!")
                Player.ChatSay("Za mna")
                Timer.Create("runTimer",12000)
                while Timer.Check("runTimer") == True:
                    Player.Run('Right')
                Misc.Pause(2000)
                Player.ChatSay("STRAZE POMOCY BIJA MNIE!")
        lvlCarpSkillNew = Player.GetRealSkillValue('Drwalstwo')
        if lvlCarpSkill != lvlCarpSkillNew:
            lvlCarpSkill = lvlCarpSkillNew
            sendDiscord("Wzrost umiejetnosci Drwalstwo masz teraz: " + str(Round(lvlCarpSkill,1)), 5814783, lvlupThumb)
        if(Timer.Check('eatingLogTimer') == False):
            Timer.Create('eatingLogTimer', 120000)
            Player.ChatSay('.glod wszystko')
            Misc.Pause(1000)
            newGlod = Journal.GetLineText('Glod')
            newBialka = Journal.GetLineText('Bialka')
            newWitaminy = Journal.GetLineText('Witaminy')
            newWeglowodany = Journal.GetLineText('Weglowodany')
            if newGlod != glod or newBialka != bialka or newWitaminy != witaminy or newWeglowodany != weglowodany :
                glod = newGlod
                bialka = newBialka
                witaminy = newWitaminy
                weglowodany = newWeglowodany
                sendDiscord("Status glodu:\n" + glod + "\n" + bialka + "\n" + witaminy + "\n" + weglowodany + "\n",2012169, foodThumb)
        if (Journal.Search( 'Zniszczyles klody' ) or
            Journal.Search( 'Sciales' ) or
            Journal.Search( 'Obciales' ) or
            Journal.Search( 'Nie masz miejsca w Twoim plecaku' ) or
            Journal.Search( 'martwego' ) or
            Journal.Search( 'Znalazles troche' ) or
            (singleMode == False and Journal.Search( 'To drzewo' )) or
            (singleMode == False and Journal.Search( 'Jesienia' )) or
            (singleMode == False and Journal.Search( 'Zima' ))):
                Journal.Clear()
                Timer.Create('choppingTimer',choppingTime)
                Misc.SendMessage( '--> Timer: %i' % ( chopCounter+1), 17 )
                chopCounter=chopCounter+1
                depositLogs()
                if singleMode == True:
                    CutTree()
        if singleMode == True and (Journal.Search( 'To drzewo' ) or Journal.Search( 'Jesienia' ) or Journal.Search( 'Zima' )):
            return
        Misc.Pause( 100 )
        
        if dropLogs == False and Journal.Search( 'Nie masz juz miejsca' ):
            Player.HeadMessage(33, 'BEETLE FULL STOPPING')
            say('Halo Halo! Kon jest FULL')
            if Gumps.HasGump(gumpId):
                Gumps.SendAction(gumpId, 1)
            sendDiscord("Konie sa przepelnione", 15291726, lumberThumb);
            Misc.Pause(6000)
            #sendEmailMessage("Halo kon chyba full", "Przemienili kampon")
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
        #sendEmailMessage("Cos sie popuslo", "Nie znalazlem konia")
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
    if logsToBoards == False:
        fullCheck()
    # Chop logs into boards
    if logsToBoards:
        saw = getByItemID(sawId, Player.Backpack.Serial)
        for item in Player.Backpack.Contains:
            if item.ItemID == logID:
                Items.UseItem(saw)
                Target.WaitForTarget(2000, True)
                Target.TargetExecute(item)
                Misc.Pause( dragDelay )
    if logsToBoards == False:
        if Player.Mount:
            Mobiles.UseMobile( Player.Serial )
            Misc.Pause( dragDelay )

    # Move boards to beetle, if they will fit in the beetle
    if logsToBoards == False:
        for item in Player.Backpack.Contains:
            if logsToBoards and item.ItemID == boardID:
                numberOfBoardsInBeetle = GetNumberOfBoardsInBeetle()
                if numberOfBoardsInBeetle + i.Amount < 1900:
                    Items.Move( i, beetle, 0 )
                    Misc.Pause( dragDelay )
            elif not logsToBoards and item.ItemID == logID:
                numberOfBoardsInBeetle = GetNumberOfLogsInBeetle()
                if numberOfBoardsInBeetle + item.Amount < 1900:
                    Items.Move( item, beetle, 0 )
                    Misc.Pause( dragDelay )
        groundItems = filterItem([boardID,logID])
        fullCheck()
        if groundItems:
            Player.HeadMessage(33, 'BEETLE FULL STOPPING')
            say('Halo 2 Halo 2! Kon jest pelny az sie przelewa')
            sendDiscord("Najwyrazniej konie sa pelne", 15291726, lumberThumb);
            Misc.Pause(6000)
            #sendEmailMessage("Halo kon wzywa", "Kon jest pelny az sie przelewa")
            sys.exit()

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
            Player.HeadMessage(33, 'BEETLE FULL STOPPING')
            say('Halo Halo! Kon jest FULL')
            sendDiscord("Przepelnienie koni trzeba je oproznic", 15291726, lumberThumb);
            Misc.Pause(6000)
            #sendEmailMessage("Hej konie pelne", "Przepelnienie koni trzeba je oproznic")
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

Player.ChatSay('.glod wszystko')
Misc.Pause(1000)
glod = Journal.GetLineText('Glod')
bialka = Journal.GetLineText('Bialka')
witaminy = Journal.GetLineText('Witaminy')
weglowodany = Journal.GetLineText('Weglowodany')
Timer.Create('eatingLogTimer', 120000)
EquipAxe()
while onLoop:
    #RecallNextSpot()
    if Player.IsGhost == True:
        say('Uwaga ! Cos sie stalo ze sie zesralo!')
        sendDiscord("Postac umarla!", 15291726, deadThumb);
        Misc.Pause(6000)
        sendEmailMessage("Halo postac padla", "Cos sie stalo umarles")
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