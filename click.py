from evdev import InputDevice, categorize, ecodes, list_devices
import select
import json
from datetime import datetime

log = []
last_click_time = None
mouse_x = 0
mouse_y = 0

def record_click(x, y, button):
    global last_click_time
    current_time = datetime.now()
    if last_click_time is None:
        time_diff = 0
    else:
        time_diff = (current_time - last_click_time).total_seconds()
    last_click_time = current_time
    entry = {
        "time": time_diff,
        "x": x,
        "y": y,
        "button": button
    }
    log.append(entry)
    print(f"[距上次 {time_diff:.2f}秒] {button} → ({x}, {y})")

# 找到所有輸入設備
devices = [InputDevice(path) for path in list_devices()]
if not devices:
    print("找不到輸入設備，請確認 /dev/input 中有事件設備（需 root 權限）")
    exit(1)

print("開始記錄，按 Esc 結束...")

try:
    while True:
        r, _, _ = select.select(devices, [], [], 1)
        for device in r:
            for event in device.read():
                if event.type == ecodes.EV_KEY:
                    # Esc 停止
                    if event.code == ecodes.KEY_ESC and event.value == 1:
                        raise KeyboardInterrupt()
                    # 滑鼠按鍵
                    if event.value == 1:
                        if event.code == ecodes.BTN_LEFT:
                            record_click(mouse_x, mouse_y, "Button.left")
                        elif event.code == ecodes.BTN_RIGHT:
                            record_click(mouse_x, mouse_y, "Button.right")
                        elif event.code == ecodes.BTN_MIDDLE:
                            record_click(mouse_x, mouse_y, "Button.middle")
                # 滑鼠相對移動
                elif event.type == ecodes.EV_REL:
                    if event.code == ecodes.REL_X:
                        mouse_x += event.value
                    elif event.code == ecodes.REL_Y:
                        mouse_y += event.value
                    elif event.code == ecodes.REL_WHEEL:
                        print(f"滾輪：({mouse_x}, {mouse_y}) 方向={event.value}")
except KeyboardInterrupt:
    pass
finally:
    for device in devices:
        try:
            device.close()
        except:
            pass

# 儲存結果
with open("mouse_log.json", "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)

print(f"\n共記錄 {len(log)} 次點擊，已儲存至 mouse_log.json")
