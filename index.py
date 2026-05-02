from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener as KbListener

import json
import time

mouse = Controller()
stop_flag = False

# 讀取 log
with open("mouse_log.json", "r", encoding="utf-8") as f:
    log = json.load(f)

count = 90

def on_key(key):
    global stop_flag
    try:
        if key == Key.esc:
            stop_flag = True
    except AttributeError:
        pass

print("3 秒後開始重播...")
time.sleep(3)

listener = KbListener(on_press=on_key)
listener.start()

for n in range(count):  
    for i, entry in enumerate(log):
        # 移動到點擊位置
        mouse.position = (entry["x"], entry["y"])        
        # 判斷按鍵
        if "left" in entry["button"]:
            time.sleep(0.1)
            mouse.press(Button.left)
            time.sleep(0.1)
            mouse.release(Button.left)
        elif "right" in entry["button"]:
            time.sleep(0.1)
            mouse.press(Button.right)
            time.sleep(0.1)
            mouse.release(Button.right)
        time.sleep(entry["time"])
        if stop_flag:
            break
    if stop_flag:
        break
    print(f"{n+1}/{count} 次重播完成")

listener.stop()
print("重播完成！")