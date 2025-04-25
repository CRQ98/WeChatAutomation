import pyautogui as pgui
import os
import time
import pyperclip


def getmouseposition():
    time.sleep(3)
    print(pgui.position())
    exit()

def initprompt():
    print("把微信框放在左上 并到左上框里")
    for i in range(1,15):
        print(f"after {i} sec will START" ,end='\r')
        time.sleep(1)

def doGrupBroadcast():
    initprompt()

    #set time pause
    pgui.PAUSE=1
    #content set
    content="你好"
    serch_part="BO grp"
    ran = 20
    #action
    ran= ran+1
    for num in range(1,ran):
        pgui.moveTo(116,65)
        pgui.click()
        serch=f"{serch_part} {num}"
        pgui.typewrite(serch)
        pgui.typewrite("\n")
        pgui.moveTo(400,500)
        pgui.click()
        pyperclip.copy(content)
        pgui.hotkey('command','v')


doGrupBroadcast()
getmouseposition()