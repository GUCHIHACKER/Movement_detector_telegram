# Movement_detector_telegram
Movement detector and capture whit telegram alarm, work in linux and windows.

# Installation
```bash
git clone https://github.com/GUCHIHACKER/Movement_detector_telegram.git
cd Movement_detector_telegram
pip install -r requirements.txt
```

# Configuration
## Create a telegram bot 
Create a telegram bot and add it to a group.
[Help Page](https://atareao.es/tutorial/crea-tu-propio-bot-para-telegram/)
## Copy telegram bot-token, chat-id and add to the script
The chat id of the group can be found here https://web.telegram.org/a/#chat-id

In this part of the code change the bot token and in chatid for yours.
```python
...
sound_enabled = True 

token = 'your-bot-token' # Change to your telegram bot token
chat_id = 'your-chat-id' # Change to the chatid of the group you created
alarm_sound = pygame.mixer.Sound('alarm.mp3')
output_folder = 'images_alarm'
...
```

## Change camera
Change the number in this part of the code, if you want to do it with a secondary camera put the number 1 and if you have more than 2 cameras, 2,3,4,etc... 

```python
...
from tkinter import filedialog
pygame.init()

i = 45
e = 25
cap = cv2.VideoCapture(0)  # Change this number to switch cameras (Default: 0)
audio_playing = False
start_time = None
prev_frame = None
...
```
## Change Alarm

Clearly you can change the alarm by changing the alarm.mp3 file to any other audio file clearly naming it the same name as the original one

# Running the tool
```bash
python main.py
```
![tool](https://github.com/GUCHIHACKER/Movement_detector_telegram/blob/main/tool-running.png)

To stop the tool press the esc key.
# Recommendations
The use of high quality webcams is recommended to improve detection, throughout the project I was using a 1080p action cam and it was great.

![camera](https://github.com/GUCHIHACKER/Movement_detector_telegram/blob/main/camera.jpeg)

If you have a lot of problems with false positives due to camera quality or anything else you can change a parameter in the code.

```python
...
            motion_pixels = np.sum(thresh) // 255

            if motion_pixels > 100:  # The larger this number is, the less sensitive the detector is, change it if you have problems with false positives
                if e >= 30:
                    threading.Thread(target=lambda: telegram_bot_msg(), daemon=True).start()
                    e = 0
...
```

# [LICENSE](https://github.com/GUCHIHACKER/Movement_detector_telegram/blob/main/LICENSE)

