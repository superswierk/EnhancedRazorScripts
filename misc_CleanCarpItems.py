import sys

#magazynier
magazynID = 0x51B09F1D
#workingBag = Target.PromptTarget( 'Wybierz pojemnik do pociecia rzeczy' )
sawId = 0x1035
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

saw = getByItemID(sawId, self_pack)
Items.UseItem(saw)
Target.WaitForTarget(2000, True)
Target.TargetExecute(magazynID)
