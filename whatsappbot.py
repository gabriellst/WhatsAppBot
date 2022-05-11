from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
import os


def browser_anonimo(save_cookies=False):
    # Setting up browser, cookie saving, reducing bot detection.
    options = webdriver.ChromeOptions()
    dir_path = os.getcwd()

    if save_cookies:

        profile = os.path.join(dir_path, "profile", "WhatsAppBotProfile")

        options.add_argument(
            r"user-data-dir={}".format(profile))

    options.add_argument("window-size=1280,720")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/99.0.4844.84 Safari/537.36")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    options.add_experimental_option('useAutomationExtension', False)

    browser = webdriver.Chrome(options=options, executable_path=r"chromedriver.exe")

    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {

        "source": """

    Object.defineProperty(navigator, 'webdriver', {

    get: () => undefined

    })

    """

    })

    browser.execute_cdp_cmd('Network.setUserAgentOverride',

                            {
                                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                             'like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

    return browser


class Bot:
    # Defining variables
    def __init__(self, input_contact, output_contact, messagernumber="", messagername="", cookies=False):
        self.browser = browser_anonimo(save_cookies=cookies)
        self.inputmsg = ""
        self.inputmsgfull = ""
        self.outputmsg = ""
        self.outputmsgfull = ""
        self.inputcontact = input_contact
        self.outputcontact = output_contact
        self.pendingmsg = []
        self.lastmedia = None
        self.messagernumber = messagernumber
        self.messagername = messagername
        self.wait = WebDriverWait(self.browser, 10)
        self.chain = ActionChains(self.browser)
        self.key = Keys()

    # Defining main run fuction

    def run(self):
        self.connect()
        while True:
            self.listening()
            self.send_new_msgs()

    #  Connecting to whatsapp
    def connect(self):
        self.browser.get("https://web.whatsapp.com/")
        self.browser.maximize_window()
        whatsapp_connected = False
        qrcode_read = False

        print("Waiting Conection, please scan QR CODE\n")

        while not whatsapp_connected:
            try:
                if not qrcode_read:
                    self.wait.until(ec.visibility_of_element_located((By.CLASS_NAME, '_2pp-n')))
                    print("QR Code loaded successfully. Connecting.\n")
                    qrcode_read = True

                self.wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'YtmXM')))
                print("Connected to whatsapp.\n")
                whatsapp_connected = True
            except:
                print("Not possible to stablish a connection, trying again.\n")
                continue

    # Searching for a specific contact
    def search_contact(self, contact_to_search):
        sleep(0.5)
        print(f"Searching for: {contact_to_search} in contact list\n")
        while True:
            try:
                # Defining the contact search box xpath and searching for the input contact.
                searcher_box_xpath = '//*[@id="side"]/div[1]/div/label/div/div[2]'
                searcher_box = self.browser.find_element(by=By.XPATH, value=searcher_box_xpath)
                searcher_box.clear()
                searcher_box.send_keys(contact_to_search)

                # Waiting for the buttons to show up.

                self.wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, '_3m_Xw')))

                # Using a method to return a list with all contacts rectangles divs.

                resultant_contacts_divs = self.find_contacts_divs()

                # Iterating through list and veryfing contact

                for contact_object in resultant_contacts_divs:

                    self.wait.until(ec.visibility_of(contact_object))

                    contact_div_text = contact_object.text  # Results in "ContactName\nDay\nmessage"
                    contact_text_split = contact_div_text.split("\n")
                    iterated_contact_name = contact_text_split[0].strip()
                    print(f"Iterated Contact: {iterated_contact_name}")
                    print(f"Contact we want to find = {contact_to_search}")
                    print("Are they equal? ", iterated_contact_name == contact_to_search)

                    if iterated_contact_name == contact_to_search.strip():
                        print("Found contact! Returning it\n")
                        return contact_object
            except:
                print("Found no contact with the specified name, trying again.\n")

    def listening(self):
        sleep(0.5)

        if self.inputmsg == "Foto":
            self.outputmsg = "Foto"

        elif self.inputmsg == "Àudio":
            self.outputmsg = "Àudio"

        elif self.inputmsg == "Figurinha":
            self.outputmsg = "Figurinha"

        print("Waiting for new messages on the input contact.\n")

        self.outputmsgfull = "".join(self.outputmsg)
        print(f"Last message sent from the input: {self.inputmsg}")
        print(f"Last message sent to the output: {self.outputmsgfull}")

        # We can search what messages are appearing given the contact rectangle div webelement.

        contact_object = self.search_contact(self.inputcontact)

        # There are some messages that appear on the contact div that we aren't interested.
        # For example, when someone gets added or removed to the group.

        text_div_classname = '_2ad1k'
        not_useful_messages_list = contact_object.find_elements(by=By.CLASS_NAME, value=text_div_classname)
        # returns a list with not useful text

        contact_div_message = contact_object.text.split("\n")
        # print(f"Contact div message {contact_div_message}\n")
        self.inputmsg = contact_div_message[-1]

        # There's a difference between strings captured from the contact rectangle div and those captured from the
        # chat itself. That way, comparing them was a bit tricky. This creates a problem that revolves around \n's
        # and spaces, so i needed to figure out a workaround for that. The easiest way to make a comparison between
        # them was to split all words and then joining them together, for every string. That way i could compare
        # messages read from the contact rectangle div and those read from the chat.

        self.inputmsg = self.inputmsg.split()
        median_index = (len(self.inputmsg) // 2) + 1
        self.inputmsg = self.inputmsg[0:median_index]
        self.inputmsg = "".join(self.inputmsg)

        self.outputmsg = self.outputmsg[0:median_index]
        self.outputmsg = "".join(self.outputmsg)

        # Verifying if there's a new message. If the user is typing, it would consider as a different message,
        # but we don't want that.

        # The two variables to compare are:
        # self.inputmsg, which is the current message read from the contact rectangle div.
        # self.outputmsg, this message is only registered when we successfully copy all new messages,
        # The last copied message becomes the outputmsg, so, new messages are only copied if they are different.

        while self.inputmsg == self.outputmsg or contact_object.text.find("digitando") != -1 or \
                any(not_useful_messages_list):
            # Updating the message.
            not_useful_messages_list = contact_object.find_elements(by=By.CLASS_NAME, value='_2ad1k')
            contact_div_message = contact_object.text.split("\n")
            self.inputmsg = contact_div_message[-1]
            self.inputmsg = self.inputmsg.split()
            median_index = (len(self.inputmsg) // 2) + 1
            self.inputmsg = self.inputmsg[0:median_index]
            self.inputmsg = "".join(self.inputmsg)

        print("Found a new message\n")
        print(f"Last message sent from the input: {self.inputmsg}")
        print(f"Last message sent to the output: {self.outputmsg}")

        # After verifying a new message, the contact is clicked so we can copy messages from it.

        contact_object.click()

    def send_new_msgs(self):
        sleep(0.5)
        # Creating a list of all messages divs, their splitted texts, and their joined texts.
        messages_divs, messages_split_list, messages_concat = self.find_messages_text()
        sleep(0.5)

        # if Its the first time running the program, it won't copy anything.

        # There's a full and half version of the output msg because when we read a message from the chat
        # It may get sliced with the "read more" section
        if self.outputmsg == "":
            self.outputmsg = messages_split_list[0]
            self.outputmsgfull = messages_concat[0]
            return False

        # The list with concatenated text is written from bottom to the top, so the latest messages are read first.
        # If we wrote the same word two times in a row, it will mark the last one as the starting point for the copy.

        # Finding list index of the latest output msg
        last_output_message_index = messages_concat.index(self.outputmsgfull)
        last_output_message_index = len(messages_concat) - last_output_message_index - 1

        # Reversing the list so we can copy its phrases in the right order.
        messages_divs = messages_divs[::-1]
        messages_split_list = messages_split_list[::-1]
        messages_concat = messages_concat[::-1]

        print(f"Latest message sent to the output: {self.outputmsgfull}")
        print(f"Starting to copy messages from the next one\n")

        # The copy starts at the next message, after the last one sent.
        next_msg_index = int(last_output_message_index + 1)
        messages_quantity = len(messages_divs)

        # We iterate through all messages, starting from the last one sent to the output contact.
        for index in range(next_msg_index, messages_quantity):
            if messages_split_list[index] is None:
                continue

            outputmsg_holder = messages_split_list[index]
            html_code = messages_divs[index].get_attribute("innerHTML")

            if outputmsg_holder != "":
                pure_text_list = self.browser.find_elements(by=By.CLASS_NAME, value='_1Gy50')
                pure_text_list_concat = ["".join(element.text.split()) for element in pure_text_list]
                pure_text_index = pure_text_list_concat.index("".join(outputmsg_holder))
                msg_div_text = pure_text_list[pure_text_index].text
                print(f"Line being copied: {msg_div_text}\n")

            else:
                msg_div_text = ""
                print(f"Selected div doesn't have text\n")

            if html_code.find("mention") != -1:
                if any(self.pendingmsg):
                    self.send_pending_msgs()

                print(f"Repplied text being sent {msg_div_text}\n")
                reply_text = self.reply_message(html_code)
                self.pendingmsg.append(reply_text)
                self.insert_send_msgs()
                self.outputmsg = reply_text.split()

            elif html_code.find("img") != -1:
                self.lastmedia = messages_divs[index]
                if any(self.pendingmsg):
                    self.send_pending_msgs()

                print(f"Media text being sent: {msg_div_text}\n")
                mediatype = self.forward_message(html_code)

                if mediatype != "Figurinha" and mediatype != "Emoji":
                    self.pendingmsg.append(msg_div_text)
                    self.insert_send_msgs()

                if msg_div_text == "":
                    self.pendingmsg.append(mediatype)
                    self.outputmsg = mediatype

                else:
                    self.outputmsg = outputmsg_holder

                self.search_click(self.inputcontact)
                break
            else:
                self.pendingmsg.append(msg_div_text)

            # self.search_click(self.inputcontact)

        if any(self.pendingmsg):
            self.outputmsg = self.pendingmsg[-1].split()
            self.send_pending_msgs()
        else:
            print("No new messages to be sent\n")

    def search_click(self, contact_name):
        contact_to_click = self.search_contact(contact_name)
        sleep(0.5)
        contact_to_click.click()

    def find_contacts_divs(self):
        contacts_div_class_name = '_3m_Xw'
        self.wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, contacts_div_class_name)))
        contacts_div_list = self.browser.find_elements(by=By.CLASS_NAME, value=contacts_div_class_name)
        return contacts_div_list

    def find_text_divs(self):
        messages_div_xpath = "//div[contains(@class, '_2wUmf')]"
        messages_div_list = self.browser.find_elements(by=By.XPATH, value=messages_div_xpath)
        self.wait.until(ec.presence_of_all_elements_located((By.XPATH, messages_div_xpath)))

        # Since we need to check the new messages first, the list needs to be flipped.

        return messages_div_list[::-1]

    def find_messages_text(self):
        messageslist = []
        concatenatedlist = []
        messages_divs = self.find_text_divs()
        for element in messages_divs:
            try:
                if element.get_attribute("className").find("message") == -1:
                    messageslist.append(None)
                    continue
            except:
                messageslist.append(None)
                continue

            html_code = element.get_attribute("innerHTML")

            if html_code.find("mention") != -1:
                reply_msg, repplied_msg = self.get_replies(html_code)
                splitted_message = reply_msg.split()
            else:
                splitted_message = element.text.split()
                splitted_message = splitted_message[0:-1]

            if any(splitted_message):
                if splitted_message[0] == "Encaminhada":
                    splitted_message = splitted_message[1:]
                if self.messagername != "":
                    while splitted_message[0] in self.messagernumber or splitted_message[0] in self.messagername:
                        print(f"Splitted message from contact = {splitted_message}")
                        splitted_message = splitted_message[1:]

            messageslist.append(splitted_message)

        for element in messageslist:
            if element is not None:
                concatenatedlist.append("".join(element))
                continue

            concatenatedlist.append(element)

        return messages_divs, messageslist, concatenatedlist

    def send_pending_msgs(self):
        self.search_click(self.outputcontact)
        self.insert_send_msgs()
        self.search_click(self.inputcontact)

    def insert_send_msgs(self):
        sleep(0.5)
        print(f"Sending messages to {self.outputcontact}\n")
        writing_box = self.browser.find_element(by=By.XPATH, value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[''1]/div/div[2]')

        for mensagem in self.pendingmsg:
            message_split = mensagem.split("\n")
            if len(message_split) > 1:
                for row in message_split:
                    writing_box.send_keys(row)
                    writing_box.send_keys(self.key.SHIFT + self.key.ENTER)

                writing_box.send_keys(self.key.ENTER)
                continue

            writing_box.send_keys(mensagem, self.key.ENTER)
            sleep(0.1)
        self.pendingmsg = []

    def reply_message(self, html_code):
        # with the html_code and its cleaning i can find all informations from a div, so thats easier

        reply_msg, repplied_msg = self.get_replies(html_code)

        self.search_click(self.outputcontact)

        sleep(0.5)

        messages_divs, messageslist, concatenatedlist = self.find_messages_text()

        for index in range(len(messageslist)):
            if messageslist[index] is not None:
                joined_text = "".join(repplied_msg.split())
                concatenatedtext = ''.join(messageslist[index])
                if joined_text == concatenatedtext:
                    repplied_text_div = messages_divs[index]
                    break

        mediatype = ""
        if html_code.find("img") != -1:
            mediatype = "Foto"

        self.hover_and_execute(repplied_text_div, command="reply", mediatype=mediatype)

        return reply_msg

    def get_replies(self, html_code):

        html_list = html_code.split('>')
        try:
            replied_msg = html_list[html_list.index('<div class=\"hooVq color-1\" role=\"button\"') + 6]
        except:
            replied_msg = html_list[html_list.index('<div class=\"hooVq color-2\" role=\"button\"') + 6]

        reply_msg = html_list[html_list.index('<div class="_1Gy50"') + 3]
        # removing </span from the strings, span occupies the 6 last strings
        reply_msg = reply_msg[:-6]
        repplied_msg = replied_msg[:-6]

        if repplied_msg.find("<img crossorigin") != -1:
            repplied_msg = repplied_msg.split("<img")[0]

        if reply_msg.find("<img crossorigin") != -1:
            reply_msg = reply_msg.split("<img")[0]

        return reply_msg, repplied_msg

    def forward_message(self, html_code):

        mediatype = ""

        messages_divs_reload = self.find_text_divs()

        for div in messages_divs_reload:
            if div.get_attribute("innerHTML") == html_code:
                lastmedia = div
                break

        media_class_names = {"emoji": "Emoji", "image": "Foto", "video": "Vídeo", "audio": "Áudio",
                             "figurinha": "Figurinha"}

        for class_name in media_class_names:

            if html_code.find(class_name) != -1:
                mediatype = media_class_names[class_name]
                break

        self.hover_and_execute(lastmedia, mediatype=mediatype, command="forward")

        forward_button = self.browser.find_element(by=By.XPATH, value='//*[@id="main"]/span[2]/div[1]/button[4]')

        self.wait.until(ec.visibility_of(forward_button))

        forward_button.click()

        search_box = self.browser.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/div[1]/div/label/div/div[2]')

        self.wait.until(ec.visibility_of(search_box))

        search_box.send_keys(self.outputcontact)

        sleep(0.5)

        contact_button = self.browser.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/div[2]/div/div/div/div[1]/button/div[2]/div')

        sleep(0.5)

        self.wait.until(ec.visibility_of(contact_button))

        contact_button.click()

        last_foward_button = self.browser.find_element(by=By.XPATH, value='//*[@id="app"]/div[1]/span[2]/div[1]/span/div[1]/div/div/div/div/div/span/div/div')

        self.wait.until(ec.visibility_of(last_foward_button))

        last_foward_button.click()

        sleep(0.5)

        return mediatype

    def hover_and_execute(self, webelement, **kwargs):

        command = kwargs.get("command")

        if command == "forward":
            command_name = "Encaminhar"
        elif command == "reply":
            command_name = "Responder"

        arrow_class_name = '_3e9My'

        content_box = webelement.find_element(by=By.TAG_NAME, value="div")

        self.chain.move_to_element(content_box).perform()

        sleep(0.2)

        try:
            arrow = self.browser.find_element(by=By.CLASS_NAME, value=arrow_class_name)
        except:
            arrow_class_name = '_3sryO'
            arrow = self.browser.find_element(by=By.CLASS_NAME, value=arrow_class_name)

        arrow.click()

        self.wait.until(ec.visibility_of_all_elements_located((By.CLASS_NAME, '_2qR8G._1wMaz._18oo2')))

        dropdown = self.browser.find_elements(by=By.CLASS_NAME, value='_2qR8G._1wMaz._18oo2')

        for option in dropdown:
            self.wait.until(ec.visibility_of(option))
            print(option.text)
            if option.text.find(command_name) != -1:
                option.click()
                break

# End
