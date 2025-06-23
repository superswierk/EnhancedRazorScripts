import sys

srcObj = Target.PromptTarget( 'SKAD' )
srcContainer = Items.FindBySerial(srcObj)
target = Target.PromptTarget( 'DOKAD' )

moveIDs = [0x1BD7, 0x1BF2, 0x0F25, 0x0F18, 0x0F15, 0x0F13]

if srcObj is None:
    Misc.SendMessage('Zly cel',33)
    sys.exit()

for item in srcContainer.Contains:
    for itemToMove in moveIDs:
        if item.ItemID == itemToMove:
            Items.Move(item,target,-1)
            Misc.Pause( 500 )
