import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QColor, QPalette
import os

def set_dark_mode(window):
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(208, 208, 208))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(208, 208, 208))
    dark_palette.setColor(QPalette.ToolTipText, QColor(208, 208, 208))
    dark_palette.setColor(QPalette.Text, QColor(208, 208, 208))
    dark_palette.setColor(QPalette.Button, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ButtonText, QColor(208, 208, 208))
    dark_palette.setColor(QPalette.BrightText, QColor(240, 240, 240))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(208, 208, 208))
    window.setPalette(dark_palette)

def create_bot():
    token = token_entry.text().strip()
    if not token:
        QMessageBox.critical(window, "Error", "The token field cannot be left empty!")
        return
    
    prefix = prefix_entry.text().strip()
    commands = [command.strip() for command in command_entry.text().split(',')]
    responses = [response.strip() for response in response_entry.toPlainText().split('\n')]
    profanity_list = [profanity.strip() for profanity in profanity_entry.toPlainText().split('\n') if profanity.strip()]

    bot_code = f'''
import re
import discord
from discord.ext import commands

Bot = commands.Bot(command_prefix="{prefix}", intents=discord.Intents.all())

def check_for_profanity(message, profanity_list):
    regex = re.compile("(%s)" % "|".join(map(re.escape, profanity_list)), re.IGNORECASE)
    if regex.search(message):
        return True
    else:
        return False

@Bot.event
async def on_message(message):
    if message.author == Bot.user:
        return

    if check_for_profanity(message.content, {profanity_list}):
        await message.delete()
    else:
        await Bot.process_commands(message)
'''

    for i in range(len(commands)):
        command = commands[i]
        response = responses[i]
        bot_code += f'''
@Bot.command()
async def {command}(ctx):
    await ctx.send("{response}")
'''

    bot_code += f'''
Bot.run('{token}')
'''

    # Get the program directory
    program_directory = os.path.dirname(os.path.realpath(__file__))

    # Create the file path
    file_path = os.path.join(program_directory, 'discord_bot.py')

    # Save the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(bot_code)

    # Show a success message to the user
    QMessageBox.information(window, "Success", f"Discord bot has been successfully created.")

def show_information():
    info_message = QMessageBox()
    info_message.setWindowTitle("Information")
    info_message.setText("When writing commands, do not leave spaces without a comma. The command and response sections are parallel to each other. For example, the text after the comma in the command section corresponds to the second line in the response section. The prefix and profanity sections are optional. You can leave them empty. The symbol in the prefix section determines the command's label. The words in the profanity section will be automatically deleted by the bot when typed in the chat.")
    info_message.setIcon(QMessageBox.Information)
    info_message.exec_()

def save_to_file():
    program_directory = os.path.dirname(os.path.realpath(__file__))
    file_path, _ = QFileDialog.getSaveFileName(window, "Save", program_directory, "Text Files (*.txt)")
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("1\n" + token_entry.text() + '\n')
            file.write("2\n" + prefix_entry.text() + '\n')
            file.write("3\n" + command_entry.text() + '\n')
            file.write("4\n" + response_entry.toPlainText() + '\n')
            file.write("5\n" + profanity_entry.toPlainText())

def load_from_file():
    program_directory = os.path.dirname(os.path.realpath(__file__))
    file_path, _ = QFileDialog.getOpenFileName(window, "Load", program_directory, "Text Files (*.txt)")
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            current_key = None
            current_text = ""
            for line in lines:
                line = line.strip()
                if line.isdigit():
                    if current_key is not None:
                        if current_key == 1:
                            token_entry.setText(current_text)
                        elif current_key == 2:
                            prefix_entry.setText(current_text)
                        elif current_key == 3:
                            command_entry.setText(current_text)
                        elif current_key == 4:
                            response_entry.setPlainText(current_text)
                        elif current_key == 5:
                            profanity_entry.setPlainText(current_text)
                    current_key = int(line)
                    current_text = ""
                else:
                    current_text += line + '\n'
            
            if current_key is not None:
                if current_key == 1:
                    token_entry.setText(current_text)
                elif current_key == 2:
                    prefix_entry.setText(current_text)
                elif current_key == 3:
                    command_entry.setText(current_text)
                elif current_key == 4:
                    response_entry.setPlainText(current_text)
                elif current_key == 5:
                    profanity_entry.setPlainText(current_text)

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Discord Bot Creator")
window.setGeometry(100, 100, 300, 300)

layout = QVBoxLayout()

token_layout = QHBoxLayout()
token_label = QLabel("Discord Token:")
token_label.setStyleSheet("color: #00FFFF; font: bold")
token_layout.addWidget(token_label)
token_layout.addWidget(QLabel())
layout.addLayout(token_layout)
token_entry = QLineEdit()
token_entry.setStyleSheet("background-color: #ADD8E6; color: black")
layout.addWidget(token_entry)

prefix_layout = QHBoxLayout()
prefix_label = QLabel("Prefix:")
prefix_label.setStyleSheet("color: #00FFFF; font: bold")
prefix_layout.addWidget(prefix_label)
prefix_layout.addWidget(QLabel())
layout.addLayout(prefix_layout)
prefix_entry = QLineEdit()
prefix_entry.setStyleSheet("background-color: #ADD8E6; color: black")
layout.addWidget(prefix_entry)

command_layout = QHBoxLayout()
command_label = QLabel("Commands (separate with commas):")
command_label.setStyleSheet("color: #00FFFF; font: bold")
command_layout.addWidget(command_label)
command_layout.addWidget(QLabel())
layout.addLayout(command_layout)
command_entry = QLineEdit()
command_entry.setStyleSheet("background-color: #ADD8E6; color: black")
layout.addWidget(command_entry)

response_layout = QHBoxLayout()
response_label = QLabel("Responses (one response per line):")
response_label.setStyleSheet("color: #00FFFF; font: bold")
response_layout.addWidget(response_label)
response_layout.addWidget(QLabel())
layout.addLayout(response_layout)
response_entry = QTextEdit()
response_entry.setStyleSheet("background-color: #ADD8E6; color: black")
layout.addWidget(response_entry)

profanity_layout = QHBoxLayout()
profanity_label = QLabel("Profanity List (one word per line):")
profanity_label.setStyleSheet("color: #00FFFF; font: bold")
profanity_layout.addWidget(profanity_label)
profanity_layout.addWidget(QLabel())
layout.addLayout(profanity_layout)
profanity_entry = QTextEdit()
profanity_entry.setStyleSheet("background-color: #ADD8E6; color: black")
layout.addWidget(profanity_entry)

button_layout = QHBoxLayout()
create_button = QPushButton("Create Bot")
create_button.setStyleSheet("background-color: #2A82DA; color: #0BF8FF; font: bold")
info_button = QPushButton("Information")
info_button.setStyleSheet("background-color: #2A82DA; color: #0BF8FF; font: bold")
save_button = QPushButton("Save")
save_button.setStyleSheet("background-color: #2A82DA; color: #0BF8FF; font: bold")
load_button = QPushButton("Load")
load_button.setStyleSheet("background-color: #2A82DA; color: #0BF8FF; font: bold")
button_layout.addWidget(info_button)
button_layout.addWidget(save_button)
button_layout.addWidget(load_button)
button_layout.addWidget(create_button)
info_button.clicked.connect(show_information)
save_button.clicked.connect(save_to_file)
load_button.clicked.connect(load_from_file)
create_button.clicked.connect(create_bot)
layout.addLayout(button_layout)
button_layout.addStretch()

youtube_label = QLabel('<a href="https://www.youtube.com/@Rhetechnic">Youtube: Rhetechnic</a>')
youtube_label.setOpenExternalLinks(True)
youtube_label.setStyleSheet("color: #00FFFF; font: bold")
layout.addWidget(youtube_label)

window.setLayout(layout)
window.show()
set_dark_mode(window)
sys.exit(app.exec_())