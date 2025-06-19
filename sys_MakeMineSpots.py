from Scripts.EnhancedRazorScripts.misc_Discord import *
from System.Collections.Generic import List
from System import Byte, Int32
import System.IO
import System.Diagnostics

def setText(text):
    path = ".\\clipboard.txt"
    System.IO.File.WriteAllText(path, text)
    System.Diagnostics.Process.Start("notepad.exe", path)

class Spot:
    x = None
    y = None
    
    def __init__ ( self, x, y):
        self.x = x
        self.y = y

spots = []
spotString = ""

setX = 125 
setY = 125
offsetLabelY = 20
offsetRadioY = 45
offsetButtonY = 170
def sendgumpText():
    global spotString
    gd = Gumps.CreateGump(movable=True) 
    Gumps.AddPage(gd, 0)
    Gumps.AddBackground(gd, 0, 0, 283, 349, 9300) 
    Gumps.AddBackground(gd, 8, 32, 264, 304, 9350) 
    Gumps.AddLabel(gd,10,10,2410,'Wklej ten tekst do skryptu:')
    Gumps.AddHtml(gd,15,42,244,284,spotString,True,True)
    setText(spotString)
    Misc.SendMessage("ZAPISANO DO SCHOWKA",1100)
    Gumps.SendGump(666666, Player.Serial, setX, setY, gd.gumpDefinition, gd.gumpStrings)
    buttoncheckText()

def buttoncheckText():
    Gumps.WaitForGump(666666, 60000)
    Gumps.CloseGump(666666)

def sendgump():
    gd = Gumps.CreateGump(movable=True) 
    
    Gumps.AddPage(gd, 0)
    Gumps.AddBackground(gd, 0, 0, 180, 100, 2620) 

    iY = 0
    Gumps.AddLabel(gd,15,iY + offsetLabelY,2407,'Tworzenie Mining Spots')

    iY = iY + 36
    Gumps.AddButton(gd,30,iY + offsetLabelY,2460,2461,123,1,0)
    Gumps.AddButton(gd,110,iY + offsetLabelY,2450,2451,124,1,0)

    Gumps.SendGump(696669, Player.Serial, setX, setY, gd.gumpDefinition, gd.gumpStrings)
    buttoncheck()
    
def buttoncheck():
    global spots
    global spotString
    Gumps.WaitForGump(696669, 60000)
    Gumps.CloseGump(696669)
    gdata = Gumps.GetGumpData(696669)
    if gdata.buttonid == 123:
        print("dodaj spot")
        spots.Add( Spot(Player.Position.X, Player.Position.Y))
        print(str(spots.Count) + ". X=" + str(spots[spots.Count - 1].x) + " Y=" + str(spots[spots.Count - 1].y))
        Misc.Pause(200)
        sendgump()
    elif gdata.buttonid == 124:
        print("wyswietlam dodane:")
        spotString = ""
        for spot in spots:
            spotString += "spots.Add( Spot( " + str(spot.x) + ", " + str(spot.y) + " ))\n"
        print(spotString)
        sendgumpText()
    else:
        print("domyslna wartosc")


sendgump()
Misc.Pause(400)