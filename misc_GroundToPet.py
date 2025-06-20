from System.Collections.Generic import List
from System import Byte, Int32

containerObj = Target.PromptTarget( 'Wybierz pojemnik z ktorego brac' )

container = Items.FindBySerial(containerObj)

itemToMoveID = 0x19B9

def filterItem(id,range=2, movable=True):
    fil = Items.Filter()
    fil.Movable = movable
    fil.RangeMax = range
    fil.Graphics = List[Int32](id)
    list = Items.ApplyFilter(fil)

    return list

groundItems = filterItem([itemToMoveID])
    
Misc.Pause(400)
for item in groundItems:
    if item.ItemID == itemToMoveID and item.Hue == 0x04b9:
        Items.Move(item.Serial,containerObj,-1)
        Misc.Pause( 500 )
Misc.Pause(400)

