import tkinter as tk
from tkinter import messagebox, scrolledtext
import pyautogui
import pytesseract
from PIL import Image
import threading
import time

# 固定座標區域（依據 1920x1080 調整）
BASE_BOX = (665, 375, 200, 50)   # 基本價值
GOLD_BOX = (620, 630, 280, 60)   # 黃金價格

def ocr_number_from_box(box):
    image = pyautogui.screenshot(region=box)
    gray = image.convert('L')
    text = pytesseract.image_to_string(gray, config="--psm 7 -c tessedit_char_whitelist=0123456789,")
    digits = ''.join(filter(str.isdigit, text.replace(",", "")))
    return int(digits) if digits else None

def calculate_difference():
    base = ocr_number_from_box(BASE_BOX)
    gold = ocr_number_from_box(GOLD_BOX)
    if base is None or gold is None:
        messagebox.showerror("辨識失敗", "無法辨識數字，請確認畫面清晰")
        return
    diff = base - gold
    color = "green" if diff > 0 else "red"
    diff_label.config(text=f"差異：{diff:+,}", fg=color)
    log_area.insert(tk.END, f"基礎：{base:,}，黃金：{gold:,}，差異：{diff:+,}\n")
    log_area.see(tk.END)

def auto_loop():
    while running[0]:
        calculate_difference()
        time.sleep(3)

def start_loop():
    if not running[0]:
        running[0] = True
        threading.Thread(target=auto_loop, daemon=True).start()
        start_btn.config(state=tk.DISABLED)
        stop_btn.config(state=tk.NORMAL)

def stop_loop():
    running[0] = False
    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)

def clear_log():
    log_area.delete('1.0', tk.END)

# 主介面
root = tk.Tk()
root.title("即時價格差異顯示器 - 全螢幕版")
root.geometry("700x350")

diff_label = tk.Label(root, text="準備辨識中...", font=("Arial", 16))
diff_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

start_btn = tk.Button(button_frame, text="啟動偵測", font=("Arial", 12), command=start_loop)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(button_frame, text="停止偵測", font=("Arial", 12), state=tk.DISABLED, command=stop_loop)
stop_btn.grid(row=0, column=1, padx=5)

clear_btn = tk.Button(button_frame, text="清除日誌", font=("Arial", 12), command=clear_log)
clear_btn.grid(row=0, column=2, padx=5)

log_area = scrolledtext.ScrolledText(root, width=80, height=10, font=("Consolas", 10))
log_area.pack(padx=10, pady=10)

running = [False]

root.after(3000, start_loop)  # 啟動後 3 秒自動啟動
root.mainloop()
