containerObj = Target.PromptTarget( 'Wybierz pojemnik z ktorego brac' )

container = Items.FindBySerial(containerObj)

#talez 0x09D7
#wiadro 0x0FAB
#topor 0x0F43
itemToMoveID = 0x0F43

while True:
    for item in container.Contains:
        if item.ItemID == itemToMoveID:
            Items.Move(item.Serial,Player.Backpack.Serial,1)
            Misc.Pause( 1000 )
    Misc.Pause(400)
