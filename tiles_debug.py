import sys

Player.ChatSay("Za mna!")
Player.ChatSay("Za mna")
Timer.Create("runTimer",12000)
while Timer.Check("runTimer") == True:
    Player.Run('Right')
sys.exit()


'''
from System.Collections.Generic import List
from System import Byte, Int32
def filterItem(id,range=30, movable=False):
    fil = Items.Filter()
    fil.Movable = movable
    fil.RangeMax = range
    fil.Graphics = List[Int32](id)
    list = Items.ApplyFilter(fil)
    return list
groundItems = filterItem([0x0C9B,])
Misc.SendMessage("StaticID Land: %i" %(len(groundItems)),33)
'''
'''
tileinfo = Statics.GetStaticsLandInfo(target.X, target.Y, Player.Map)
tiles = Statics.GetStaticsTileInfo(target.X, target.Y, Player.Map)
Misc.SendMessage("StaticID Land: 0x{:x} #tiles{}".format(tileinfo.StaticID, len(tiles)), 66)
if len(tiles) > 0:
    Misc.SendMessage("Static ID Tile: 0x{:x} #tiles{}".format(tiles[0].StaticID, len(tiles)), 66)
'''

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
#boardId=0x1BD7
#workingBag = Target.PromptTarget( 'Wybierz cel' )
#boards = getByItemID(boardId, workingBag)
#print(str(boards.Amount) + " " + boards.Name)

