containerObj = Target.PromptTarget( 'Wybierz pojemnik z ktorego brac' )

container = Items.FindBySerial(containerObj)




itemToMoveID = 0x1766


for item in Player.Backpack.Contains:
    if item.ItemID == itemToMoveID:
        Items.Move(item.Serial,containerObj,1)
        Misc.Pause( 1000 )

