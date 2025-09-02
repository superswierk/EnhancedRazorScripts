from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys
enemyThumb = "https://i.imgur.com/YvbQw56.png"
cookingTimerMs = 15000
#water = Target.PromptGroundTarget( 'Wybierz pojemnik z woda' )
self_pack = Player.Backpack.Serial
#rod = Player.GetItemOnLayer( 'LeftHand' ).Serial

coockBook = 0x5523838B
playerBag = 0x5415DCAA
pantryBag = 0x53F07BE8

def resetStock():
    print("reset stocka")
    Restock.RunOnce("uncookedfish",pantryBag,playerBag,100)
    Organizer.RunOnce("cookedfish",playerBag,pantryBag,100)

def clearJournalCooking():
    Journal.Clear( 'Nie udalo Ci sie' )
    Journal.Clear( 'O kurcze' )
    Journal.Clear( 'Udalo Ci sie' )
    
def checkJournalCooking():
    if (Journal.Search( 'Nie udalo Ci sie' ) or
        Journal.Search( 'O kurcze' ) or
        Journal.Search( 'Udalo Ci sie' )):
            return True
    return False

    
resetStock()
Journal.Clear()
while True:
    Misc.SendMessage('Gotuje...',55)
    Items.UseItem(coockBook)
    gumpId = 0
    Misc.Pause(500)
    while gumpId == 0:
        Misc.Pause(100)
        gumpId = Gumps.CurrentGump()
    
    Gumps.SendAdvancedAction(gumpId, 99, [], [1], ["100"])
    Timer.Create('cookingTimer',cookingTimerMs)
    while True:
        Misc.Pause(200)
        if checkJournalCooking() == True:
            clearJournalCooking()
            Timer.Create('cookingTimer',cookingTimerMs)
        if Timer.Check('cookingTimer') == False:
            break
    Misc.Pause(1000)
    resetStock()
    Misc.Pause(1000)
    Misc.SendMessage('Koniec gotowania',55)
    
