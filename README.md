# 🟢 WhatsApp Auto Message Fowarder Bot - Alpha 1.0.0 🟢

### This is a program that automatically sends a message from a contact to another. 📧

- It is in a **very early state**.

- I've made it using Python and Selenium Library.

- The purpose of this project is to find a way to automate information propagation.

### This is a small video i made to show some of it's functionality, it is in brazilian portuguese.
*Clicking the image will redirect you to a video hosted on my personal website.*

[![Watch the video](http://gabrielaraujo.xyz/thumbnailgit.png)](http://gabrielaraujo.xyz/projetowhatsapp.mp4)

## How to use it

- First, import the class "Bot" and store the names of the contacts you want to exchange messages.

- Then, you'll need to connect to whatsapp by scanning the QR code showed on your screen.

```html
from whatsappbot import Bot

input_contact_name = "Input"
output_contact_name = "Output"

bot = Bot(input_contact_name, output_contact_name)
bot.run()

```

- After that, messages sent to the Input contact will automatically be sent to the Output contact.

#### Things it can do:
○ Send: Short messages, long messages, stacked messages, messages with links, pictures with text, text with emojis. Reply normal text and text with links.

#### Things it can't do, yet:
○ Send audios, stickers, pictures with no text and messages with emojis only. Reply audios, stickers and pictures.

# Notes

If you haven't saved the number of the person who's messages to a group, you'll need to specificy the name and number of that person in the class construction parameters. It's part of the process. 

I made this project for personal use only.

This is the first "big" "application" i have done. I'm still new to this.

I don't think the code is pretty, it lacks organization and may not be optimized. For now, i don't intend to update this, it has taken a lot of time from me, but i learned a lot from it.

Again, the program is in a very early state, there's plenty of bugs that i haven't figured out how to solve yet. Also, it can stop working due to the browser's loading time and
other exceptions.

