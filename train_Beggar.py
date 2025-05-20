import sys

person = None
def MoveToMob():
    global person
    person = Target.GetTargetFromList('beggar') 
    if person is None:
        Misc.SendMessage('Nie znalazlo nikog',53)
        sys.exit()
    mobPerson = Mobiles.FindBySerial( person.Serial )
    Misc.SendMessage('to jest cel: %s' % (mobPerson),53)
    treeCoords = PathFinding.Route()
    treeCoords.MaxRetry = 5
    treeCoords.StopIfStuck = False
    treeCoords.X = mobPerson.Position.X
    treeCoords.Y = mobPerson.Position.Y + 1

    if PathFinding.Go( treeCoords ):
        Misc.SendMessage('First Try')
        Misc.Pause( 1000 )
    else:
        Misc.Resync()
        treeCoords.X = mobPerson.Position.X + 1
        treeCoords.Y = mobPerson.Position.Y
        if PathFinding.Go( treeCoords ):
            Misc.SendMessage( 'Second Try' )
        else:
            treeCoords.X = mobPerson.Position.X - 1
            treeCoords.Y = mobPerson.Position.Y
            if PathFinding.Go( treeCoords ):
                Misc.SendMessage( 'Third Try' )
            else:
                treeCoords.X = mobPerson.Position.X
                treeCoords.Y = mobPerson.Position.Y - 1
                Misc.SendMessage( 'Final Try' )
                if PathFinding.Go( treeCoords ):
                    Misc.NoOperation()
                else:
                    return False
    Misc.SendMessage( '--> Dotarlem', 77 )
    Misc.Resync()
    return True

while True:
    if MoveToMob() == True:
        Timer.Create('beggingTimer', 60000)
        while True:
            Journal.Clear()
            Player.UseSkill('Zebranie')
            Target.WaitForTarget( 2000, True )
            Target.TargetExecute( person.Serial )
            Misc.Pause(8200)
            if Timer.Check('beggingTimer') == False:
                Friend.AddPlayer('ignorelist',person.Name,person.Serial)
                Misc.SendMessage( '--> Ide dalej', 77 )
                break
    else:
        Friend.AddPlayer('ignorelist',person.Name,person.Serial)
        Misc.SendMessage( '--> Nie ma dojscia next!!!', 77 )
        

