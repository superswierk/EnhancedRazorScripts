from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys
tinkerExpThumb = "https://i.imgur.com/BgYU7mR.png"
braceletId = 0x1086

watchPart = Items.FindBySerial( Target.PromptTarget( 'Wybierz czesci do zegara' ))

if watchPart is None:
    Misc.SendMessage('Zly cel',33)
    sys.exit()
containerFrom = Items.FindBySerial( watchPart.Container )
watchPartId = watchPart.ItemID


Misc.SendMessage('Zaczynam produkcje zegaraka',33)
for watchPartItem in containerFrom.Contains:
    if watchPartItem is not None and watchPartItem.ItemID == watchPartId:
        for bracelet in containerFrom.Contains:
            if bracelet is not None and bracelet.ItemID == braceletId:
                print("uzwyam czesci")
                Items.UseItem(watchPartItem)
                Target.WaitForTarget(10000, False)
                Misc.Pause(500)
                Target.TargetExecute(bracelet)
                Journal.Clear()
                while True:
                    Misc.Pause(300)
                    if Journal.Search("Zlozyles czesci") == True or Journal.Search("Stworzyles") == True:
                        if Journal.Search("Stworzyles") == True:
                            sendDiscord(Journal.GetLineText("Stworzyles"), 9592372, tinkerExpThumb)
                        break
                print("zegarek zrobiony")
                Misc.Pause(2000)
                break
Misc.SendMessage('Produkcja zakonczona',33)