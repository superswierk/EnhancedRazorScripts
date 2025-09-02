from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys
enemyThumb = "https://i.imgur.com/YvbQw56.png"
fishingTimerMs = 15000
water = Target.PromptGroundTarget( 'Wybierz pojemnik z woda' )
self_pack = Player.Backpack.Serial
rod = Player.GetItemOnLayer( 'LeftHand' ).Serial
runDrection = "East"
enemeyMessage = False

def clearJournalEnemy():
    Journal.Clear("ent: ent")
    Journal.Clear("zywiolak wody: zywiolak wody")
    Journal.Clear("waz morski: waz morski")
    Journal.Clear("Oops, to nie ryba!")
    Journal.Clear("Przyciagnales uwage")
    Journal.Clear("podchodzi zobaczyc co ciekawego")

def checkJournalEnemy():
    if (Journal.Search("ent: ent") or 
        Journal.Search("zywiolak wody: zywiolak wody") or 
        Journal.Search("waz morski: waz morski") or 
        Journal.Search("Oops, to nie ryba!") or 
        Journal.Search("Przyciagnales uwage") or 
        Journal.Search("podchodzi zobaczyc co ciekawego")):
            return True
    return False
def clearJournalFishing():
    Journal.Clear( 'Slabo dzis biora...' )
    Journal.Clear( 'Wylowiles' )
    Journal.Clear( 'Wyglada' )
    Journal.Clear( 'Moze' )
    Journal.Clear( 'Oho! haczyk od twojej' )
    Journal.Clear( 'Zlapales' )
    Journal.Clear( 'Dorwales' )
    Journal.Clear( 'Znalazles' )
    Journal.Clear( 'Wyszarpales' )
    Journal.Clear( 'Udalo Ci sie' )
    
def checkJournalFishing():
    if (Journal.Search( 'Slabo dzis biora...' ) or
        Journal.Search( 'Wylowiles' ) or
        Journal.Search( 'Wyglada' ) or
        Journal.Search( 'Moze' ) or
        Journal.Search( 'Oho! haczyk od twojej' ) or
        Journal.Search( 'Zlapales' ) or
        Journal.Search( 'Dorwales' ) or
        Journal.Search( 'Znalazles' ) or
        Journal.Search( 'Wyszarpales' ) or
        Journal.Search( 'Udalo Ci sie' )):
            return True
    return False
Journal.Clear()
while True:
    Misc.SendMessage('Zarzucam wedke',55)
    Items.UseItem(rod)
    Target.WaitForTarget(2000, True)
    Target.TargetExecute(water.X,water.Y,water.Z)
    Timer.Create('fishingTimer',fishingTimerMs)
    while True:
        Misc.Pause(200)
        if enemeyMessage == False:
            enemy = Target.GetTargetFromList( 'enemywar' )
            if enemy != None or checkJournalEnemy():
                enemeyMessage = True
                sendDiscord("Chyba wylowiles wroga!", 15291726, enemyThumb)
                Timer.Create("runTimer",8000)
                while Timer.Check("runTimer") == True:
                    Player.Run(runDrection)
                sys.exit()
        if checkJournalFishing() == True:
            clearJournalFishing()
            Timer.Create('fishingTimer',fishingTimerMs)
        if Timer.Check('fishingTimer') == False:
            break
    Misc.Pause(2000)  
    Misc.SendMessage('Koniec lowienia',55)
