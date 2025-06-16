from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys

musicId = 0x0E9E
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


def playMusic():
    global musicId
    playItem = getByItemID(musicId, Player.Backpack.Serial)
    Misc.Pause(400)
    if playItem is not None:
        Items.UseItem(playItem)
        print('Gram muzyke!')
    else:
        print('nie gram muzyki cos nie tak!')
        

stealTarget = Target.PromptTarget( 'Select whom to steal' )

Player.UseSkill('Okradanie')
Target.WaitForTarget( 5000 , True )
Target.TargetExecute(stealTarget)
Journal.Clear()
while True:
    Misc.Pause(400)
    if (Journal.Search("Nie udalo Ci sie okrasc") or
       Journal.Search("Udalo Ci sie ukrasc") or
       Journal.Search("Ujawniles sie") or 
       Journal.Search("Za szybko")):
        if Journal.Search("Udalo Ci sie ukrasc") or Journal.Search("Za szybko"):
            Misc.Pause(4000)
            Player.UseSkill('Ukrywanie')
            Misc.Pause(4000)
            playMusic()
            Misc.Pause(12000)
            Player.UseSkill('Ukrywanie')
            Misc.Pause(4000)
            playMusic()
            Misc.Pause(12000)
            Player.UseSkill('Ukrywanie')
            Misc.Pause(4000)
            playMusic()
            Misc.Pause(12000)
            Player.UseSkill('Ukrywanie')
            Misc.Pause(8000)
        Journal.Clear()
        Misc.Pause(2000)
        Player.UseSkill('Okradanie')
        Target.WaitForTarget( 5000 , True )
        Target.TargetExecute(stealTarget)
    #if Timer.Check("stealTimer") == False:
    
     #   Timer.Create("stealTimer",14000)