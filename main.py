import os
import cv2
import time
import pygame
import requests
import threading
import webbrowser
import numpy as np
import tkinter as tk
from tkinter import filedialog
pygame.init()

i = 45
e = 25
cap = cv2.VideoCapture(0)  # Change this number to switch cameras (Default: 0)
audio_playing = False
start_time = None
prev_frame = None
sound_enabled = True 

token = 'your-bot-token' # Change to your telegram bot token
chat_id = 'your-chat-id' # Change to the chatid of the group you created
alarm_sound = pygame.mixer.Sound('alarm.mp3')
output_folder = 'images_alarm'

def telegram_bot_images():
    global output_folder, chat_id, token, latest_captured_image

    if latest_captured_image:
        rute_image = os.path.join(output_folder, latest_captured_image)
        with open(rute_image, 'rb') as img_file:
            requests.post('https://api.telegram.org/bot'+token+'/sendPhoto', data={'chat_id': chat_id}, files={'photo': img_file})


def telegram_bot_msg():
    global chat_id, token

    msg = "Movement Alarm Detection!!!"

    response = requests.post('https://api.telegram.org/bot'+token+'/sendMessage', data={'chat_id': chat_id, 'text': msg})
    if response.status_code == 200:
        print('Mensaje enviado exitosamente.')
    else:
        print('Error al enviar el mensaje. Código de estado:', response.status_code)
        print('Response:', response.text)

    
def set_output_folder():
    global output_folder
    output_folder = filedialog.askdirectory()
    if output_folder:
        label_output_folder.config(text=f'Output images folder: {output_folder}')

def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    if sound_enabled:
        label_sound_status.config(text='Alarm: Enabled')
    else:
        label_sound_status.config(text='Alarm: Disabled')

def capture_image():
    global output_folder, cap, latest_captured_image

    if output_folder:
        ret, frame = cap.read()
        if ret:
            timestamp = time.strftime("%Y_m%m_d%d_h%H_min%M_s%S")
            filename = f"capture_{timestamp}.jpg"
            latest_captured_image = filename 
            full_filename = os.path.join(output_folder, filename)
            cv2.imwrite(full_filename, frame)
            label_capture_status.config(text=f'Image captured: {full_filename}')
        else:
            label_capture_status.config(text='Error capturing image')
        telegram_bot_images()
        os.remove(full_filename)


def start_detection():
    global audio_playing, start_time, cap, prev_frame, sound_enabled, i, e
    while True:
        time.sleep(0.1)
        i += 1
        e += 1
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray_blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        if prev_frame is not None:
            frame_diff = cv2.absdiff(gray_blurred, prev_frame)

            _, thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)

            motion_pixels = np.sum(thresh) // 255

            if motion_pixels > 100:  # The larger this number is, the less sensitive the detector is, change it if you have problems with false positives
                if e >= 30:
                    threading.Thread(target=lambda: telegram_bot_msg(), daemon=True).start()
                    e = 0

                if i >= 50:
                    capture_image()
                    i = 0

                if sound_enabled and not audio_playing:
                    audio_playing = True
                    alarm_sound.play()
            else:
                

                if audio_playing:
                    alarm_sound.stop()
                    audio_playing = False


        prev_frame = gray_blurred

        cv2.imshow('Motion Detection (Press Esc to Close) - By GUCHI', frame)
        k = cv2.waitKey(10)
        if k == 27:
            break
    
    audio_playing = False
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    root.quit()

def open_link(event):
    webbrowser.open("https://github.com/GUCHIHACKER/Movement_detector_telegram")

root = tk.Tk()
root.title("Motion Detection and Capture - By GUCHI")
root.geometry("600x300")
icon_path = 'icon.ico'
root.iconbitmap(default=icon_path)
root.configure(bg='gray20')
dark_style = {'bg': 'gray20', 'fg': 'white'}

button_set_output = tk.Button(root, text="Set Output images Folder (Default images_alarm)", command=set_output_folder, **dark_style)
button_set_output.pack(pady=10)

button_toggle_sound = tk.Button(root, text="Toggle Alarm", command=toggle_sound, **dark_style)
button_toggle_sound.pack(pady=10)

button_start_detection = tk.Button(root, text="Start Detection", command=start_detection, **dark_style)
button_start_detection.pack(pady=10)

label_output_folder = tk.Label(root, text="Output Folder: Default (images_alarm)", **dark_style)
label_output_folder.pack(pady=10)

label_sound_status = tk.Label(root, text="Sound: Enabled", **dark_style)
label_sound_status.pack(pady=10)

label_capture_status = tk.Label(root, text="", **dark_style)
label_capture_status.pack(pady=10)

label_hyperlink = tk.Label(root, text="Git-Hub repository", cursor="hand2", **dark_style)
label_hyperlink.pack(pady=10)
label_hyperlink.bind("<Button-1>", open_link)


root.mainloop()