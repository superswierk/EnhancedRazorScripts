from Scripts.EnhancedRazorScripts.misc_Discord import *
from System.Collections.Generic import List
from System import Byte, Int32, Double
import sys
import time

Timer.Create( 'lockTimer', 1 )
lockTimerMs = 10200

lockPicksId = 0x14FB
keyChainSerial = 0x547EEEEA

crates = []

class Crate:
    serialId = None
    def __init__ ( self, serialId):
        self.serialId = serialId

# Helper Functions
###################################

def currentTime():
    return Double(time.time() + Double(7200))

def isInJournal(text, secondsAgo):
    jList = Journal.GetJournalEntry( currentTime() - secondsAgo )
    for element in jList:
        if (element.Text.find(text) != -1):
            return True
    return False


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

def waitForTimer(name):
    while Timer.Check(name) == True:
        Misc.Pause(400)        
###################################


workingBag = Target.PromptTarget( 'wybierz kontener do pracy' )



def SetCrates():
    global crates
    crates = []
    crates.Add( Crate( 0x54A6DE69 ))
    crates.Add( Crate( 0x54FEE694 ))
    crates.Add( Crate( 0x54FEE6B0 ))
    crates.Add( Crate( 0x54FEE68F ))

def CloseCrate():
    global crates
    
    if isInJournal("Zapis Stanu",40) == True:
        while isInJournal("Koniec zapisywania",40) == False:
            Misc.Pause(1000)
            print("Czekam na zapis swiata...");
    
    Items.UseItem(keyChainSerial)
    Target.WaitForTarget(2000, False)
    Target.TargetExecute(crates[0].serialId)
    Misc.Pause(1000)
    crates.pop( 0 )
    
    
def OpenCrate():
    global crates
    
    if isInJournal("Zapis Stanu",40) == True:
        while isInJournal("Koniec zapisywania",40) == False:
            Misc.Pause(1000)
            print("Czekam na zapis swiata...");
    
    
    print("jestem tutaj 1")
    workingLockpicks = getByItemID(lockPicksId, workingBag)
    print("jestem tutaj 2")
    Journal.Clear('Nie udalo Ci sie otworzyc')
    Journal.Clear('Juz cos robisz')
    Journal.Clear('Udalo sie otworzyc')
    if workingLockpicks is not None:
        print("jestem tutaj 33")
        Items.UseItem(workingLockpicks)
        Target.WaitForTarget(2000, False)
        print("jestem tutaj 44")
        Target.TargetExecute(crates[0].serialId)
        Timer.Create('lockTimer',lockTimerMs)
    else:
        Misc.SendMessage('Brak wytrychow!', 77)
        sys.exit()
        return False
    print("a teraz tutaj tutaj")
    while True:
        Misc.Pause(200)
        if Journal.Search('Nie udalo Ci sie otworzyc') or Journal.Search('Juz cos robisz'):
            Journal.Clear('Nie udalo Ci sie otworzyc')
            Journal.Clear('Juz cos robisz')
            return False
        if Journal.Search('Udalo sie otworzyc'):
            Journal.Clear('Udalo sie otworzyc')
            crates.pop( 0 )
            return True
        
while True:
    print('zaczynamy zamykanie')
    SetCrates()
    counter = 0
    while crates.Count > 0:
        Misc.Pause(100)
        counter += 1
        CloseCrate()
        print(f"zamknalem nr {counter}")
    print('zaczynamy wlamywanie')
    SetCrates()
    counter = 1
    while crates.Count > 0:
        Misc.Pause(100)
        print(f"otwieram... crates:{crates.Count}")
        waitForTimer('lockTimer')
        if OpenCrate() == True:
            print(f"otworzono skrzynie nr {counter}")
            counter += 1
        else:
            print(f"nie udalo sie ze skrzynia nr {counter}")
    print('konczymy wlamywanie')
    Misc.Pause(12000)


    
    
    
