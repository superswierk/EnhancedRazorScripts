import sys




#magazynier
#vaekin magazynID = 0x51B09F1E
#dajson magazynID = 0x53D780E8
magazynID = 0x53D780E8

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
for item in containerFrom.Contains:
    if item.ItemID == itemIDFrom:
        Items.Move(item,magazynID,-1)
        Misc.Pause( 1000 )
