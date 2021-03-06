# WhatsApp Auto Message Fowarder Bot - Alpha v1.0.1

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
1. Download ChromeDriver [<ins>**here**</ins>](https://chromedriver.chromium.org/downloads) on it's official website.
2. Make sure to have the most compatible version with your browser.
3. Paste the <ins>*chromedriver.exe*</ins> file on your <ins>*C:\Program Files\Python*</ins> folder.

### Using the program

- Import our "Bot" class and inform those contact names which you want to exchange messages with.

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
If you're willing to copy messages from one or various persons in a group, <ins>you'll need to populate a list with their names **OR** phone numbers </ins> and then reference it on the "Bot" creation function.

Something like this:

```html

from whatsappbot import Bot

input_contact_name = "Group 1"
output_contact_name = "Group 2"

messager_names = ["Gabriel", "Marcos", "Thalles", "Davi", "Guilherme", "Caio", "Luiz", "C??ndido"]

messager_numbers = ["+55 61 3686-4237", "+55 91 3613-3162"]

bot = Bot(input_contact_name, output_contact_name, messagername=messager_names, messagernumber=messager_numbers)

bot.run()

```

#### Things it can do:
> * Send short messages, long messages, stacked phrases, messages with links without a link preview, pictures with text, text with emojis. 
> * Reply normal text, text with emojis and text with links.

#### Things it can't do, yet:
> * Send audios, stickers, pictures with no text, messages with emojis only, messages with a link preview.
> * Reply audios, stickers and pictures.
> * These features will be implemented within further updates.

# Notes

If you try to do something not metioned in the "Things it can do" section, the program will probably crash. There are a lot of exceptions and cases that need to be analyzed and solved.

I made this project for personal use only.

This is the first "application" I have done. 

I don't think the code is pretty, it lacks organization and may not be optimized. For now, I won't make updates, it has taken a lot of time from me, but I've learned a lot from it.

Again, the program is in a very early state, there's plenty of bugs that I haven't figured out how to solve yet. Also, it can stop working due to the browser's loading time and other exceptions.
