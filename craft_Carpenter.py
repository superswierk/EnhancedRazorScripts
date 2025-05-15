import sys
from System.Net.Mail import SmtpClient, MailMessage, MailAddress
from System.Net import NetworkCredential

#tools = Target.PromptTarget( 'Wybierz narzedzia stolarskie' )
workingBag = Target.PromptTarget( 'Wybierz pojemnik do pracy' )
claenCraftedItems = False
tools = 0x53BE5FDC
#boards = Target.PromptTarget( 'Wybierz deski' )
boards = 0x53BD2DC6
boardId = 0x1BD7
sawId = 0x53BCDAE9
cleanItemId = 0x0F64
toolsId = 0x1030
self_pack = Player.Backpack.Serial

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
    tools = getByItemID(toolsId, self_pack)
    Items.UseItem(tools)
    Misc.SendMessage('czekam na gump1', 77)
    Gumps.WaitForGump(0,10000)
    Misc.Pause(2000)
    gumpId = Gumps.CurrentGump()
    #Gumps.SendAdvancedAction(gumpId, 3940, [], [1,2], ["4",""])
    Gumps.SendAdvancedAction(gumpId, 3636, [], [1,2], ["100",""])
    Target.WaitForTarget(10000, False)
    boards = getByItemID(boardId, workingBag)
    if boards is not None:
        Target.TargetExecute(boards)
    else:
        Misc.SendMessage('Koniec desek', 77)
        sendEmailMessage('Uwaga stolarzu', 'Deski sie skonczyly')
        sys.exit()
        
    
def doCleaning():
    cleanItem = getByItemID(cleanItemId, workingBag)
    Misc.SendMessage('Rozwalam rzeczy',55)
    while cleanItem is not None:
        Items.UseItem(sawId)
        Target.WaitForTarget(2000, True)
        Target.TargetExecute(cleanItem)
        Misc.Pause(3000)
        cleanItem = getByItemID(cleanItemId, workingBag)
Journal.Clear()
doCarpet()
while True:
    if Journal.Search( '100 z 100' ) or Journal.Search( 'Pociales' ) or Journal.Search( 'odzyskac' ):
        Journal.Clear()
        Misc.SendMessage('Restart', 67)
        Player.UseSkill('Ukrywanie')
        Misc.Pause(1000)
        doCarpet()
    if claenCraftedItems == True and Journal.Search( 'miejsca w pojemniku' ):
        Misc.SendMessage('czyszczenie pojemnika', 67)
        Journal.Clear()
        doCleaning()
    Misc.Pause(200)