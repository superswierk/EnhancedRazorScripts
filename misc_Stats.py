from Scripts.EnhancedRazorScripts.misc_Discord import *
import sys
Round = lambda x, n: eval('"%.'+str(int(n))+'f" % '+repr(int(x)+round(float('.'+str(float(x)).split('.')[1]),n)))
lumberThumb = "https://i.imgur.com/FAb0xg0.png"
deadThumb = "https://i.imgur.com/QjVeOoA.png"
foodThumb = "https://i.imgur.com/uB0tTVj.png"
enemyThumb = "https://i.imgur.com/YvbQw56.png"
lvlupThumb = "https://i.imgur.com/j5rUy80.png"
apoThumb = "https://i.imgur.com/eDQLGaI.png"

skillName =  'Druciarstwo'

Journal.Clear()
lvlStealSkill = Player.GetRealSkillValue(skillName)
lvlStealSkillNew = Player.GetRealSkillValue(skillName)
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
    Misc.Pause(2000)
    if apocalipse == False and Journal.Search('Apokalipsa'):
        apokalipseStr = Journal.GetLineText('Apokalipsa')
        apocalipse = True
        sendDiscord("Uwaga:\n" + apokalipseStr + "\n", 14696255, apoThumb)
    lvlStealSkillNew = Player.GetRealSkillValue(skillName)
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