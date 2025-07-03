import sys
hidingMs = 10200
stealthMs = 12200
musicId = 0x0E9E #tamburyn 0x0E9E
Misc.SendMessage( 'Beginning Hidding training', 90 )

Timer.Create( 'hidingTimer', 1 )
Timer.Create( 'stealthTimer', 1 )


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

def playMusic():
    global musicId
    playItem = getByItemID(musicId, Player.Backpack.Serial)
    if playItem is not None:
        Items.UseItem(playItem)
        print('Gram muzyke!')
        
    else:
        print('nie gram muzyki cos nie tak!')


def saveGameCheck():
    if Journal.Search("Zapisywanie Stanu Swiata"):
        Journal.Clear("Zapisywanie Stanu Swiata")
        if Timer.Check('hidingTimer') == True:
            rTime = Timer.Remaining('hidingTimer')
            Timer.Create('hidingTimer',rTime + 3000)
        if Timer.Check('stealthTimer') == True:
            rTime = Timer.Remaining('stealthTimer')
            Timer.Create('stealthTimer',rTime + 3000)

def waitForTimer(name):
    while Timer.Check(name) == True:
        saveGameCheck()
        Misc.Pause(400)

def forceHide():
    print("probuje ukryc")
    Journal.Clear("ukryles sie")
    Journal.Clear("Nie udalo Ci sie ukryc")
    Journal.Clear("Juz cos robisz")
    Player.UseSkill( 'Ukrywanie' )
    Timer.Create( 'hidingTimer', hidingMs )
    while True:
        Misc.Pause(400)
        saveGameCheck()
        if Journal.Search("Nie udalo Ci sie ukryc") or Journal.Search("Juz cos robisz"):
            Misc.Pause(400)
            playMusic()
            waitForTimer('hidingTimer')
            Journal.Clear("Nie udalo Ci sie ukryc")
            Journal.Clear("Juz cos robisz")
            Player.UseSkill( 'Ukrywanie' )
            Timer.Create( 'hidingTimer', hidingMs )
        if Journal.Search("ukryles sie"):
            Journal.Clear("ukryles sie")
            Misc.Pause(400)
            playMusic()
            print("udalo sie")
            return
Journal.Clear()
while True:
    Misc.Pause(400)
    forceHide()
    waitForTimer('hidingTimer')
    