import sys
from System.Collections.Generic import List
from System import Byte, Int32
from math import sqrt
import clr
clr.AddReference('System.Speech')
from System.Speech.Synthesis import SpeechSynthesizer
from Scripts.EnhancedRazorScripts.misc_Discord import *

Round = lambda x, n: eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n)))
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

trees = []
treeCoords = None


if silentMode == False:
    beetle = Target.PromptTarget( 'Wybierz konia beetle' )
    Player.ChatSay( 77, '.pojemnik' )
    Target.WaitForTarget( 5000 , True )
    Target.TargetExecute(beetle)

    newBeetle = Target.PromptTarget( 'Wybierz konia newBeetle' )
    Player.ChatSay( 77, '.pojemnik' )
    Target.WaitForTarget( 5000 , True )
    Target.TargetExecute(newBeetle)

class Tree:
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
        
        
def SetDigSpots():
    global trees
    trees = []
    trees.Add( Tree( 804, 932 ))
    trees.Add( Tree( 807, 923 ))
    trees.Add( Tree( 813, 916 ))
    trees.Add( Tree( 820, 906 ))
    trees.Add( Tree( 824, 902 ))
    trees.Add( Tree( 828, 904 ))
    trees.Add( Tree( 825, 910 ))
    trees.Add( Tree( 815, 920 ))
    trees.Add( Tree( 819, 924 ))
    trees.Add( Tree( 810, 927 ))
    trees.Add( Tree( 803, 919 ))
    trees.Add( Tree( 796, 920 ))
    trees.Add( Tree( 792, 914 ))
    trees.Add( Tree( 797, 912 ))
    trees.Add( Tree( 795, 915 ))
    trees.Add( Tree( 803, 920 ))
    trees.Add( Tree( 810, 927 ))
    #trees = sorted( trees, key = lambda tree: sqrt( pow( ( tree.x - Player.Position.X ), 2 ) + pow( ( tree.y - Player.Position.Y ), 2 ) ) )


    
def MoveToTree():
    global trees
    print("ide do drzew")
    print(trees.Count)
    print(trees[0].x)
    if silentMode == False:
        Player.ChatSay( 77, 'Za mna!' )
        Misc.Pause(2000)
        Player.ChatSay( 77, 'za mna' )
        Misc.Pause(2000)
    Player.PathFindTo(trees[0].x,trees[0].y,-30)
    Misc.Pause(14000)
    Misc.SendMessage( '--> Reached DigSpot: %i, %i' % ( trees[ 0 ].x, trees[ 0 ].y ), 77 )
    trees.pop( 0 )
    if silentMode == False:
        Player.ChatSay( 77, 'Podejdzcie!' )
        Misc.Pause(2000)
        Player.ChatSay( 77, 'Podejdzcie!' )
        Misc.Pause(2000)
    if trees.Count == 0:
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
        Player.HeadMessage( 1100, 'You\'re out of pickaxes!' )
        return
    Items.UseItem( pickaxe )
    Target.WaitForTarget( 2000, True )
    Target.TargetExecuteRelative( Player.Serial, 1 )      

SetDigSpots()
# Start mining
Misc.SendMessage( 'Start', 90 )
MoveToGround()
MoveToTree()
lvlCarpSkill = Round(Player.GetRealSkillValue('Gornictwo'),1)
Player.ChatSay('.glod wszystko')
Misc.Pause(1000)
glod = Journal.GetLineText('Glod')
bialka = Journal.GetLineText('Bialka')
witaminy = Journal.GetLineText('Witaminy')
weglowodany = Journal.GetLineText('Weglowodany')
Timer.Create('eatingLogTimer', 120000)
Timer.Create('digTimer',8200)
print("poczatek pracy")
guards = False
Journal.Clear()
doMine()
while True:
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
    lvlCarpSkillNew = Round(Player.GetRealSkillValue('Gornictwo'),1)
    if lvlCarpSkill != lvlCarpSkillNew:
        lvlCarpSkill = lvlCarpSkillNew
        sendDiscord("Wzrost umiejetnosci Gornictwo masz teraz: " + str(lvlCarpSkill), 5814783, lvlupThumb)
        Misc.Pause(1000)
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
        MoveToTree()
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        Misc.Pause(1000)
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        

    if Timer.Check('digTimer') == False:
        if guards == True:
            guards = False
        else:
            MoveToTree()
        print("koniec digTimer")
        Timer.Create('digTimer',8200)
        doMine()
    if Journal.Search('Nie masz miejsca'):
        sendDiscord("Nie masz juz miejsca na rude", 15291726, miningThumb);
        Misc.Pause(2000)
        sys.exit()

    if Journal.Search('Wykopales') or Journal.Search('Nie udalo Ci sie') or Journal.Search('W tym miejscu'):
        Journal.Clear('Wykopales')
        Journal.Clear('Nie udalo Ci sie')
        Journal.Clear('W tym miejscu')
        MoveToGround()
        Timer.Create('digTimer',8200)
    if Journal.Search('Trzasnales'):
        Journal.Clear('Trzasnales')
        MoveToGround()
        Misc.Pause(20000)
        Timer.Create('digTimer',8200)
        #print("trzasnales kontynuuj")
        #doMine()
    Misc.Pause(200)


