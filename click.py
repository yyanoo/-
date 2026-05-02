from pynput import mouse
from datetime import datetime
import json

log = []
last_click_time = None

def on_click(x, y, button, pressed):
    global last_click_time
    if pressed:
        current_time = datetime.now()
        
        if last_click_time is None:
            # 第一次點擊
            time_diff = 0
        else:
            # 計算距上次點擊的時間差
            time_diff = (current_time - last_click_time).total_seconds()
        
        last_click_time = current_time
        
        entry = {
            "time": time_diff,
            "x": x,
            "y": y,
            "button": str(button)
        }
        log.append(entry)
        print(f"[距上次 {time_diff:.2f}秒] {button} → ({x}, {y})")

def on_scroll(x, y, dx, dy):
    print(f"滾輪：({x}, {y}) 方向=({dx}, {dy})")

print("開始記錄，按 Esc 結束...")

with mouse.Listener(on_click=on_click, on_scroll=on_scroll) as listener:
    from pynput.keyboard import Key, Listener as KbListener

    def on_key(key):
        if key == Key.esc:
            listener.stop()
            return False

    with KbListener(on_press=on_key) as kb:
        kb.join()

# 儲存結果
with open("mouse_log.json", "w", encoding="utf-8") as f:
    json.dump(log, f, ensure_ascii=False, indent=2)

print(f"\n共記錄 {len(log)} 次點擊，已儲存至 mouse_log.json")