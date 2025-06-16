from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys


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
            Misc.Pause(2000)
            Player.UseSkill('Ukrywanie')
            Misc.Pause(36000)
        Journal.Clear()
        Misc.Pause(2000)
        Player.UseSkill('Okradanie')
        Target.WaitForTarget( 5000 , True )
        Target.TargetExecute(stealTarget)
    #if Timer.Check("stealTimer") == False:
    
     #   Timer.Create("stealTimer",14000)