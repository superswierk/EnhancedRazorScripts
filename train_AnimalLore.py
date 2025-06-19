animalLoreTimerMilliseconds = 8000

# Select what to run Animal Lore on
animalLoreTarget = Target.PromptTarget( 'Select animal to train on' )
Mobiles.Message( animalLoreTarget, 52, 'Selected for animal lore training' )

def TrainAnimalLore():
    '''
    Trains Animal Lore with the selected target
    '''
    global animalLoreTarget

    Timer.Create( 'animalLoreTimer', 1 )
    targetStillExists = Mobiles.FindBySerial( animalLoreTarget )

    while targetStillExists != None and not Player.IsGhost:
        if not Timer.Check( 'animalLoreTimer' ):
            Player.UseSkill( 'Wiedza o Zwierzetach' )
            Target.WaitForTarget( 2000, True )
            Target.TargetExecute( animalLoreTarget )
            Timer.Create( 'animalLoreTimer', animalLoreTimerMilliseconds )

    if targetStillExists == None:
        Player.HeadMessage( 55, 'Selected target for animal lore is gone' )

# Start Training
TrainAnimalLore()