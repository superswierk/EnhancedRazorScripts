# OG from AbelGoodwin https://github.com/hampgoodwin/razorenhancedscripts
# Modified by Matsamilla
#
# Last updated: 12/2/21

from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys
Round = lambda x, n: eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n)))
lumberThumb = "https://i.imgur.com/FAb0xg0.png"
farmThumb = "https://i.imgur.com/vhfYDCW.png"
deadThumb = "https://i.imgur.com/QjVeOoA.png"
foodThumb = "https://i.imgur.com/uB0tTVj.png"
enemyThumb = "https://i.imgur.com/YvbQw56.png"
lvlupThumb = "https://i.imgur.com/j5rUy80.png"

   
singleMode = True
silentMode = True
dropLogs = True
scanRadius = 30
#********************
# serial of your beetle, logs go here when full
if dropLogs == False: 
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


# Trees where there is no longer enough wood to be harvested will not be revisited until this much time has passed
treeCooldown = 12000000 # 1,200,000 ms is 20 minutes

# Want this script to alert you for humaniods?
alert = False
#********************

chopCounter=0

# Parameters
#0x0C76 marchew
#0x0C7D kukurdza
#0x0C9B pomidor
#0x1A9B len 0x1A99
#0x0D1E winogrono
#0x0D04 kapusta
#0x1B22 salata 0x0C93
#0x0C61 rzepa
#0x0C6F cebula
#0x0C69 sprouts
#0x0C6C dynia
#0x0C5D adbuz
#0x0C4F bawelna 0x0C50
#0x0D04 kapusta
#0x0C55 pszenica 0x1A93
#0x0D98 jablon
treeStaticIDs = [ 0x1A93, 0x0C7D ]
useItemID = None
isColliding = False
    
#axeSerial = None
EquipAxeDelay = 1000
TimeoutOnWaitAction = 4000
ChopDelay = 1000
dragDelay = 700
hideDelay = 300
#przenica 0x1A93
#log 0x1BDD
#kukurydza 0x0C7F
#pomidor 0x0C6C
#len 0x1A9D
#grono 0x09D1
#bawelna 0x0DF9
#cebula 0x0C6D
#marchew 0x0C78
vegTable = [  0x1EBF, 0x0C7F ]
logID = 0x0C7F
boardID = 0x1BD7
weightLimit = Player.MaxWeight - 10
bankX = 2051
bankY = 1343
axeList = [ 0x26BB ]
rightHand = Player.CheckLayer( 'RightHand' )
leftHand = Player.CheckLayer( 'LeftHand' )


# System Variables
from System.Collections.Generic import List
from System import Byte, Int32
from math import sqrt
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
    pathlock = 0
    if silentMode == False:
        Player.ChatSay( 77, 'Wszyscy za mna' )
    Misc.SendMessage( '--> Moving to TreeSpot: %i, %i' % ( trees[ 0 ].x, trees[ 0 ].y ), 77 )
    Misc.Resync()
    treeCoords = PathFinding.Route()
    treeCoords.MaxRetry = 5
    treeCoords.StopIfStuck = False
    treeCoords.X = trees[ 0 ].x
    if isColliding:
        treeCoords.Y = trees[ 0 ].y + 1
    else:
        treeCoords.Y = trees[ 0 ].y
    #Items.Message(trees[0], 1, "Here")
    
    
    if PathFinding.Go( treeCoords ):
        #Misc.SendMessage('First Try')
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
        Misc.Pause( 100 )
        pathlock = pathlock + 1
        if pathlock > 350:
            Misc.Resync()
            treeCoords = PathFinding.Route()
            treeCoords.MaxRetry = 5
            treeCoords.StopIfStuck = False
            treeCoords.X = trees[ 0 ].x
            if isColliding:
                treeCoords.Y = trees[ 0 ].y + 1
            else:
                treeCoords.Y = trees[ 0 ].y
            
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


def EquipAxe():
    global axeSerial

    if not rightHand:
        for item in Player.Backpack.Contains:
            if item.ItemID in axeList:
                Player.EquipItem( item.Serial )
                Misc.Pause( 600 )
                axeSerial = Player.GetItemOnLayer( 'RightHand' ).Serial
    elif Player.GetItemOnLayer( 'RightHand' ).ItemID in axeList:
        axeSerial = Player.GetItemOnLayer( 'RightHand' ).Serial
    else:
        Player.HeadMessage( 35, 'You must have an axe to chop trees!' )
        Misc.Pause( 1000 )

def depositLogs():
    if dropLogs == True:
        Misc.Pause(100)
        MoveToGround()
    else:
        MoveToBeetle()

def CutTree():
    global chopCounter
    global blockCount
    global trees
    chopCounter = 0
    hide()
    if Target.HasTarget():
        Misc.SendMessage( '--> Detected block, canceling target!', 77 )
        Target.Cancel()
        Misc.Pause( 500 )
        

    depositLogs()
        
    if Player.Weight >= weightLimit or Journal.Search( 'Nie masz miejsca w Twoim plecaku' ):
        depositLogs()
        Misc.SendMessage( '--> Przeciazenie!', 77 )
        sendDiscord("Jestes full", 15291726, farmThumb);
        Misc.Pause(6000)
        sys.exit()
    
    
    Journal.Clear()
    Gumps.ResetGump()
    Items.UseItem( Player.GetItemOnLayer( 'RightHand' ) )
    Target.WaitForTarget( TimeoutOnWaitAction , True )
    if useItemID == None:
        Target.TargetExecute( trees[ 0 ].x, trees[ 0 ].y, trees[ 0 ].z, trees[ 0 ].id )
    else:
        Target.TargetExecute( trees[ 0 ].x, trees[ 0 ].y, trees[ 0 ].z, useItemID )
    if silentMode == False:
        Player.ChatSay( 77, 'Podejdzcie' )
    choppingTime = 8000
    if singleMode == True:
        choppingTime = 8000
    
    Misc.Pause(1200)
    gumpId = Gumps.CurrentGump()
    gData = Gumps.GetGumpData(gumpId)
    Timer.Create('choppingTimer',choppingTime)
    while ( Timer.Check('choppingTimer') == True ):
        Misc.Pause(400)
        if (Journal.Search( 'Nie udalo Ci sie' ) or 
            Journal.Search( 'Udalo Ci sie' )or 
            Journal.Search( 'Nie masz miejsca w Twoim plecaku' )or 
            Journal.Search( 'martwego' ) or 
            Journal.Search( 'Znalazles troche' ) or 
            (singleMode == False and Journal.Search( 'Z tej rosliny' )) or 
            (singleMode == False and Journal.Search( 'Jesienia' ))):
                Journal.Clear()
                Timer.Create('choppingTimer',choppingTime)
                chopCounter=chopCounter+1
                depositLogs()
                if singleMode == True:
                    CutTree()
        if singleMode == True and (Journal.Search( 'Z tej rosliny' ) or Journal.Search( 'Jesienia' )):
            return
        Misc.Pause( 100 )
        
        if dropLogs == False and Journal.Search( 'Nie masz juz miejsca' ):
            Player.HeadMessage(33, 'BEETLE FULL STOPPING')
            if Gumps.HasGump(gumpId):
                Gumps.SendAction(gumpId, 1)
            sendDiscord("Konie sa przepelnione", 15291726, farmThumb);
            Misc.Pause(6000)
            sys.exit()
    Misc.Pause( 2000 )
    Misc.SendMessage( '--> Spaduwa', 77 )
    Misc.Pause( 100 )


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
    for item in Mobiles.FindBySerial( beetle ).Backpack.Contains:
        if item.ItemID == boardID:
            numberOfBoards += item.Amount

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
        for vegID in vegTable:
            if item.ItemID == vegID:
                Items.DropItemGroundSelf(item,0)
                Misc.Pause( dragDelay )
    

def MoveToBeetle():
    fullCheck()

    if Player.Mount:
        Mobiles.UseMobile( Player.Serial )
        Misc.Pause( dragDelay )

    # Move boards to beetle, if they will fit in the beetle
    for item in Player.Backpack.Contains:
        if  item.ItemID == logID:
            numberOfBoardsInBeetle = GetNumberOfLogsInBeetle()
            if numberOfBoardsInBeetle + item.Amount < 1900:
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

def fullCheck():
    global beetle
    global newBeetle
    if dropLogs == False and (Journal.Search( 'zwierze nie moze') or Journal.Search( 'too heavy')):
        if beetle == newBeetle:
            Player.HeadMessage(33, 'BEETLE FULL STOPPING')
            sendDiscord("Konie sa przepelnione", 15291726, farmThumb);
            Misc.Pause(6000)
            sys.exit()
        else:
            beetle = newBeetle

##Friend.ChangeList('lj')
Misc.SendMessage('--> Start up Farming', 77)
EquipAxe()
while onLoop:
    #RecallNextSpot()
    if Player.IsGhost == True:
        print("UMARLES")
        Misc.Pause(2000)
        sys.exit() 
    Misc.SendMessage('--> Starting Round', 87)
    ScanStatic()
    i = 0
    while trees.Count > 0 and Player.IsGhost == False :
        MoveToTree()
        CutTree()
        trees.pop( 0 )
        trees = sorted( trees, key = lambda tree: sqrt( pow( ( tree.x - Player.Position.X ), 2 ) + pow( ( tree.y - Player.Position.Y ), 2 ) ) )
    trees = []
    Misc.Pause( 200 )