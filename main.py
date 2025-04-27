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
    "pic/serch_bar.png",
    "pic/textarea.png",
    "pic/fileasis.png"
]

screenshotname="screenshot.png"

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
    for template in template_list:
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
        template = cv2.imread(template_name)
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
        results[template_name] = found_positions

    # 3. 显示带框的匹配图像
    cv2.imshow("Matched Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return results

def getContentFromMyChat():
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

def init():
    initprompt()
    PreprocessAllTemplate()
    screenshot()
    locations_dict=locate()
    print(locations_dict)   




init()
#getmouseposition()
#doGrupBroadcast()
#then conn to llm to get complete and good format text
