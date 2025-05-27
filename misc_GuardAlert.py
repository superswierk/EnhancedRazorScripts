while True:
    if Journal.Search("Przyciagnales uwage",) or Journal.Search("podchodzi zobaczyc co ciekawego ") or Journal.Search("wir"):
        Journal.Clear()
        Player.ChatSay("STRAZE POMOCY BIJA MNIE")
        Misc.Pause(1000)
        Player.ChatSay("STRAZE POMOCY BIJA MNIE!")
