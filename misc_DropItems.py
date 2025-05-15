import sys

#magazynier
magazynID = 0x51B09F1E
itemsToDrop = [0x09D7, 0x15F8]
dragDelay = 700

def MoveToGround():
    for item in Player.Backpack.Contains:
        for itemToDrop in itemsToDrop: 
            if item.ItemID == itemToDrop:
                Items.DropItemGroundSelf(item,0)
                Misc.Pause( dragDelay )
                
MoveToGround()
Misc.SendMessage( 'Wyrzucilem co trzeba', 31 )
