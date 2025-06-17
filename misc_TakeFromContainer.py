containerObj = Target.PromptTarget( 'Wybierz pojemnik z ktorego brac' )

container = Items.FindBySerial(containerObj)

itemToMoveID = 0x09D7

while True:
    for item in container.Contains:
        if item.ItemID == itemToMoveID:
            Items.Move(item.Serial,Player.Backpack.Serial,1)
            Misc.Pause( 1000 )
    Misc.Pause(400)
