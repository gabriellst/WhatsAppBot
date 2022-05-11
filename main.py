from whatsappbot import Bot

input_contact_name = "Input"
output_contact_name = "Output"

# List with all messager names
messager_names = []
# List with all messager numbers
messager_numbers = []

bot = Bot(input_contact_name, output_contact_name, messagername=messager_names, messagernumber=messager_numbers)

bot.run()
