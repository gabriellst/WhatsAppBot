# WhatsApp Auto Message Fowarder Bot - Alpha v1.0.0

### This is a program that automatically copies a new message from a contact and sends to another. 

- The purpose of this project is to find a way to automate information propagation.

- It is in a **very early state**. Bugs are expected.

- I've made it using Python and Selenium Library.

### Here's a small video i've made showing off some of it's functionalities, it is in brazilian portuguese.
*Clicking the image will redirect you to a video hosted on my personal website.*

[![Watch the video](http://gabrielaraujo.xyz/thumbnailgit.png)](http://gabrielaraujo.xyz/projeto_whatsapp.mp4)

# How to use it

### First, make sure to install Selenium and Chromedriver on your PC.

* *Installing Selenium:*

```html
!pip install selenium
```

* *Installing ChromeDriver:*
1. Download chromedriver [**here**](https://chromedriver.chromium.org/downloads) on it's official website.
2. Make sure to have the most compatible version with your browser.
3. Paste the chromedriver.exe file on your *C:\Program Files\Python* folder.

### Using the program

- Import our "Bot" class and inform those contact names who you want to exchange messages.

```html
from whatsappbot import Bot

input_contact_name = "Input"
output_contact_name = "Output"

bot = Bot(input_contact_name, output_contact_name)
bot.run()

```

- Then, you'll need to connect to whatsapp by scanning a QR code showed on your screen.

- After that, messages sent to the Input contact will automatically be sent to the Output contact.

### Group messaging
If you're willing to copy messages from one or various persons in a group, you'll need to populate a list with their names **OR** phone numbers and then reference it on the "Bot" creation function.

Something like this:

```html

from whatsappbot import Bot

input_contact_name = "Group 1"
output_contact_name = "Group 2"

messager_names = ["Gabriel", "Davy", "Thalles", "Davi", "Guilherme", "Caio", "Luiz", "Cândido"]

messager_numbers = ["+55 61 3686-4237", "+55 91 3613-3162"]

bot = Bot(input_contact_name, output_contact_name, messagername=messager_names, messagernumber=messager_numbers)

bot.run()

```


#### Things it can do:
> * Send: Short messages, long messages, stacked messages, messages with links, pictures with text, text with emojis. Reply normal text and text with links.

#### Things it can't do, yet:
> * Send audios, stickers, pictures with no text messages with emojis only, messages with link preview.
> * Reply audios, stickers and pictures.
> * These features will be implemented within further updates.

# Notes

If you haven't saved the number of the person who's sending messages to a group, you'll need to specificy the name and number of that person in the class function. It's part of the process. 

I made this project for personal use only.

This is the first "big" "application" i have done. I'm still new to this.

I don't think the code is pretty, it lacks organization and may not be optimized. For now, i don't intend to update this, it has taken a lot of time from me, but i learned a lot from it.

Again, the program is in a very early state, there's plenty of bugs that i haven't figured out how to solve yet. Also, it can stop working due to the browser's loading time and other exceptions.

