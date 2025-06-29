import sys
hidingMs = 10200
stealthMs = 12200

Misc.SendMessage( 'Beginning Stealth training', 90 )

Timer.Create( 'hidingTimer', 1 )
Timer.Create( 'stealthTimer', 1 )

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
    Journal.Clear("ukryles sie")
    Journal.Clear("Nie udalo Ci sie ukryc")
    Journal.Clear("Juz cos robisz")
    Player.UseSkill( 'Ukrywanie' )
    Timer.Create( 'hidingTimer', hidingMs )
    while True:
        Misc.Pause(400)
        saveGameCheck()
        if Journal.Search("Nie udalo Ci sie ukryc") or Journal.Search("Juz cos robisz"):
            waitForTimer('hidingTimer')
            Journal.Clear("Nie udalo Ci sie ukryc")
            Journal.Clear("Juz cos robisz")
            Player.UseSkill( 'Ukrywanie' )
            Timer.Create( 'hidingTimer', hidingMs )
        if Journal.Search("ukryles sie"):
            Journal.Clear("ukryles sie")
            Misc.Pause(400)
            return
Journal.Clear()
forceHide()
Misc.SendMessage("Na pewno sie schowales", 77)
waitForTimer('hidingTimer')
Journal.Clear("Zeby sie skradac")
Journal.Clear("Juz cos robisz")
Journal.Clear("Odkryles siebie")
Journal.Clear("Teraz poruszasz sie")
Misc.SendMessage("Prubuje zakradac", 77)
Player.UseSkill( 'Zakradanie' )
Timer.Create( 'stealthTimer', stealthMs )
while True:
    Misc.Pause(400)
    saveGameCheck()
    if Journal.Search("Teraz poruszasz sie"):
        Journal.Clear("Teraz poruszasz sie")
        waitForTimer('stealthTimer')
        Misc.SendMessage("Prubuje zakradac", 77)
        Player.UseSkill( 'Zakradanie' )
        Timer.Create( 'stealthTimer', stealthMs )
    if Journal.Search("Odkryles siebie") or Journal.Search("Zeby sie skradac"):
        Journal.Clear("Odkryles siebie")
        Journal.Clear("Zeby sie skradac")
        Misc.SendMessage("Nie udalo sie zakradac", 1100)
        waitForTimer('stealthTimer')
        forceHide()
        Misc.SendMessage("Na pewno sie schowales", 77)
        waitForTimer('hidingTimer')
        Misc.SendMessage("Prubuje zakradac", 77)
        Player.UseSkill( 'Zakradanie' )
        Timer.Create( 'stealthTimer', stealthMs )
