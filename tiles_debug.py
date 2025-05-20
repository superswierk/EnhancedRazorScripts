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
target = Target.PromptGroundTarget( 'Wybierz cel' )



tileinfo = Statics.GetStaticsLandInfo(target.X, target.Y, Player.Map)
tiles = Statics.GetStaticsTileInfo(target.X, target.Y, Player.Map)
Misc.SendMessage("StaticID Land: 0x{:x} #tiles{}".format(tileinfo.StaticID, len(tiles)), 66)
if len(tiles) > 0:
    Misc.SendMessage("Static ID Tile: 0x{:x} #tiles{}".format(tiles[0].StaticID, len(tiles)), 66)
    
