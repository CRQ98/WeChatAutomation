import pyautogui as pgui
import time
import pyperclip
import pytesseract
import cv2
import numpy as np
from PIL import Image
import cv2
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

template_list = [
    "serchbar",
    "textarea",
    "copy",
    "coner"
]
template_paths = ["pic/" + template + ".png" for template in template_list]
screenshotname="pic/screenshot.png"
locations_dict={}
#set time pause
pgui.PAUSE=0.6

def initprompt():
    print("最大化微信 置顶 不要遮挡 6秒后开始\n")
    for i in range(1,7):
        print(f"after {i} sec will START" ,end='\r')
        time.sleep(1)

def PreprocessingImg(imgname):
    img = Image.open(imgname)
    gray_img=img.convert('L')
    threshold = 128
    binary_img = gray_img.point(lambda p: p > threshold and 255)
    binary_img.save(imgname, icc_profile=None)

def PreprocessAllTemplate():
    for template in template_paths:

        PreprocessingImg(template)

def getTextFromImg(imgname):
    # 加载图像
    img = Image.open(imgname)
    PreprocessingImg(imgname)
    # 使用 Tesseract 进行 OCR 识别
    text = pytesseract.image_to_string(img,lang='chi_sim')
    # 打印识别到的文本
    return text

def getmouseposition():
    print(pgui.position())

def screenshot():
    screenshot = pgui.screenshot()
    screenshot.save(screenshotname)
    PreprocessingImg(screenshotname)

def locate():
    # 1. 读取截图
    screenshot()
    image = cv2.imread(screenshotname)  # 大图

    # 计算缩放比例
    screen_width, screen_height = pgui.size()
    img_height, img_width = image.shape[:2]
    scale_x = screen_width / img_width
    scale_y = screen_height / img_height

    # 结果字典
    results = {}
    
    threshold = 0.9 
    # 2. 定位每一个 template
    for template_name in template_list:
        template_path=f"pic/{template_name}.png"
        template = cv2.imread(template_path)
        if template is None:
            print(f"警告: 模板 {template_name} 加载失败，跳过。")
            continue
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)

        found_positions = []
        for pt in zip(*locations[::-1]):
            # 计算中心点
            target_x = pt[0] + template.shape[1] // 2
            target_y = pt[1] + template.shape[0] // 2

            # 缩放到屏幕尺寸
            real_x = int(target_x * scale_x)
            real_y = int(target_y * scale_y)

            found_positions.append((real_x, real_y))

            # 画矩形确认 (注意：要用原图尺寸)
            cv2.rectangle(image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 1)
            cv2.putText(image, template_name, (pt[0], pt[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        # 把所有找到的位置记录下来
        locations_dict[template_name] = found_positions

    # 3. 显示带框的匹配图像
    if 0:
        cv2.imshow("Matched Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        time.sleep(2)

def get_location(name):
    x,y=locations_dict[name][0]
    return x,y

def copy(content):
    pyperclip.copy(content)
def paste():
    pgui.click()
    pgui.hotkey('command','v')
def insert(content):
    copy(content)
    paste()

def getContentFromMyChat():
    pgui.moveTo(get_location("serchbar"))
    insert('文件传输助手')
    pgui.typewrite("\n")
    pgui.moveTo(1381,757)#text box
    pgui.rightClick()
    locate()
    time.sleep(2)
    pgui.moveTo(get_location("copy"))
    pgui.click()
    return pyperclip.paste()

def GrupBroadcast(serch_part,length):

    #content set
    content=getContentFromMyChat()

    #action
    for num in range(1,length+1):
        pgui.moveTo(get_location("serchbar"))
        pgui.click()
        serchtext=f"{serch_part} {num}"
        if num<10:
            serchtext=f"{serch_part} 0{num}"
        insert(serchtext)
        pgui.typewrite("\n")
        pgui.moveTo(get_location("textarea"))
        pgui.click()
        insert(content)

def init():
    initprompt()
    PreprocessAllTemplate()
    locate()

serch_part="BO grp"
length = 3
time.sleep(4)
screenshot = pgui.screenshot()
screenshot.save(screenshotname)
conerimg="pic/coner.png"
mean_brightness = np.mean(screenshot)
image=cv2.imread(screenshotname)

if mean_brightness<180:
    adjusted_image = cv2.convertScaleAbs(image, alpha=5, beta=0)
    gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
    cv2.imwrite(binary_img,screenshotname)
else:
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray_image, 250, 255, cv2.THRESH_BINARY)
    cv2.imshow('Original Image', image)
    cv2.imshow('gray_image',gray_image)
    cv2.imshow('binary_img',binary_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if 0:
    init()
    GrupBroadcast(serch_part,length)


#time.sleep(4)
#getmouseposition()

#then conn to llm to get complete and good format text
