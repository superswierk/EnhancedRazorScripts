from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys
from System.Net.Mail import SmtpClient, MailMessage, MailAddress
from System.Net import NetworkCredential
Round = lambda x, n: eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n)))
carpThumb = "https://i.imgur.com/ssu1MFc.png"
apoThumb = "https://i.imgur.com/eDQLGaI.png"
foodThumb = "https://i.imgur.com/uB0tTVj.png"
lvlupThumb = "https://i.imgur.com/j5rUy80.png"
#tools = Target.PromptTarget( 'Wybierz narzedzia stolarskie' )
workingBag = Target.PromptTarget( 'Wybierz pojemnik do pracy' )
claenCraftedItems = False
tools = 0x53BE5FDC
#boards = Target.PromptTarget( 'Wybierz deski' )
itemsToDrop = [0x13F9,]
boardId = 0x1BD7
sawId = 0x1035
cleanItemId = 0x0F64
toolsId = 0x1030
self_pack = Player.Backpack.Serial
workingBoards = None

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
        
def sendEmailMessage(sub, tex):
    mail = MailMessage()
    mail.From = MailAddress("ultimaandrzej@gmail.com");


    smtp = SmtpClient()
    smtp.Port                  = 587;   
    smtp.EnableSsl             = True;
    #smtp.DeliveryMethod        = SmtpDeliveryMethod.Network; 
    ##smtp.UseDefaultCredentials = True; 
    smtp.Credentials = NetworkCredential("ultimaandrzej@gmail.com",  "xxxx xxxx xxxx xxxx");  
    smtp.Host        = "smtp.gmail.com";            

    mail.To.Add(MailAddress("superswierk@gmail.com"));
    mail.IsBodyHtml = True;
    st              = "Test";
    mail.Subject = sub
    mail.Body = tex;
    smtp.Send(mail);
###################################

def doCarpet():
    global workingBoards
    tools = getByItemID(toolsId, self_pack)
    Items.UseItem(tools)
    Misc.SendMessage('czekam na gump1', 77)
    Gumps.WaitForGump(0,10000)
    Misc.Pause(4000)
    gumpId = Gumps.CurrentGump()
    #Gumps.SendAdvancedAction(gumpId, 3940, [], [1,2], ["4",""])
    #Gumps.SendAdvancedAction(gumpId, 3636, [], [1,2], ["100",""])
    Gumps.SendAdvancedAction(gumpId, 1, [], [1,2], ["100",""])
    Target.WaitForTarget(10000, False)
    workingBoards = getByItemID(boardId, workingBag)
    if workingBoards is not None:
        Target.TargetExecute(workingBoards)
    else:
        Misc.SendMessage('Koniec desek', 77)
        #sendEmailMessage('Uwaga stolarzu', 'Deski sie skonczyly')
        sendDiscord("Uwaga koniec desek!", 14696255, carpThumb)
        Misc.Pause(6000)
        sys.exit()

def MoveToGround():
    for item in Player.Backpack.Contains:
        for itemToDrop in itemsToDrop: 
            if item.ItemID == itemToDrop:
                Items.DropItemGroundSelf(item,0)
                Misc.Pause( 700 )
        
def destroyItems():
    saw = getByItemID(sawId, Player.Backpack.Serial)
    Items.UseItem(saw)
    Journal.Clear()
    Target.WaitForTarget(2000, True)
    Target.TargetExecute(workingBag)
    Timer.Create('destroyTimer',4000)
    while Timer.Check('destroyTimer')==True:
        if Journal.Search('Poci'):
            Journal.Clear('Poci')
            Timer.Create('destroyTimer',4000)
        Misc.Pause(200)
    
def doCleaning():
    cleanItem = getByItemID(cleanItemId, workingBag)
    Misc.SendMessage('Rozwalam rzeczy',55)
    while cleanItem is not None:
        Items.UseItem(sawId)
        Target.WaitForTarget(2000, True)
        Target.TargetExecute(cleanItem)
        Misc.Pause(3000)
        cleanItem = getByItemID(cleanItemId, workingBag)

lvlCarpSkill = Round(Player.GetRealSkillValue('Stolarstwo'),1)
Player.ChatSay('.glod wszystko')
Misc.Pause(1000)
glod = Journal.GetLineText('Glod')
bialka = Journal.GetLineText('Bialka')
witaminy = Journal.GetLineText('Witaminy')
weglowodany = Journal.GetLineText('Weglowodany')
Timer.Create('eatingLogTimer', 120000)
Timer.Create('boardStatusTimer', 900000)
Journal.Clear()
doCarpet()
craftCounter = 0
apocalipse = False
while True:
    if Journal.Search('Brakuje Ci'):
        sendDiscord("Uwaga koniec desek!", 14696255, carpThumb)
        Misc.Pause(6000)
        sys.exit()
    if(Timer.Check('boardStatusTimer') == False):
        Timer.Create('boardStatusTimer', 900000)
        workingBoards = getByItemID(boardId, workingBag)
        if workingBoards is not None:
            sendDiscord("Pracuje na deskach: " + str(workingBoards.Amount) + " " + workingBoards.Name, 9592372, carpThumb)
    if(Timer.Check('eatingLogTimer') == False):
        Timer.Create('eatingLogTimer', 120000)
        if apocalipse == False and Journal.Search('Apokalipsa'):
            apokalipseStr = Journal.GetLineText('Apokalipsa')
            apocalipse = True
            sendDiscord("Uwaga:\n" + apokalipseStr + "\n", 14696255, apoThumb)
  
        Player.ChatSay('.glod wszystko')
        Misc.Pause(1000)
        newGlod = Journal.GetLineText('Glod')
        newBialka = Journal.GetLineText('Bialka')
        newWitaminy = Journal.GetLineText('Witaminy')
        newWeglowodany = Journal.GetLineText('Weglowodany')
        if newGlod != glod or newBialka != bialka or newWitaminy != witaminy or newWeglowodany != weglowodany :
            glod = newGlod
            bialka = newBialka
            witaminy = newWitaminy
            weglowodany = newWeglowodany
            if apocalipse:
                sendDiscord("Status glodu:\n" + glod + "\n" + bialka + "\n" + witaminy + "\n" + weglowodany + "\n" + apokalipseStr + "\n",14696255, apoThumb)
            else:
                sendDiscord("Status glodu:\n" + glod + "\n" + bialka + "\n" + witaminy + "\n" + weglowodany + "\n",2012169, foodThumb)
    lvlCarpSkillNew = Round(Player.GetRealSkillValue('Stolarstwo'),1)
    if lvlCarpSkill != lvlCarpSkillNew:
        lvlCarpSkill = lvlCarpSkillNew
        sendDiscord("Wzrost umiejetnosci Stolarstwo masz teraz: " + str(lvlCarpSkill), 5814783, lvlupThumb)
        Misc.Pause(1000)
    if (craftCounter > 0 and Timer.Check('choppingTimer') == False) or Journal.Search( '100 z 100' ) or Journal.Search( 'Pociales' ) or Journal.Search( 'odzyskac' ):
        Journal.Clear()
        Misc.SendMessage('Restart', 67)
        Misc.SendMessage('counter restart: %i' % (craftCounter), 67)
        Player.UseSkill('Ukrywanie')
        Misc.Pause(5000)
        craftCounter = 0
        doCarpet()
    elif Journal.Search( 'Stworzyles' ) or Journal.Search( 'wyskoczyla' ):
        Journal.Clear('Stworzyles')
        Journal.Clear('wyskoczyla')
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
        sendDiscord("Plecak pelny tne deski", 13093386, carpThumb)
        #sendEmailMessage('Uwaga stolarzu', 'nie ma miejsca w pojemniku')
        #sys.exit()
        destroyItems()
        Misc.Pause(2000)
        MoveToGround()
        Misc.Pause(2000)
        doCarpet()
    Misc.Pause(200)