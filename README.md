# Movement_detector_telegram
Movement detector and capture whit telegram alarm

# Installation
```bash
git clone https://github.com/GUCHIHACKER/Movement_detector_telegram.git
cd Movement_detector_telegram
pip install -r requirements.txt
```
# Configuration
## Create a telegram bot 
Create a telegram bot and add it to a group
[Help Page](https://atareao.es/tutorial/crea-tu-propio-bot-para-telegram/)
## Copy telegram bot-token, chat-id and add to the script
The chat id can be found here https://web.telegram.org/a/#your-bot-token

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
##Change camera
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
