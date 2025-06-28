from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys

musicId = 0x0E9E  #0x0E9E tamburyn 0x0EB1 duza harfa
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
        
def snoop(target):
    print("snoop func")
    Timer.Create("snoopWatchdog",60000)
    Journal.Clear()
    Player.UseSkill('Zagladanie')
    Target.WaitForTarget( 5000 , True )
    Target.TargetExecute(target)
    while True:
        Misc.Pause(200) #waiting
        if Timer.Check("snoopWatchdog") == False:
            Journal.Clear()
            print("snoop func ret watchdog FALSE")
            Misc.Pause(200)
            return False
        if Journal.Search('Oddaliles') or Journal.Search('za daleko') or Journal.Search('Nie widzisz'):
            Journal.Clear()
            Misc.Pause(3000)
            print("snoop func ret FALSE")
            return False
        if Journal.Search('Musisz chwile') or Journal.Search('You must') or Journal.Search('am already'):
            Misc.Pause(3000)
            Journal.Clear()
            Player.UseSkill('Zagladanie')
            Target.WaitForTarget( 5000 , True )
            Target.TargetExecute(target)
        if Journal.Search('Udalo Ci sie otworzyc') or Journal.Search('Juz podgladasz'):
            Journal.Clear('Udalo Ci sie otworzyc')
            Journal.Clear('Juz podgladasz')
            print('snoop func ret SUKCES')
            return True
        if Journal.Search('Nie udalo Ci sie otworzyc'):
            Journal.Clear('Nie udalo Ci sie otworzyc')
            print('snoop func ret FALSE')
            return False 
        
def steal(itemToSteal):
    print("steal func")
    Journal.Clear()
    Timer.Create("stealWatchdog",14000)
    Player.UseSkill('Okradanie')
    Target.WaitForTarget( 5000 , True )
    Target.TargetExecute(itemToSteal)
    while True:
        Misc.Pause(200)#waiting
        if Timer.Check("stealWatchdog") == False or Journal.Search("Tego nie da Ci"):
            return False
        if Journal.Search('You must') or Journal.Search('am already'):
            Misc.Pause(1000)
            Journal.Clear()
            Timer.Create("stealWatchdog",14000)
            return True
        if (Journal.Search("Udalo Ci sie ukrasc") or
            Journal.Search("Nie Udalo Ci sie ukrasc") or
            Journal.Search("Udalo Ci sie ukrasc") or 
            Journal.Search("Ujawniles sie")):
            Misc.Pause(5000)
            Journal.Clear()
            Timer.Create("stealWatchdog",14000)
            return True

            
stealTarget = Target.PromptTarget( 'Select whom to steal' )

while True:
    Misc.Pause(200)
    if snoop(stealTarget) == True:
        Misc.Pause(2000)
        while True:
            #talerz 0x09D7
            #wiadro 0x0FAB
            #topor 0x0F43
            item = Items.FindByID(0x0F43,0x0000,0x543C2CEA,False,False)
            if steal(item) == False:
                break
    Misc.Pause(2000)
    print("restart main loop")
    
sys.exit()
Player.UseSkill('Okradanie')
Target.WaitForTarget( 5000 , True )
Target.TargetExecute(stealTarget)
Journal.Clear()
while True:
    Misc.Pause(400)
    if Journal.Search("You must wait"):
        Journal.Clear()
        Misc.Pause(2000)
        Player.UseSkill('Okradanie')
        Target.WaitForTarget( 5000 , True )
        Target.TargetExecute(stealTarget)
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