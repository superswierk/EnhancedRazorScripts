import sys
from System.Collections.Generic import List
from System import Byte, Int32
from math import sqrt
import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer
from Scripts.EnhancedRazorScripts.misc_Discord import *

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

spots = []

if silentMode == False:
    beetle = Target.PromptTarget( 'Wybierz konia beetle' )
    Player.ChatSay( 77, '.pojemnik' )
    Target.WaitForTarget( 5000 , True )
    Target.TargetExecute(beetle)

    newBeetle = Target.PromptTarget( 'Wybierz konia newBeetle' )
    Player.ChatSay( 77, '.pojemnik' )
    Target.WaitForTarget( 5000 , True )
    Target.TargetExecute(newBeetle)

class Spot:
    x = None
    y = None
    
    def __init__ ( self, x, y):
        self.x = x
        self.y = y

def hide():
    if  Player.BuffsExist('Ukrywanie') == False and Timer.Check('hideTimer') == False:
        Misc.Pause( 700 )
        Player.UseSkill('Ukrywanie')
        Timer.Create('hideTimer',10000)
        Misc.Pause( 1000 )
        
        
def SetDigSpotsMistas():
    global spots
    spots = []
    spots.Add( Spot( 804, 932 ))
    spots.Add( Spot( 807, 923 ))
    spots.Add( Spot( 813, 916 ))
    spots.Add( Spot( 820, 906 ))
    spots.Add( Spot( 824, 902 ))
    spots.Add( Spot( 828, 904 ))
    spots.Add( Spot( 825, 910 ))
    spots.Add( Spot( 815, 920 ))
    spots.Add( Spot( 819, 924 ))
    spots.Add( Spot( 810, 927 ))
    spots.Add( Spot( 803, 919 ))
    spots.Add( Spot( 796, 920 ))
    spots.Add( Spot( 792, 914 ))
    spots.Add( Spot( 797, 912 ))
    spots.Add( Spot( 795, 915 ))
    spots.Add( Spot( 803, 920 ))
    spots.Add( Spot( 810, 927 ))

    
def SetDigSpots():
    global spots
    spots = []
    spots.Add( Spot( 4738, 144 ))
    spots.Add( Spot( 4739, 150 ))
    spots.Add( Spot( 4737, 155 ))
    spots.Add( Spot( 4736, 160 ))
    spots.Add( Spot( 4735, 167 ))
    spots.Add( Spot( 4741, 169 ))
    spots.Add( Spot( 4732, 172 ))
    spots.Add( Spot( 4735, 175 ))
    spots.Add( Spot( 4739, 171 ))
    spots.Add( Spot( 4740, 166 ))
    spots.Add( Spot( 4743, 163 ))
    spots.Add( Spot( 4742, 158 ))
    spots.Add( Spot( 4742, 143 ))
    spots.Add( Spot( 4742, 147 ))
    spots.Add( Spot( 4740, 142 ))


    
def MoveToSpot():
    global spots
    print("Move To Spot")
    if silentMode == False:
        Player.ChatSay( 77, 'Za mna!' )
        Misc.Pause(2000)
        Player.ChatSay( 77, 'za mna' )
        Misc.Pause(2000)
    Player.PathFindTo(spots[0].x,spots[0].y,-30)
    Misc.Pause(14000)
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
    if Journal.Search("Przyciagnales uwage",) or Journal.Search("podchodzi zobaczyc co ciekawego ") or Journal.Search("wir"):
        guards = True
        Misc.Pause(1000)
        Journal.Clear()
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        sendDiscord("Jakas potwora sie pojawila", 15291726, enemyThumb);
        Misc.Pause(200)
        MoveToSpot()
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        Misc.Pause(1000)
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        

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


