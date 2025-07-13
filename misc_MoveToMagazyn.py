import sys

#Player.ChatSay(".sortuj")
#Misc.Pause(1000)
#Target.TargetExecute(0x51B09F1E)
#sys.exit()
#magazynier
#vaekin magazynID = 0x51B09F1E
#dajson magazynID = 0x53D780E8
magazynID = 0x53D780E8
if Player.Name == "Vaekin":
    magazynID = 0x51B09F1E
if Player.Name == "Dajson":
    magazynID = 0x53D780E8
if Player.Name == "Spruce":
    magazynID = 0x53F07BE8
    
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
'''
#Player.ChatSay('.licz')
sawId = 0x1035
saw = getByItemID(sawId, Player.Backpack.Serial)
Items.UseItem(saw)
Target.WaitForTarget( 5000 , True )
Target.TargetExecute(magazynID)
sys.exit()
'''
'''
Player.ChatSay('.licz')
Target.WaitForTarget( 5000 , True )
Target.TargetExecute(magazynID)
sys.exit()
'''
itemFrom = Items.FindBySerial( Target.PromptTarget( 'Wybierz typ a przeniose wszystkie' ))

if itemFrom is None:
    Misc.SendMessage('Zly cel',33)
    sys.exit()
containerFrom = Items.FindBySerial( itemFrom.Container )
itemIDFrom = itemFrom.ItemID
containerTo = magazynID

Misc.SendMessage('Przenosze',33)
for i, item in enumerate(containerFrom.Contains):
    if item.ItemID == itemIDFrom:
        Items.Move(item,magazynID,-1)
        Misc.Pause( 500 )
        
Misc.SendMessage('Przenoszenie ZAKONCZONE',63)
