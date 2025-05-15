import sys

bloodBandages = 0x0E20
water = Target.PromptGroundTarget( 'Wybierz pojemnik z woda' )
self_pack = Player.Backpack.Serial

# Helper Functions
###################################
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
###################################
bandage = getByItemID(bloodBandages, self_pack)
Journal.Clear()
while (bandage is not None ) and (not Journal.Search( 'nie umyjesz' )) and ( not Journal.Search( 'nie wyleczysz')):
    Misc.SendMessage('Myje bandaze',55)
    Items.UseItem(bandage)
    Target.WaitForTarget(2000, True)
    Target.TargetExecute(water.X,water.Y,water.Z)
    Misc.Pause(1000)
    if Journal.Search( 'nie umyjesz' ) or Journal.Search( 'nie wyleczysz' ):
        break
    Misc.Pause(3000)
    bandage = getByItemID(bloodBandages, self_pack)
Misc.Pause(200)  
Misc.SendMessage('Koniec mycia',55)
