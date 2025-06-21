while True:
    enemy = Target.GetTargetFromList( 'enemywar' )
    if Journal.Search("Przyciagnales uwage",) or Journal.Search("podchodzi zobaczyc co ciekawego") or enemy != None:
        Journal.Clear()
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        Misc.Pause(2000)
        Player.ChatSay("STRAZE POMOCY BIJA MNIE!")
        Misc.Pause(2000)
    Misc.Pause(200)
