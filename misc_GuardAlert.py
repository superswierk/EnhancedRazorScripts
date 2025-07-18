from Scripts.EnhancedRazorScripts.misc_Discord import *
enemyThumb = "https://i.imgur.com/YvbQw56.png"
miningThumb = "https://i.imgur.com/cEvazS3.png"
Journal.Clear()
while True:
    enemy = Target.GetTargetFromList( 'enemywar' )
    if Journal.Search("ent: ent") or Journal.Search("Przyciagnales uwage") or Journal.Search("podchodzi zobaczyc co ciekawego") or enemy != None:
        if Journal.Search("ent: ent"):
            sendDiscord("Uwaga wrog w popblizu!", 15291726, enemyThumb)
        Journal.Clear()
        
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        Misc.Pause(2000)
        Player.ChatSay("STRAZE POMOCY BIJA MNIE!")
        Misc.Pause(2000)
    if Journal.Search( 'Nie masz miejsca' ) == True:
        Journal.Clear( 'Nie masz miejsca' )
        sendDiscord("Konie przepelnione!", 15291726, miningThumb)
    Misc.Pause(200)
