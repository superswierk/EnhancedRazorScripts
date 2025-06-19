import sys

containerObj = Target.PromptTarget( 'Wybierz pojemnik z ktorego wywalic rzeczy' )
container = Items.FindBySerial(containerObj)
itemsToDrop = [0x09D7, 0x15F8,0x0FF6]
dragDelay = 400

def MoveToGround():
    for item in container.Contains:
        for itemToDrop in itemsToDrop: 
            if item.ItemID == itemToDrop:
                Items.DropItemGroundSelf(item,0)
                Misc.Pause( dragDelay )
                
MoveToGround()
Misc.SendMessage( 'Wyrzucilem co trzeba', 31 )
