import pyautogui as pgui
import time
import pyperclip
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'


def get_imgmsg(imgname):
    region = (380, 150, 500, 620)
    screenshot= pgui.screenshot(region=region)
    screenshot.save(imgname)

def PreprocessingImg(imgname):
    img = Image.open(imgname)
    gray_img=img.convert('L')
    threshold = 128
    binary_img = gray_img.point(lambda p: p > threshold and 255)
    binary_img.save(imgname)

def getTextFromImg(imgname)->str:
    # 加载图像
    img = Image.open(imgname)
    img.show()
    # 使用 Tesseract 进行 OCR 识别
    text = pytesseract.image_to_string(img,lang='chi_sim')

    # 打印识别到的文本
    return text

def getmouseposition():
    time.sleep(4)
    print(pgui.position())
    #exit()

def initprompt():
    print("把微信框放在左上 并到左上框里 不要遮挡\n")
    for i in range(1,15):
        print(f"after {i} sec will START" ,end='\r')
        time.sleep(1)

def getContentFromMyChat()-> str:
    pgui.moveTo(130,65)#serch bar
    pgui.click()
    content="文件传输助手"
    pyperclip.copy(content)
    pgui.hotkey('command','v')
    pgui.typewrite("\n")
    pgui.moveTo(600,900)#text box
    pgui.rightClick()
    pgui.moveTo(1380,757)
    pgui.click()
    return pyperclip.paste()
    

def doGrupBroadcast():
    initprompt()

    #set time pause
    pgui.PAUSE=1
    #content set
    content=getContentFromMyChat()
    serch_part="BO grp"
    ran = 10
    #action
    ran= ran+1
    for num in range(1,ran):
        pgui.moveTo(116,65)#serch bar
        pgui.click()
        serch=f"{serch_part} {num}"
        pgui.typewrite(serch)
        pgui.typewrite("\n")
        pgui.moveTo(400,500)
        pgui.click()
        pyperclip.copy(content)
        pgui.hotkey('command','v')

def parse_img():
    imgname="temp.png"
    get_imgmsg(imgname)
    PreprocessingImg(imgname)
    text=getTextFromImg(imgname)
    print(text)

doGrupBroadcast()
#getmouseposition()
#parse_img()
#then conn to llm to get complete and good format text
