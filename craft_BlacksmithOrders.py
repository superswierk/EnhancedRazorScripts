from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys
from System.Collections.Generic import List
from System import Byte, Int32, Double
from math import sqrt
import System.IO
import time

carpThumb = "https://i.imgur.com/eIbSwww.png"
carpErrorThumb = "https://i.imgur.com/HTsTVcG.png"
apoThumb = "https://i.imgur.com/eDQLGaI.png"
foodThumb = "https://i.imgur.com/uB0tTVj.png"
lvlupThumb = "https://i.imgur.com/j5rUy80.png"
HoldOrdersTimerMs = 310000


CRAFTITEMS = {
    "czekaj": { "itemID" : 6666, "pageID" : 2, "type" : "metal" },
    "sztylet": { "itemID" : 3921, "pageID" : 10, "type" : "metal" },
    "szpikulec": { "itemID" : 11553, "pageID" : 10, "type" : "metal" },
    "katana": { "itemID" : 5118, "pageID" : 10, "type" : "metal" },
    "kris": { "itemID" : 5121, "pageID" : 10, "type" : "metal" },
    "sejmitar": { "itemID" : 5045, "pageID" : 10, "type" : "metal" },
    "krotki_miecz": { "itemID" : 5184, "pageID" : 10, "type" : "metal" },
    "sai": { "itemID" : 10234, "pageID" : 10, "type" : "metal" },
    "elfickie_ostrze": { "itemID" : 11552, "pageID" : 10, "type" : "metal" },
    "dlugi_mlot": { "itemID" : 5178, "pageID" : 14, "type" : "metal" },
    "duzy_mlot": { "itemID" : 5180, "pageID" : 14, "type" : "metal" },
    "bulawa": { "itemID" : 3932, "pageID" : 14, "type" : "metal" },
    "wojenna_bulawa": { "itemID" : 5126, "pageID" : 14, "type" : "metal" },
    "tetsubo": { "itemID" : 10225, "pageID" : 14, "type" : "metal" },
    "berlo": { "itemID" : 9916, "pageID" : 14, "type" : "metal" },
    "diamentowa_bulawa": { "itemID" : 11556, "pageID" : 14, "type" : "metal" },
    "dlugi_miecz": { "itemID" : 3936, "pageID" : 11, "type" : "metal" },
    "bitewny_miecz": { "itemID" : 3934, "pageID" : 11, "type" : "metal" },
    "dlugi_miecz": { "itemID" : 3936, "pageID" : 11, "type" : "metal" },
    "wielki_miecz": { "itemID" : 5049, "pageID" : 11, "type" : "metal" },
    "topor_zdobiony": { "itemID" : 11560, "pageID" : 12, "type" : "metal" },
    "duzy_bojowy_topor": { "itemID" : 5114, "pageID" : 12, "type" : "metal" },
    "niszczycielski_topor": { "itemID" : 3909, "pageID" : 12, "type" : "metal" },
    "siekiera": { "itemID" : 3913, "pageID" : 12, "type" : "metal" },
    "dwureczna_siekiera": { "itemID" : 5186, "pageID" : 12, "type" : "metal" },
    "podwojna_siekiera": { "itemID" : 3915, "pageID" : 12, "type" : "metal" },
    "kama": { "itemID" : 10232, "pageID" : 12, "type" : "metal" },
    "wojenny_topor": { "itemID" : 5039, "pageID" : 12, "type" : "metal" },
    "krotka_wlocznia": { "itemID" : 5122, "pageID" : 13, "type" : "metal" },
    "wlocznia": { "itemID" : 3939, "pageID" : 13, "type" : "metal" }, 
    "berdysz": { "itemID" : 3918, "pageID" : 13, "type" : "metal" },
    "halabarda": { "itemID" : 5182, "pageID" : 13, "type" : "metal" },
    "wojenne_widly": { "itemID" : 5124, "pageID" : 13, "type" : "metal" },
    "podwojne_ostrza": { "itemID" : 9919, "pageID" : 13, "type" : "metal" },
}



ORES = {
    "zelazo": 0x0000, #0x1BF2
    "zloto": 0x0461,
    "srebro": 0x0515,
    "veryt": 0x0590,
    "blackrock": 0x0455,
    "agapit": 0x0400,
    "valoryt": 0x07d1,
    "mytheril": 0x0528,
    "azuryt": 0x04df,
    "bloodrock": 0x051d,
    "royal": 0x04b9,
    "grafit": 0x03e7,
    "zwykle": 0x0000, #0x1BD7
    "dab": 0x0096,
    "orzech": 0x0611,
    "cedr": 0x0094,
    "cis": 0x0220,
    "wierzba": 0x01b8,
    "ohii": 0x05aa,
    "cyprys": 0x0091,
    "brak_materialu": 0x6666
}
boardsId = [0x1BD7]
stubsId = [0x1BF2]
KLEJNOTY = [0x0F25, 0x0F18, 0x0F15, 0x0F13]

toolsId = 0x102C
self_pack = Player.Backpack.Serial
orderID = 0x14F0
activeColor = 0x051e
inactiveColor = 0x051e

class CraftItem:
    itemID = None
    oreColor = None
    pageID = None
    typ = None
    amount = None
    itemName = None
    
    def __init__ ( self, itemID, oreColor, pageID, typ,  amount, itemName):
        self.itemID = itemID
        self.oreColor = oreColor
        self.pageID = pageID
        self.typ = typ
        self.amount = amount
        self.itemName = itemName
        
craftItems = []
workingBag = Target.PromptTarget( 'Wybierz pojemnik do pracy' )

srcOrd = 0x538A4E64#Target.PromptTarget( 'Pojemnik na zamowienia' )
ordContainer = Items.FindBySerial(srcOrd)
if srcOrd is None:
    Misc.SendMessage('Zly cel',33)
    sys.exit()
    
def currentTime():
    return Double(time.time() + Double(7200))

def isInJournal(text, secondsAgo):
    jList = Journal.GetJournalEntry( currentTime() - secondsAgo )
    for element in jList:
        if (element.Text.find(text) != -1):
            return True
    return False
    
def AcceptOrders():
    global ordContainer
    print("Akceptuje zamowienia po kolei")
    Misc.Pause(1000)
    if isInJournal("Zapis Stanu",40) == True:
        while isInJournal("Koniec zapisywania",40) == False:
            Misc.Pause(1000)
            print("Czekam na zapis swiata...");
        Misc.Pause(3000)
    for item in ordContainer.Contains:
        if item.ItemID == orderID and item.Color == activeColor:
            Items.UseItem(item)
            gumpId = 0
            Misc.Pause(500)
            while gumpId == 0:
                Misc.Pause(100)
                gumpId = Gumps.CurrentGump()
            print(f"First gump {gumpId} found")
            Gumps.SendAction(gumpId, 2)
            Gumps.WaitForGump(gumpId,10000)
            Misc.Pause(1000)
            #gumpId = 0
            #while gumpId == 0:
            #    Misc.Pause(100)
            #    gumpId = Gumps.CurrentGump()
            print(f"Second gump {gumpId} found")
            Gumps.SendAction(gumpId, 0)
            Misc.Pause(1000)


def createItemsToCraft():
    global craftItems
    craftItems = []
    
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
        
def getByItemIDColor(itemsIds, color, source):
    #find an item id in container serial
    searchItem = Items.FindBySerial(source)
    if hasattr(searchItem,'Contains'):
        for itemid in itemsIds:
            for item in searchItem.Contains:
                if item.ItemID == itemid and item.Color == color:
                    return item
                else:
                    Misc.NoOperation()
    else:
        Misc.NoOperation()
        
def usun_ostatnia_linie(tekst):
    # Dzieli string na listę linii. '\n' jest domyślnym separatorem.
    linie = tekst.splitlines()

    # Sprawdza, czy są jakieś linie do usunięcia.
    if len(linie) > 0:
        # Łączy wszystkie linie z wyjątkiem ostatniej, używając znaku nowej linii.
        return '\n'.join(linie[:-1])
    else:
        # Jeśli string jest pusty, zwraca pusty string.
        return ""
        
        
errorMessage = "Nieznany blad! Nie udalo sie dokonczyc craftowania"
realItemsCrafted = 0

def waitForTimer(name):
    while Timer.Check(name) == True:
        Misc.Pause(400)

def clearJournal():
    Journal.Clear('fatalnym')
    Journal.Clear('Brakuje Ci')
    Journal.Clear( 'miejsca w pojemniku' )
    Journal.Clear( 'Wykules' ) #Stworzyles
    Journal.Clear( 'Wypsnal' ) #przeskoczyly

def craftItem( itemToCraft ):
    global errorMessage
    global workingBag
    global realItemsCrafted
    realItemsCrafted = 0
    
    if itemToCraft.itemName == "czekaj":
        print("Dummy item czekanie")
        realItemsCrafted += 1
        return True
    
    endString = str(itemToCraft.amount) + " z " + str(itemToCraft.amount)
    tools = Player.GetItemOnLayer( 'RightHand' ).Serial
    Items.UseItem(tools)
    Misc.SendMessage('czekam na gump craftingu', 77)
    Gumps.WaitForGump(0,10000)
    Misc.Pause(4000)
    gumpId = Gumps.CurrentGump()
    print(f"wysylam page {itemToCraft.pageID}")
    Gumps.SendAdvancedAction(gumpId, itemToCraft.pageID, [], [1,2], [str(itemToCraft.amount),""])
    Misc.SendMessage('czekam na gump strony', 77)
    Gumps.WaitForGump(gumpId, 10000)
    Misc.Pause(500)
    print(f"wysylam id {itemToCraft.itemID}")
    Gumps.SendAdvancedAction(gumpId, itemToCraft.itemID, [], [1,2], [str(itemToCraft.amount),""])
    
    Target.WaitForTarget(10000, False)
    if itemToCraft.typ == "metal":
        workingBoards = getByItemIDColor(stubsId, itemToCraft.oreColor, workingBag)
    elif itemToCraft.typ == "drewno":
        workingBoards = getByItemIDColor(boardsId, itemToCraft.oreColor, workingBag)
    else:
        workingBoards = getByItemIDColor(KLEJNOTY, itemToCraft.oreColor, workingBag)
    if workingBoards is not None:
        Target.TargetExecute(workingBoards)
    else:
        Misc.SendMessage('Brak sztab!', 77)
        errorMessage = "Brakuje sztab!"
        Misc.Pause(2000)
        return False
    print("zaczynam craftowac")
    craftCounter = 0
    Timer.Create('craftingTimer', 12000)
    clearJournal()
    while True:
        Misc.Pause(300)
        Journal.Clear('Brakuje Ci skladnikow')
        if Journal.Search('fatalnym'):
            Journal.Clear('fatalnym')
            print("fatalny stan narzedzia")
        if Journal.Search('Brakuje Ci'):
            print("Koniec desek")
            errorMessage = "Koniec sztab!"
            Misc.Pause(2000)
            return False
        if Journal.Search( 'miejsca w pojemniku' ):
            print("Nie ma juz miejsca w pojemniku")
            realItemsCrafted += 1
            errorMessage = "Nie ma juz miejsca w pojemniku"
            Misc.Pause(2000)
            return False
        if  Journal.Search( endString ) or Timer.Check('craftingTimer') == False:
            if Journal.Search( endString ):
                craftCounter = craftCounter + 1
            if craftCounter > 0:
                print("Skonczylem craftowanie tego itemu")
                realItemsCrafted += 1
                Misc.Pause(2000)
                return True
            else:
                print("Wyglada ze nawet nie zaczelo sie nic")
                errorMessage = "Wyglada ze nawet nie zaczelo sie nic"
                Misc.Pause(2000)
                return False
        if Journal.Search( 'Wykules' ) or Journal.Search( 'Wypsnal' ):
            if Journal.Search( 'Wykules' ):
                realItemsCrafted += 1
            Journal.Clear('Wykules')
            Journal.Clear('Wypsnal')
            Timer.Create('craftingTimer',12000)
            craftCounter = craftCounter + 1
            print(craftCounter)

pathToScript = Misc.ScriptCurrent()
directoryPath = pathToScript.rsplit("\\",1)[0]

fileName = directoryPath + "\\craft_ItemList_Kowalstwo.txt"
fileBody = System.IO.File.ReadAllText(fileName)
jobsTable = fileBody.split("\n")
fileNameProgress = directoryPath + "\\craft_ItemList_Kowalstwo.progress"

craftItems = []
for job in jobsTable:
    print("to je linia: " + job + " end")
    if job != "":
        line = job.split(";")
        craftItems.Add( CraftItem( CRAFTITEMS[line[0]]["itemID"], ORES[line[1]],CRAFTITEMS[line[0]]["pageID"], CRAFTITEMS[line[0]]["type"], int(line[2]), line[0]) )

overrideLastAmount = 0
try:
    filePrevBody = System.IO.File.ReadAllText(fileNameProgress)
except Exception as e:
        print("Blad kurczaki : ",e)
        System.IO.File.WriteAllText(fileNameProgress, "" )
        filePrevBody = System.IO.File.ReadAllText(fileNameProgress)
if filePrevBody != "":
    jobsDoneTable = filePrevBody.split("\n")
    prevIt = 0
    for jobDone in jobsDoneTable:
        print("to je linia: " + job + " end")
        if jobDone != "":
            line = jobDone.split(";")
            newAmount = int(craftItems[prevIt].amount) - int(line[1])
            if newAmount > 0:
                tempBody = usun_ostatnia_linie(filePrevBody)
                System.IO.File.WriteAllText(fileNameProgress,tempBody)
                overrideLastAmount = int(craftItems[prevIt].amount)
            if newAmount < 0:
                newAmount = 0
            craftItems[prevIt].amount = newAmount
            prevIt += 1

        
#itemID = None
#oreColor = None
#pageID = None
#typ = None
#amount = None
#itemName = None

craftIterator = 0
successIterator = 0
wasFail = False
for iItem, item in enumerate(craftItems):
    Misc.Pause(300)
    craftIterator = craftIterator + 1
    print("craftuje item nr " + str(craftIterator))
    if item.amount <= 0:
        print("skipping item nr " + str(craftIterator))
        continue
    if craftItem(item) == True:
        print("Sukces udalo sie scraftowac nr " + str(craftIterator))
        successIterator += 1
        
        if overrideLastAmount > 0:
                realItemsCrafted = overrideLastAmount
                System.IO.File.AppendAllText(fileNameProgress, "\n" )
                overrideLastAmount = 0
        System.IO.File.AppendAllText(fileNameProgress, f"{item.itemName};{realItemsCrafted}\n" )
        Misc.Pause(1000)
        if iItem < (craftItems.Count - 1) and craftItems[iItem + 1].itemName == "czekaj":
            print("WYKONUJE CZEKANIE")
            waitForTimer("HoldOrdersTimer")
            Timer.Create("HoldOrdersTimer",HoldOrdersTimerMs);
            print("KONCZE CZEKANIE")
        Journal.Clear("Mam zamowienie")
        if craftItems[iItem].itemName == "czekaj":
            print("skip accept orders")
        else:
            AcceptOrders()
        Misc.Pause(600)
        if Journal.Search("Mam zamowienie"):
            Journal.Clear("Mam zamowienie")
            sendDiscord("Zamowienie specjalnie zaraz wpadnie", 9592372, carpThumb)
    else:
        wasFail = True
        sendDiscord(errorMessage + f"\nUkonczono z sukcesem tylko {successIterator} zadan", 14696255, carpErrorThumb)
        print("Nie udalo sie scraftowac nr " + str(craftIterator))
        print("PRZERYWAM SKRYPT COS NIE TAK")
        if realItemsCrafted > 0:
            if overrideLastAmount > 0:
                realItemsCrafted = overrideLastAmount
                System.IO.File.AppendAllText(fileNameProgress, "\n" )
                overrideLastAmount = 0
            System.IO.File.AppendAllText(fileNameProgress, f"{item.itemName};{realItemsCrafted}\n" )
        break
    
if wasFail == False:
    System.IO.File.WriteAllText(fileNameProgress, "" )
    sendDiscord(f"Sukces zakonczone craftowanie {successIterator} zadan", 9592372, carpThumb)
Misc.Pause(2000)
