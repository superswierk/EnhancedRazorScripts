from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys
Round = lambda x, n: eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n)))
carpThumb = "https://i.imgur.com/wGXF6p5.png"
apoThumb = "https://i.imgur.com/eDQLGaI.png"
foodThumb = "https://i.imgur.com/uB0tTVj.png"
lvlupThumb = "https://i.imgur.com/j5rUy80.png"
#tools = Target.PromptTarget( 'Wybierz narzedzia stolarskie' )
workingBag = Target.PromptTarget( 'Wybierz pojemnik do pracy' )
claenCraftedItems = False
tools = 0x53BE5FDC
#boards = Target.PromptTarget( 'Wybierz deski' )
itemsToDrop = [0x13F6, 0x14FB, 0x26BB, 0x0F9D]
boardId = 0x1BF2
sawId = 0x1035
cleanItemId = 0x0F64
toolsId = 0x1EBC
self_pack = Player.Backpack.Serial
workingBoards = None
owen = 0x53F1D04E

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

def doCarpet():
    global workingBoards
    tools = getByItemID(toolsId, self_pack)
    Items.UseItem(tools)
    Misc.SendMessage('czekam na gump1', 77)
    Gumps.WaitForGump(0,10000)
    Misc.Pause(4000)
    gumpId = Gumps.CurrentGump()
    Gumps.SendAdvancedAction(gumpId, 1, [], [1,2], ["100",""])
    Target.WaitForTarget(10000, False)
    workingBoards = getByItemID(boardId, workingBag)
    if workingBoards is not None:
        Target.TargetExecute(workingBoards)
    else:
        Misc.SendMessage('Koniec sztab', 77)
        sendDiscord("Uwaga koniec sztab!", 14696255, carpThumb)
        Misc.Pause(6000)
        sys.exit()

def MoveToGround():
    for item in Player.Backpack.Contains:
        for itemToDrop in itemsToDrop: 
            if item.ItemID == itemToDrop:
                Items.DropItemGroundSelf(item,0)
                Misc.Pause( 700 )
        
def destroyItems():
    global owen
    saw = owen
    Items.UseItem(saw)
    Journal.Clear()
    Target.WaitForTarget(2000, True)
    Target.TargetExecute(workingBag)
    Misc.SendMessage('zaczynam niszczycz', 67)
    Timer.Create('destroyTimer',8000)
    Journal.Clear('Przetapianie zakonczone')
    Journal.Clear('topi')
    while Timer.Check('destroyTimer')==True:
        if Journal.Search('Przetapianie zakonczone'):
            Journal.Clear('Przetapianie zakonczone')
            break
        if Journal.Search('topi'):
            Journal.Clear('topi')
            Timer.Create('destroyTimer',8000)
        Misc.Pause(200)
    Misc.SendMessage('skonczylem niszczycz', 67)
    
def doCleaning():
    cleanItem = getByItemID(cleanItemId, workingBag)
    Misc.SendMessage('Rozwalam rzeczy',55)
    while cleanItem is not None:
        Items.UseItem(sawId)
        Target.WaitForTarget(2000, True)
        Target.TargetExecute(cleanItem)
        Misc.Pause(3000)
        cleanItem = getByItemID(cleanItemId, workingBag)


Timer.Create('boardStatusTimer', 900000)
Journal.Clear()
doCarpet()
craftCounter = 0

while True:
    Journal.Clear('Brakuje Ci skladnikow')
    if Journal.Search('fatalnym'):
        Journal.Clear('fatalnym')
        sendDiscord("Uwaga narzedzia druciarskie sie koncza!", 9592372, carpThumb)
    if Journal.Search('Brakuje Ci'):
        sendDiscord("Uwaga koniec desek!", 14696255, carpThumb)
        Misc.Pause(6000)
        sys.exit()
    if(Timer.Check('boardStatusTimer') == False):
        Timer.Create('boardStatusTimer', 900000)
        workingBoards = getByItemID(boardId, workingBag)
        if workingBoards is not None:
            sendDiscord("Pracuje na sztabach: " + str(workingBoards.Amount) + " " + workingBoards.Name, 9592372, carpThumb)

    if (craftCounter > 0 and Timer.Check('choppingTimer') == False) or Journal.Search( '100 z 100' ) or Journal.Search( 'Pociales' ) or Journal.Search( 'odzyskac' ):
        Journal.Clear()
        Misc.SendMessage('Restart', 67)
        Misc.SendMessage('counter restart: %i' % (craftCounter), 67)
        Player.UseSkill('Ukrywanie')
        Misc.Pause(5000)
        craftCounter = 0
        doCarpet()
    elif Journal.Search( 'Stworzyles' ) or Journal.Search( 'przeskoczyly' ):
        Journal.Clear('Stworzyles')
        Journal.Clear('przeskoczyly')
        Timer.Create('choppingTimer',12000)
        craftCounter = craftCounter + 1
        Misc.SendMessage('counter: %i' % (craftCounter), 67)
    if claenCraftedItems == True and Journal.Search( 'miejsca w pojemniku' ):
        Misc.SendMessage('czyszczenie pojemnika', 67)
        Journal.Clear()
        doCleaning()
    elif Journal.Search( 'miejsca w pojemniku' ):
        Journal.Clear( 'miejsca w pojemniku' )
        Misc.SendMessage('nie ma miejsca', 67)
        sendDiscord("Plecak pelny przetapiam na sztaby", 13093386, carpThumb)
        destroyItems()
        Misc.Pause(2000)
        MoveToGround()
        Misc.Pause(5000)
        craftCounter = 0
        doCarpet()
    Misc.Pause(400)
    
    
