from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys
Round = lambda x, n: eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n)))
lumberThumb = "https://i.imgur.com/FAb0xg0.png"
deadThumb = "https://i.imgur.com/QjVeOoA.png"
foodThumb = "https://i.imgur.com/uB0tTVj.png"
enemyThumb = "https://i.imgur.com/YvbQw56.png"
lvlupThumb = "https://i.imgur.com/j5rUy80.png"
apoThumb = "https://i.imgur.com/eDQLGaI.png"
lvlCarpSkill = Round(Player.GetRealSkillValue('Zagladanie'),1)

musicId = 0x0E9E
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


def playMusic():
    global musicId
    global self_pack
    playItem = getByItemID(musicId, Player.Backpack.Serial)
    if Timer.Check('musicTimer') == False:
        Misc.Pause(400)
        Timer.Create('musicTimer',10000)
        if playItem is not None:
            Items.UseItem(playItem)
            print('Gram muzyke!')
            Misc.Pause(4000)
        else:
            print('nie gram muzyki cos nie tak!')
            
def hide():
    if  Player.BuffsExist('Ukrywanie') == False and Timer.Check('hideTimer') == False:
        Misc.Pause( 700 )
        Player.UseSkill('Ukrywanie')
        Timer.Create('hideTimer',12000)
        print('Ukrywam sie!')
        Misc.Pause( 4000 )

def PlayerWalk( direction ):
    '''
    Moves the player in the specified direction
    '''

    playerPosition = Player.Position
    if Player.Direction == direction:
        Player.Walk( direction )
    else:
        Player.Walk( direction )
        Player.Walk( direction )
    return

def FollowMobile( mobile, maxDistanceToMobile = 2, startPlayerStuckTimer = False ):
    '''
    Uses the X and Y coordinates of the animal and player to follow the animal around the map
    Returns True if player is not stuck, False if player is stuck
    '''

    mobilePosition = mobile.Position
    playerPosition = Player.Position
    directionToWalk = ''
    if mobilePosition.X > playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'Down'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'Left'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'Right'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'Up'
    if mobilePosition.X > playerPosition.X and mobilePosition.Y == playerPosition.Y:
        directionToWalk = 'East'
    if mobilePosition.X < playerPosition.X and mobilePosition.Y == playerPosition.Y:
        directionToWalk = 'West'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y > playerPosition.Y:
        directionToWalk = 'South'
    if mobilePosition.X == playerPosition.X and mobilePosition.Y < playerPosition.Y:
        directionToWalk = 'North'

    if startPlayerStuckTimer:
        Timer.Create( 'playerStuckTimer', 5000 )

    playerPosition = Player.Position
    PlayerWalk( directionToWalk )

    newPlayerPosition = Player.Position
    if playerPosition == newPlayerPosition and not Timer.Check( 'playerStuckTimer' ):
        # Player has been stuck in the same position for a while, try to find them a way out of the stuck position
        return False
        if Player.Direction == 'Up':
            for i in range ( 5 ):
                Player.Walk( 'Down' )
        elif Player.Direction == 'Down':
            for i in range( 5 ):
                Player.Walk( 'Up' )
        elif Player.Direction == 'Right':
            for i in range( 5 ):
                Player.Walk( 'Left' )
        elif Player.Direction == 'Left':
            for i in range( 5 ):
                Player.Walk( 'Right' )
        Timer.Create( 'playerStuckTimer', 5000 )
    elif playerPosition != newPlayerPosition:
        Timer.Create( 'playerStuckTimer', 5000 )

    if Player.DistanceTo( mobile ) > maxDistanceToMobile:
        # This pause may need further tuning
        # Don't want to create a ton of infinite calls if the player is stuck, but also don't want to not be able to catch up to animals
        Misc.Pause( 100 )
        FollowMobile( mobile, maxDistanceToMobile )
    return True

snoopTarget = Target.PromptTarget( 'Select whom to snoop' )

goToItem = Items.FindBySerial(0x53C8FE96)

def snoop(target):
    Journal.Clear()
    Player.UseSkill('Zagladanie')
    Target.WaitForTarget( 5000 , True )
    Target.TargetExecute(target)
    while True:
        Misc.Pause(200) #waiting
        if Journal.Search('Oddaliles') or Journal.Search('za daleko'):
            Journal.Clear()
            Misc.Pause(3000)
            return False
        if Journal.Search('Musisz chwile') or Journal.Search('Juz podgladasz') or Journal.Search('You must'):
            Misc.Pause(3000)
            Journal.Clear()
            Player.UseSkill('Zagladanie')
            Target.WaitForTarget( 5000 , True )
            Target.TargetExecute(target)
        if Journal.Search('Udalo Ci sie otworzyc'):
            Journal.Clear('Udalo Ci sie otworzyc')
            print('koniec zagladania SUKCES')
            return True
        if Journal.Search('Nie udalo Ci sie otworzyc'):
            Journal.Clear('Nie udalo Ci sie otworzyc')
            print('koniec zagladania FAIL')
            return False 

Journal.Clear()
lvlCarpSkill = Player.GetRealSkillValue('Zagladanie')
lvlCarpSkillNew = Player.GetRealSkillValue('Zagladanie')
Player.ChatSay('.glod wszystko')
Misc.Pause(1000)
glod = Journal.GetLineText('Glod')
bialka = Journal.GetLineText('Bialka')
witaminy = Journal.GetLineText('Witaminy')
weglowodany = Journal.GetLineText('Weglowodany')
newGlod = Journal.GetLineText('Glod')
newBialka = Journal.GetLineText('Bialka')
newWitaminy = Journal.GetLineText('Witaminy')
newWeglowodany = Journal.GetLineText('Weglowodany')
Timer.Create('eatingLogTimer', 120000)
Timer.Create('snoopDelay',1000)
apocalipse = False
while True:
    if apocalipse == False and Journal.Search('Apokalipsa'):
        apokalipseStr = Journal.GetLineText('Apokalipsa')
        apocalipse = True
        sendDiscord("Uwaga:\n" + apokalipseStr + "\n", 14696255, apoThumb)
    playMusic()
    lvlCarpSkillNew = Player.GetRealSkillValue('Zagladanie')
    if lvlCarpSkill != lvlCarpSkillNew:
        lvlCarpSkill = lvlCarpSkillNew
        sendDiscord("Wzrost umiejetnosci Zagladanie masz teraz: " + str(Round(lvlCarpSkill,1)), 5814783, lvlupThumb)
    if(Timer.Check('eatingLogTimer') == False):
        Timer.Create('eatingLogTimer', 120000)
        Player.ChatSay('.glod wszystko')
        Misc.Pause(3000)
        newGlod = Journal.GetLineText('Glod')
        newBialka = Journal.GetLineText('Bialka')
        newWitaminy = Journal.GetLineText('Witaminy')
        newWeglowodany = Journal.GetLineText('Weglowodany')
        if newGlod != glod or newBialka != bialka or newWitaminy != witaminy or newWeglowodany != weglowodany :
            glod = newGlod
            bialka = newBialka
            witaminy = newWitaminy
            weglowodany = newWeglowodany
            sendDiscord("Status glodu:\n" + glod + "\n" + bialka + "\n" + witaminy + "\n" + weglowodany + "\n",2012169, foodThumb)

    snoopTargetGo = Mobiles.FindBySerial( snoopTarget )
    if Player.DistanceTo( snoopTargetGo ) > 1:
        FollowMobile( snoopTargetGo, 1, True )
    
    if Timer.Check('snoopDelay') == False:
        if snoop(snoopTargetGo) == True:
            hide()
            Timer.Create('snoopDelay',21000)
            
            if Player.DistanceTo( goToItem ) > 1:
                FollowMobile( goToItem, 1, True )
        else:
            Timer.Create('snoopDelay',2000)
