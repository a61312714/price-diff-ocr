import pyautogui
import pytesseract
import tkinter as tk
from tkinter import messagebox
import threading
import time
from PIL import Image

# 內建預設辨識範圍大小
REGION_WIDTH = 200
REGION_HEIGHT = 60

# 儲存座標
coords = {}

def get_position(label):
    messagebox.showinfo("請準備", f"請將滑鼠移到【{label}】的位置，3 秒後會自動抓取座標")
    time.sleep(3)
    x, y = pyautogui.position()
    coords[label] = (x, y, REGION_WIDTH, REGION_HEIGHT)

def get_price(region):
    try:
        screenshot = pyautogui.screenshot(region=region)
        text = pytesseract.image_to_string(screenshot, config='--psm 7').strip()
        text = text.replace(',', '').replace(' ', '')
        return int(''.join(filter(str.isdigit, text)))
    except:
        return None

def update_loop():
    while True:
        base = get_price(coords["基本價值"])
        gold = get_price(coords["黃金價格"])
        if base is not None and gold is not None:
            diff = gold - base
            color = "green" if diff <= 0 else "red"
            result_var.set(f"黃金價格：{gold} 元\n基本價值：{base} 元\n差值：{diff:+}")
            result_label.config(fg=color)
        else:
            result_var.set("無法辨識數字，請確認畫面清晰")
            result_label.config(fg="black")
        time.sleep(1)

# 主視窗
root = tk.Tk()
root.title("即時價格差異顯示器")
root.geometry("400x200")

result_var = tk.StringVar(value="準備中...")

result_label = tk.Label(root, textvariable=result_var, font=("Arial", 14), wraplength=380, justify="center")
result_label.pack(pady=30)

# 啟動流程
def start_monitor():
    threading.Thread(target=lambda: (
        get_position("基本價值"),
        get_position("黃金價格"),
        update_loop()
    )).start()

root.after(100, start_monitor)
root.mainloop()
