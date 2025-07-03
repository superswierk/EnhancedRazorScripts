from Scripts.EnhancedRazorScripts.misc_Discord import *
from System.Collections.Generic import List
from System import Byte, Int32, Double
import sys
Round = lambda x, n: eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n)))
lumberThumb = "https://i.imgur.com/FAb0xg0.png"
deadThumb = "https://i.imgur.com/QjVeOoA.png"
foodThumb = "https://i.imgur.com/uB0tTVj.png"
enemyThumb = "https://i.imgur.com/YvbQw56.png"
lvlupThumb = "https://i.imgur.com/j5rUy80.png"
apoThumb = "https://i.imgur.com/eDQLGaI.png"

setX = 125 
setY = 125
offsetLabelY = 20
offsetRadioY = 45
offsetButtonY = 170

STATICSKILLS = {
    "Druciarstwo": 11,
    "Stolarstwo": 12,
    "Okaradanie": 13,
    "Zagladanie": 14,
    "Gornictwo": 15,
    "Wlamywanie": 16,
    "Drwalstwo": 17,
    "Tworzenie Lukow": 18,
    "Rolnictwo": 19,
    "Zakradanie": 20,
    "Ukrywanie": 21
}



def sendgump():
    gd = Gumps.CreateGump(movable=True) 
    
    Gumps.AddPage(gd, 0)
    Gumps.AddBackground(gd, 0, 0, 200, (STATICSKILLS.Count + 3) * 20 + offsetRadioY, 2620) 

    iY = 0
    Gumps.AddLabel(gd,15,iY + offsetLabelY,2407,'Wybierz skill do sledzenia:')
    
    defaultSelected = STATICSKILLS[list(STATICSKILLS.keys())[0]]
    print(defaultSelected)
    if Misc.CheckSharedValue("misc_StatsState") == True:
        defaultSelected = Misc.ReadSharedValue("misc_StatsState")
    
    for skill in STATICSKILLS:
        defultValue = False
        if STATICSKILLS[skill] == defaultSelected:
            defultValue = True
        Gumps.AddRadio(gd,15,iY + offsetRadioY,209,208,defultValue,STATICSKILLS[skill])
        Gumps.AddLabel(gd,35,iY + offsetRadioY,2407,skill)
        iY = iY + 20
    
    iY = iY + 20
    Gumps.AddButton(gd,120,iY + offsetRadioY,247,248,456,1,0)

    Gumps.SendGump(696969, Player.Serial, setX, setY, gd.gumpDefinition, gd.gumpStrings)
    buttoncheck()



def buttoncheck():
    global skillName
    Gumps.WaitForGump(696969, 60000)
    Gumps.CloseGump(696969)
    gdata = Gumps.GetGumpData(696969)
    switchList = gdata.switches
    if switchList.Count >= 1:
        Misc.SetSharedValue("misc_StatsState",switchList[0])
        for skill in STATICSKILLS:   
            if switchList[0] == STATICSKILLS[skill]:
                skillName =  skill
                print(f"{skill}")
        if skillName is None:
            skillName = 'Druciarstwo'
            print("Default value " + skillName)
    else:
        print("error nie zaznaczyles nic uzwyam domyslnego " + skillName)

skillName = 'Druciarstwo'
sendgump()
Misc.Pause(2000)

Journal.Clear()
lvlStealSkill = float(Player.GetRealSkillValue(skillName))
lvlStealSkillNew = float(Player.GetRealSkillValue(skillName))
Player.ChatSay('.glod wszystko')
Misc.Pause(3000)
glod = Journal.GetLineText('Glod')
bialka = Journal.GetLineText('Bialka')
witaminy = Journal.GetLineText('Witaminy')
weglowodany = Journal.GetLineText('Weglowodany')
newGlod = Journal.GetLineText('Glod')
newBialka = Journal.GetLineText('Bialka')
newWitaminy = Journal.GetLineText('Witaminy')
newWeglowodany = Journal.GetLineText('Weglowodany')
Timer.Create('eatingLogTimer', 120000)
apocalipse = False
while True:
    Misc.Pause(1000)
    if Player.IsGhost == True:
        sendDiscord("Postac umarla!", 15291726, deadThumb);
        Misc.Pause(2000)
        sys.exit()
    if apocalipse == False and Journal.Search('Apokalipsa'):
        apokalipseStr = Journal.GetLineText('Apokalipsa')
        apocalipse = True
        sendDiscord("Uwaga:\n" + apokalipseStr + "\n", 14696255, apoThumb)
    lvlStealSkillNew = float(Player.GetRealSkillValue(skillName))
    if lvlStealSkillNew > float(70) or int(lvlStealSkillNew) == lvlStealSkillNew:
        if lvlStealSkill != lvlStealSkillNew:
            lvlStealSkill = lvlStealSkillNew
            sendDiscord("Wzrost umiejetnosci " + skillName + " masz teraz: " + str(Round(lvlStealSkill,1)), 5814783, lvlupThumb)
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