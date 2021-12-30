# version 1.0
import ctypes
import logging
import os
import random
import re
import sys
import threading
import time
import tkinter as tk
import requests
import hashlib
import urllib.request
import logging
from tqdm import tqdm
from datetime import datetime
from tkinter import filedialog
# from progress.spinner import Spinner
from tkinter.font import Font

import pandas as pd
import paramiko
import requests
# from selenium.common.exceptions import TimeoutException
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

#url for update
RAW_PATH = 'https://raw.githubusercontent.com/maximpalych/p.synergo/main/test.py'

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
cl = paramiko.SSHClient()
cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ethers_status = []
THREAD_POOL = 0
THREAD_POOL_MAX = 2
RESET_MODE = False
TEST_MODE = False
MSVK_MODE = False
RESET_MSVK_MODE = False
FILE = ''
FILE_FOLDER = ''
BG_COLOR = '#3D3D3D'
SELECT_COLOR = '#28b463'
TXT_COLOR = '#FAE5D3'
TXT_SELECT_COLOR = '#000000'
TXT_FILE_COLOR = '#F1C40F'
COLOR_OFF = '#E74C3C'
COLOR_ON = '#27AE60'
SHOW_BUTTON = '#34495E'
RESET_BTN = '#5B2C6F'
STRT_BTN = '#28B463'
STP_BTN = '#CB4335'
path_o4vm13 = "D:\\Documents\\synergo\\ASynergoFirmware\\no_data\\O4vm13_no_date_14042021\\General_IPC-HX2XXX" \
              "-Molec_MultiLang_PN-CustomPro_V2.800.14SW002.0.R.200829.bin"
path_5vm50 = "D:\\Documents\\synergo\\ASynergoFirmware\\no_data\\5VM50_21052021_no_date\\General_IPC-HX5XXX" \
             "-Volt_MultiLang_PN_Stream3-CustomPro_V2.800.14SW006.0.R.200729.bin"
path_5vm50_shakh = "C:\\A_Firmware\\5mp\\5VM50_21052021_no_date\\General_IPC-HX5XXX-Volt_MultiLang_PN_Stream3-CustomPro_V2.800.14SW006.0.R.200729.bin"

hosts = {}
for i in range(101, 123):
    hosts[i - 100] = [f'192.168.3.{i}', '', '']
windows_pos_table = {
    '1': [False, 0, 0],
    '2': [False, 685, 0],
    '3': [False, 1370, 0],
    '4': [False, 0, 735],
    '5': [False, 685, 735],
    '6': [False, 1370, 735]}

logging.getLogger("paramiko").setLevel(logging.WARNING)
logger_cam = logging.getLogger('camInfo')
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    filename="camInfo.log",
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title('SynergoFlashTool')
        self.parent.wm_attributes('-topmost', True)
        screen_width = self.parent.winfo_screenwidth() // 2
        screen_height = self.parent.winfo_screenheight() // 2
        self.parent.geometry('+{}+{}'.format(screen_width, screen_height))
        self.parent.resizable(False, False)
        self.parent.attributes('-toolwindow', True)

        self.main_frame = tk.Frame(parent, bg=BG_COLOR)
        self.main_frame.grid(row=0, column=0)

        self.cam_frame_left = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.cam_frame_left.grid(row=0, column=0, padx=2, pady=2)
        self.cam_frame_right = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.cam_frame_right.grid(row=0, column=1, padx=2, pady=2)

        self.ping_label = tk.Label(self.cam_frame_left, text='P', bg=BG_COLOR, fg=TXT_COLOR)
        self.ping_label.grid(row=0, column=1)
        self.web_label = tk.Label(self.cam_frame_left, text='W', bg=BG_COLOR, fg=TXT_COLOR)
        self.web_label.grid(row=0, column=2)
        self.flash_label = tk.Label(self.cam_frame_left, text='F', bg=BG_COLOR, fg=TXT_COLOR)
        self.flash_label.grid(row=0, column=3)

        self.cam_1_label = tk.Label(self.cam_frame_left, text='Cam .1 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_1_label.grid(row=1, column=0, padx=2, pady=2)
        self.cam_1_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_1_rec_ping.grid(row=1, column=1, padx=2, pady=2)
        self.cam_1_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_1_rec_web.grid(row=1, column=2, padx=2, pady=2)
        self.cam_1_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_1_rec_flash.grid(row=1, column=3, padx=2, pady=2)
        self.cam_1_checkbox_value = tk.BooleanVar()
        self.cam_1_checkbox_value.set(False)
        self.cam_1_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_1_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_1_checkbox.grid(row=1, column=4, padx=2, pady=2)
        self.cam_1_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_1'), padx=2, pady=2, bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_1_reset_button.grid(row=1, column=5, padx=2, pady=2)

        self.cam_2_label = tk.Label(self.cam_frame_left, text='Cam .2 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_2_label.grid(row=2, column=0, padx=2, pady=2)
        self.cam_2_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_2_rec_ping.grid(row=2, column=1, padx=2, pady=2)
        self.cam_2_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_2_rec_web.grid(row=2, column=2, padx=2, pady=2)
        self.cam_2_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_2_rec_flash.grid(row=2, column=3, padx=2, pady=2)
        self.cam_2_checkbox_value = tk.BooleanVar()
        self.cam_2_checkbox_value.set(False)
        self.cam_2_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_2_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_2_checkbox.grid(row=2, column=4, padx=2, pady=2)
        self.cam_2_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_2'), padx=2, pady=2, bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_2_reset_button.grid(row=2, column=5, padx=2, pady=2)

        self.cam_3_label = tk.Label(self.cam_frame_left, text='Cam .3 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_3_label.grid(row=3, column=0, padx=2, pady=2)
        self.cam_3_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_3_rec_ping.grid(row=3, column=1, padx=2, pady=2)
        self.cam_3_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_3_rec_web.grid(row=3, column=2, padx=2, pady=2)
        self.cam_3_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_3_rec_flash.grid(row=3, column=3, padx=2, pady=2)
        self.cam_3_checkbox_value = tk.BooleanVar()
        self.cam_3_checkbox_value.set(False)
        self.cam_3_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_3_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_3_checkbox.grid(row=3, column=4, padx=2, pady=2)
        self.cam_3_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_3'), padx=2, pady=2, bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_3_reset_button.grid(row=3, column=5, padx=2, pady=2)

        self.cam_4_label = tk.Label(self.cam_frame_left, text='Cam .4  ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_4_label.grid(row=4, column=0, padx=2, pady=2)
        self.cam_4_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_4_rec_ping.grid(row=4, column=1, padx=2, pady=2)
        self.cam_4_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_4_rec_web.grid(row=4, column=2, padx=2, pady=2)
        self.cam_4_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_4_rec_flash.grid(row=4, column=3, padx=2, pady=2)
        self.cam_4_checkbox_value = tk.BooleanVar()
        self.cam_4_checkbox_value.set(False)
        self.cam_4_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_4_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_4_checkbox.grid(row=4, column=4, padx=2, pady=2)
        self.cam_4_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_4'), padx=2, pady=2, bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_4_reset_button.grid(row=4, column=5, padx=2, pady=2)

        self.cam_5_label = tk.Label(self.cam_frame_left, text='Cam .5  ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_5_label.grid(row=5, column=0, padx=2, pady=2)
        self.cam_5_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_5_rec_ping.grid(row=5, column=1, padx=2, pady=2)
        self.cam_5_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_5_rec_web.grid(row=5, column=2, padx=2, pady=2)
        self.cam_5_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_5_rec_flash.grid(row=5, column=3, padx=2, pady=2)
        self.cam_5_checkbox_value = tk.BooleanVar()
        self.cam_5_checkbox_value.set(False)
        self.cam_5_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_5_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_5_checkbox.grid(row=5, column=4, padx=2, pady=2)
        self.cam_5_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_5'), padx=2, pady=2, bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_5_reset_button.grid(row=5, column=5, padx=2, pady=2)

        self.cam_6_label = tk.Label(self.cam_frame_left, text='Cam .6  ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_6_label.grid(row=6, column=0, padx=2, pady=2)
        self.cam_6_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_6_rec_ping.grid(row=6, column=1, padx=2, pady=2)
        self.cam_6_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_6_rec_web.grid(row=6, column=2, padx=2, pady=2)
        self.cam_6_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_6_rec_flash.grid(row=6, column=3, padx=2, pady=2)
        self.cam_6_checkbox_value = tk.BooleanVar()
        self.cam_6_checkbox_value.set(False)
        self.cam_6_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_6_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_6_checkbox.grid(row=6, column=4, padx=2, pady=2)
        self.cam_6_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_6'), padx=2, pady=2, bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_6_reset_button.grid(row=6, column=5, padx=2, pady=2)

        self.cam_7_label = tk.Label(self.cam_frame_left, text='Cam .7  ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_7_label.grid(row=7, column=0, padx=2, pady=2)
        self.cam_7_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_7_rec_ping.grid(row=7, column=1, padx=2, pady=2)
        self.cam_7_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_7_rec_web.grid(row=7, column=2, padx=2, pady=2)
        self.cam_7_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_7_rec_flash.grid(row=7, column=3, padx=2, pady=2)
        self.cam_7_checkbox_value = tk.BooleanVar()
        self.cam_7_checkbox_value.set(False)
        self.cam_7_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_7_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_7_checkbox.grid(row=7, column=4, padx=2, pady=2)
        self.cam_7_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_7'), padx=2, pady=2, bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_7_reset_button.grid(row=7, column=5, padx=2, pady=2)

        self.cam_8_label = tk.Label(self.cam_frame_left, text='Cam .8  ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_8_label.grid(row=8, column=0, padx=2, pady=2)
        self.cam_8_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_8_rec_ping.grid(row=8, column=1, padx=2, pady=2)
        self.cam_8_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_8_rec_web.grid(row=8, column=2, padx=2, pady=2)
        self.cam_8_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_8_rec_flash.grid(row=8, column=3, padx=2, pady=2)
        self.cam_8_checkbox_value = tk.BooleanVar()
        self.cam_8_checkbox_value.set(False)
        self.cam_8_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_8_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_8_checkbox.grid(row=8, column=4, padx=2, pady=2)
        self.cam_8_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_8'), padx=2, pady=2, bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_8_reset_button.grid(row=8, column=5, padx=2, pady=2)

        self.cam_9_label = tk.Label(self.cam_frame_left, text='Cam .9  ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_9_label.grid(row=9, column=0, padx=2, pady=2)
        self.cam_9_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_9_rec_ping.grid(row=9, column=1, padx=2, pady=2)
        self.cam_9_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_9_rec_web.grid(row=9, column=2, padx=2, pady=2)
        self.cam_9_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_9_rec_flash.grid(row=9, column=3, padx=2, pady=2)
        self.cam_9_checkbox_value = tk.BooleanVar()
        self.cam_9_checkbox_value.set(False)
        self.cam_9_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_9_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_9_checkbox.grid(row=9, column=4, padx=2, pady=2)
        self.cam_9_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_9'), padx=2, pady=2, bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_9_reset_button.grid(row=9, column=5, padx=2, pady=2)

        self.cam_10_label = tk.Label(self.cam_frame_left, text='Cam .10 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_10_label.grid(row=10, column=0, padx=2, pady=2)
        self.cam_10_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_10_rec_ping.grid(row=10, column=1, padx=2, pady=2)
        self.cam_10_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_10_rec_web.grid(row=10, column=2, padx=2, pady=2)
        self.cam_10_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_10_rec_flash.grid(row=10, column=3, padx=2, pady=2)
        self.cam_10_checkbox_value = tk.BooleanVar()
        self.cam_10_checkbox_value.set(False)
        self.cam_10_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_10_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_10_checkbox.grid(row=10, column=4, padx=2, pady=2)
        self.cam_10_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_10'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_10_reset_button.grid(row=10, column=5, padx=2, pady=2)

        self.cam_11_label = tk.Label(self.cam_frame_left, text='Cam .11 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_11_label.grid(row=11, column=0, padx=2, pady=2)
        self.cam_11_rec_ping = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_11_rec_ping.grid(row=11, column=1, padx=2, pady=2)
        self.cam_11_rec_web = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_11_rec_web.grid(row=11, column=2, padx=2, pady=2)
        self.cam_11_rec_flash = tk.Label(self.cam_frame_left, text='     ', bg=COLOR_OFF)
        self.cam_11_rec_flash.grid(row=11, column=3, padx=2, pady=2)
        self.cam_11_checkbox_value = tk.BooleanVar()
        self.cam_11_checkbox_value.set(False)
        self.cam_11_checkbox = tk.Checkbutton(self.cam_frame_left, variable=self.cam_11_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_11_checkbox.grid(row=11, column=4, padx=2, pady=2)
        self.cam_11_reset_button = tk.Button(self.cam_frame_left, text=" R ", command=lambda: resetOneFlash('cam_11'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_11_reset_button.grid(row=11, column=5, padx=2, pady=2)

        self.ping_label = tk.Label(self.cam_frame_right, text='P ', bg=BG_COLOR, fg=TXT_COLOR)
        self.ping_label.grid(row=0, column=1)
        self.web_label = tk.Label(self.cam_frame_right, text='W ', bg=BG_COLOR, fg=TXT_COLOR)
        self.web_label.grid(row=0, column=2)
        self.flash_label = tk.Label(self.cam_frame_right, text='F ', bg=BG_COLOR, fg=TXT_COLOR)
        self.flash_label.grid(row=0, column=3)

        self.cam_12_label = tk.Label(self.cam_frame_right, text='Cam .12 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_12_label.grid(row=1, column=0, padx=2, pady=2)
        self.cam_12_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_12_rec_ping.grid(row=1, column=1, padx=2, pady=2)
        self.cam_12_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_12_rec_web.grid(row=1, column=2, padx=2, pady=2)
        self.cam_12_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_12_rec_flash.grid(row=1, column=3, padx=2, pady=2)
        self.cam_12_checkbox_value = tk.BooleanVar()
        self.cam_12_checkbox_value.set(False)
        self.cam_12_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_12_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_12_checkbox.grid(row=1, column=4, padx=2, pady=2)
        self.cam_12_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_12'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_12_reset_button.grid(row=1, column=5, padx=2, pady=2)

        self.cam_13_label = tk.Label(self.cam_frame_right, text='Cam .13 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_13_label.grid(row=2, column=0, padx=2, pady=2)
        self.cam_13_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_13_rec_ping.grid(row=2, column=1, padx=2, pady=2)
        self.cam_13_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_13_rec_web.grid(row=2, column=2, padx=2, pady=2)
        self.cam_13_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_13_rec_flash.grid(row=2, column=3, padx=2, pady=2)
        self.cam_13_checkbox_value = tk.BooleanVar()
        self.cam_13_checkbox_value.set(False)
        self.cam_13_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_13_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_13_checkbox.grid(row=2, column=4, padx=2, pady=2)
        self.cam_13_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_13'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_13_reset_button.grid(row=2, column=5, padx=2, pady=2)

        self.cam_14_label = tk.Label(self.cam_frame_right, text='Cam .14 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_14_label.grid(row=3, column=0, padx=2, pady=2)
        self.cam_14_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_14_rec_ping.grid(row=3, column=1, padx=2, pady=2)
        self.cam_14_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_14_rec_web.grid(row=3, column=2, padx=2, pady=2)
        self.cam_14_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_14_rec_flash.grid(row=3, column=3, padx=2, pady=2)
        self.cam_14_checkbox_value = tk.BooleanVar()
        self.cam_14_checkbox_value.set(False)
        self.cam_14_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_14_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_14_checkbox.grid(row=3, column=4, padx=2, pady=2)
        self.cam_14_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_14'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_14_reset_button.grid(row=3, column=5, padx=2, pady=2)

        self.cam_15_label = tk.Label(self.cam_frame_right, text='Cam .15 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_15_label.grid(row=4, column=0, padx=2, pady=2)
        self.cam_15_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_15_rec_ping.grid(row=4, column=1, padx=2, pady=2)
        self.cam_15_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_15_rec_web.grid(row=4, column=2, padx=2, pady=2)
        self.cam_15_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_15_rec_flash.grid(row=4, column=3, padx=2, pady=2)
        self.cam_15_checkbox_value = tk.BooleanVar()
        self.cam_15_checkbox_value.set(False)
        self.cam_15_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_15_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_15_checkbox.grid(row=4, column=4, padx=2, pady=2)
        self.cam_15_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_15'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_15_reset_button.grid(row=4, column=5, padx=2, pady=2)

        self.cam_16_label = tk.Label(self.cam_frame_right, text='Cam .16 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_16_label.grid(row=5, column=0, padx=2, pady=2)
        self.cam_16_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_16_rec_ping.grid(row=5, column=1, padx=2, pady=2)
        self.cam_16_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_16_rec_web.grid(row=5, column=2, padx=2, pady=2)
        self.cam_16_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_16_rec_flash.grid(row=5, column=3, padx=2, pady=2)
        self.cam_16_checkbox_value = tk.BooleanVar()
        self.cam_16_checkbox_value.set(False)
        self.cam_16_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_16_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_16_checkbox.grid(row=5, column=4, padx=2, pady=2)
        self.cam_16_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_16'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_16_reset_button.grid(row=5, column=5, padx=2, pady=2)

        self.cam_17_label = tk.Label(self.cam_frame_right, text='Cam .17 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_17_label.grid(row=6, column=0, padx=2, pady=2)
        self.cam_17_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_17_rec_ping.grid(row=6, column=1, padx=2, pady=2)
        self.cam_17_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_17_rec_web.grid(row=6, column=2, padx=2, pady=2)
        self.cam_17_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_17_rec_flash.grid(row=6, column=3, padx=2, pady=2)
        self.cam_17_checkbox_value = tk.BooleanVar()
        self.cam_17_checkbox_value.set(False)
        self.cam_17_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_17_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_17_checkbox.grid(row=6, column=4, padx=2, pady=2)
        self.cam_17_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_17'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_17_reset_button.grid(row=6, column=5, padx=2, pady=2)

        self.cam_18_label = tk.Label(self.cam_frame_right, text='Cam .18 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_18_label.grid(row=7, column=0, padx=2, pady=2)
        self.cam_18_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_18_rec_ping.grid(row=7, column=1, padx=2, pady=2)
        self.cam_18_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_18_rec_web.grid(row=7, column=2, padx=2, pady=2)
        self.cam_18_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_18_rec_flash.grid(row=7, column=3, padx=2, pady=2)
        self.cam_18_checkbox_value = tk.BooleanVar()
        self.cam_18_checkbox_value.set(False)
        self.cam_18_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_18_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_18_checkbox.grid(row=7, column=4, padx=2, pady=2)
        self.cam_18_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_18'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_18_reset_button.grid(row=7, column=5, padx=2, pady=2)

        self.cam_19_label = tk.Label(self.cam_frame_right, text='Cam .19 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_19_label.grid(row=8, column=0, padx=2, pady=2)
        self.cam_19_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_19_rec_ping.grid(row=8, column=1, padx=2, pady=2)
        self.cam_19_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_19_rec_web.grid(row=8, column=2, padx=2, pady=2)
        self.cam_19_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_19_rec_flash.grid(row=8, column=3, padx=2, pady=2)
        self.cam_19_checkbox_value = tk.BooleanVar()
        self.cam_19_checkbox_value.set(False)
        self.cam_19_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_19_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_19_checkbox.grid(row=8, column=4, padx=2, pady=2)
        self.cam_19_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_19'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_19_reset_button.grid(row=8, column=5, padx=2, pady=2)

        self.cam_20_label = tk.Label(self.cam_frame_right, text='Cam .20 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_20_label.grid(row=9, column=0, padx=2, pady=2)
        self.cam_20_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_20_rec_ping.grid(row=9, column=1, padx=2, pady=2)
        self.cam_20_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_20_rec_web.grid(row=9, column=2, padx=2, pady=2)
        self.cam_20_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_20_rec_flash.grid(row=9, column=3, padx=2, pady=2)
        self.cam_20_checkbox_value = tk.BooleanVar()
        self.cam_20_checkbox_value.set(False)
        self.cam_20_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_20_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_20_checkbox.grid(row=9, column=4, padx=2, pady=2)
        self.cam_20_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_20'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_20_reset_button.grid(row=9, column=5, padx=2, pady=2)

        self.cam_21_label = tk.Label(self.cam_frame_right, text='Cam .21 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_21_label.grid(row=10, column=0, padx=2, pady=2)
        self.cam_21_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_21_rec_ping.grid(row=10, column=1, padx=2, pady=2)
        self.cam_21_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_21_rec_web.grid(row=10, column=2, padx=2, pady=2)
        self.cam_21_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_21_rec_flash.grid(row=10, column=3, padx=2, pady=2)
        self.cam_21_checkbox_value = tk.BooleanVar()
        self.cam_21_checkbox_value.set(False)
        self.cam_21_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_21_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_21_checkbox.grid(row=10, column=4, padx=2, pady=2)
        self.cam_21_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_21'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_21_reset_button.grid(row=10, column=5, padx=2, pady=2)

        self.cam_22_label = tk.Label(self.cam_frame_right, text='Cam .22 ', bg=BG_COLOR, fg=TXT_COLOR)
        self.cam_22_label.grid(row=11, column=0, padx=2, pady=2)
        self.cam_22_rec_ping = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_22_rec_ping.grid(row=11, column=1, padx=2, pady=2)
        self.cam_22_rec_web = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_22_rec_web.grid(row=11, column=2, padx=2, pady=2)
        self.cam_22_rec_flash = tk.Label(self.cam_frame_right, text='     ', bg=COLOR_OFF)
        self.cam_22_rec_flash.grid(row=11, column=3, padx=2, pady=2)
        self.cam_22_checkbox_value = tk.BooleanVar()
        self.cam_22_checkbox_value.set(False)
        self.cam_22_checkbox = tk.Checkbutton(self.cam_frame_right, variable=self.cam_22_checkbox_value, onvalue=True, offvalue=False, bg=BG_COLOR)
        self.cam_22_checkbox.grid(row=11, column=4, padx=2, pady=2)
        self.cam_22_reset_button = tk.Button(self.cam_frame_right, text=" R ", command=lambda: resetOneFlash('cam_22'), padx=2, pady=2, bg=BG_COLOR,
                                             fg=TXT_COLOR)
        self.cam_22_reset_button.grid(row=11, column=5, padx=2, pady=2)

        self.button_frame_left = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.button_frame_left.grid(row=1, column=0, padx=2, pady=2)
        self.button_frame_right = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.button_frame_right.grid(row=1, column=1, padx=2, pady=2)
        self.button_frame_vertical = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.button_frame_vertical.grid(row=0, column=2, padx=2, pady=2, sticky='new')

        self.test_button = tk.Button(self.button_frame_left, text='START\nCHECK', height=2, width=8, command=startCheckButton, padx=2, pady=2, font=font_arial,
                                     bg=STRT_BTN)
        self.test_button.grid(row=0, column=0, padx=2, pady=2)
        self.test_button = tk.Button(self.button_frame_left, text='STOP\nCHECK', height=2, width=8, command=stopCheckButton, padx=2, pady=2, font=font_arial,
                                     bg=STP_BTN)
        self.test_button.grid(row=0, column=1, padx=2, pady=2)

        self.reset_all_button = tk.Button(self.button_frame_right, text='RESET ALL', height=2, command=resetAllFlash, padx=2, pady=2, font=font_arial,
                                          bg=SHOW_BUTTON)
        self.reset_all_button.grid(row=0, column=1, padx=2, pady=2)

        self.makeExcelFile_button = tk.Button(self.button_frame_vertical, text='MAKE EXCEL', width=11, command=makeExcelFile, padx=2, pady=2,
                                              bg=COLOR_ON, fg='white')
        self.makeExcelFile_button.grid(row=0, column=0, padx=2, pady=10)
        self.checkAllFlash_button = tk.Button(self.button_frame_vertical, text='CHECK ALL', width=11, command=checkAllFlash, padx=1, pady=1,
                                              bg='lightgreen')
        self.checkAllFlash_button.grid(row=1, column=0, padx=2, pady=2)
        self.unCheckAllFlash_button = tk.Button(self.button_frame_vertical, text='UNCHECK ALL', width=11, command=unCheckAllFlash, padx=1, pady=1,
                                                bg='lightcoral')
        self.unCheckAllFlash_button.grid(row=2, column=0, padx=2, pady=2)
        self.show_thread_button = tk.Button(self.button_frame_vertical, text='SHOW\nTHREADS', width=11, command=showThreadButton, padx=1, pady=1,
                                            bg=SHOW_BUTTON, fg=TXT_COLOR)
        self.show_thread_button.grid(row=3, column=0, padx=2, pady=2)
        self.show_info_button = tk.Button(self.button_frame_vertical, text='SHOW\nINFO', width=11, command=showInfoButton, padx=1, pady=1,
                                          bg=SHOW_BUTTON, fg=TXT_COLOR)
        self.show_info_button.grid(row=4, column=0, padx=2, pady=2)

        self.open_file_button = tk.Button(self.button_frame_vertical, text='OPEN\nFILE', width=11, command=open_file, padx=1, pady=1, bg=BG_COLOR, fg=TXT_COLOR)
        self.open_file_button.grid(row=5, column=0, padx=2, pady=2)

        self.thread_pool = tk.Label(self.button_frame_vertical, text='maximum\nthread', bg=BG_COLOR, fg=TXT_COLOR)
        self.thread_pool.grid(row=6, column=0, padx=2, pady=2)

        self.plus_button = tk.Button(self.button_frame_vertical, text='+', width=11, command=plusTHREADPOOL, padx=1, pady=1, bg=BG_COLOR, fg=TXT_COLOR)
        self.plus_button.grid(row=7, column=0, padx=2, pady=2)

        self.thread_pool = tk.Label(self.button_frame_vertical, text=str(THREAD_POOL_MAX), bg=BG_COLOR, fg=TXT_COLOR)
        self.thread_pool.grid(row=8, column=0, padx=2, pady=2)

        self.minus_button = tk.Button(self.button_frame_vertical, text='-', width=11, command=minusTHREADPOOL, padx=1, pady=1, bg=BG_COLOR, fg=TXT_COLOR)
        self.minus_button.grid(row=9, column=0, padx=2, pady=2)

        if TEST_MODE:
            self.test_button = tk.Button(self.button_frame_vertical, text='test', width=11, command=test_button, padx=1, pady=1, bg=BG_COLOR, fg=TXT_COLOR)
            self.test_button.grid(row=10, column=0, padx=2, pady=2)

        self.text_frame = tk.LabelFrame(self.main_frame, text='Chosen file ', bg=BG_COLOR, fg=TXT_COLOR)
        self.text_frame.grid(row=2, column=0, padx=2, pady=2, sticky='ew', columnspan=3)

        self.text_filepath = tk.Text(self.text_frame, width=60, heigh=3, wrap=tk.WORD, bg=BG_COLOR, fg=TXT_FILE_COLOR)
        self.text_filepath.grid(row=2, column=0, padx=2, pady=2)
        if RESET_MODE:
            self.text_filepath.insert(tk.END, 'RESET MODE')
        elif TEST_MODE:
            self.text_filepath.insert(tk.END, 'TEST MODE')
        elif MSVK_MODE:
            self.text_filepath.insert(tk.END, 'MSVK MODE')
        elif RESET_MSVK_MODE:
            self.text_filepath.insert(tk.END, 'RESET MSVK MODE')
        else:
            self.text_filepath.insert(tk.END, 'no file')


class ThreadWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Threads')
        self.parent.wm_attributes('-topmost', True)
        # screen_width = self.parent.winfo_screenwidth() // 2
        # screen_height = self.parent.winfo_screenheight() // 2
        parent_width = main_window.winfo_width() + 20
        geometry = re.split(r"[x+]", main_window.geometry())
        if int(geometry[2]) + parent_width + 470 > self.parent.winfo_screenwidth():
            self.parent.geometry(f'+{int(geometry[2]) - parent_width}+{int(geometry[3])}')
        else:
            self.parent.geometry(f'+{int(geometry[2]) + parent_width}+{int(geometry[3])}')
        self.parent.resizable(False, False)

        self.main_frame = tk.Frame(parent)
        self.main_frame.grid(row=0, column=0)

        self.thread_list = tk.Text(self.main_frame, width=60, heigh=30, wrap=tk.WORD)
        self.thread_list.grid(row=0, column=0, padx=2, pady=2)

    def show_threads(self):
        self.thread_list['state'] = 'normal'
        self.thread_list.delete(1.0, tk.END)
        text = ''
        for thread in threading.enumerate():
            text += thread.getName() + '\n'
        self.thread_list.insert(tk.END, text)
        self.thread_list['state'] = 'disabled'


class CamInfoWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title('Cam info')
        self.parent.wm_attributes('-topmost', True)
        geometry = re.split(r"[x+]", main_window.geometry())
        self.parent.geometry(f'+{int(geometry[2])}+{int(geometry[3])}')
        self.parent.resizable(False, False)
        self.main_frame = tk.Frame(parent)
        self.main_frame.grid(row=0, column=0)
        self.cam_info = tk.Text(self.main_frame, width=60, heigh=30, wrap=tk.WORD)
        self.cam_info.grid(row=0, column=0, padx=2, pady=2)

    def update_info(self):
        self.cam_info['state'] = 'normal'
        self.cam_info.delete(1.0, tk.END)
        ips = []
        sns = []
        macs = []
        for cam_id in hosts:
            if hosts[cam_id][1] != '' and hosts[cam_id][2] != '':
                # print(f'{hosts[cam_id][1]}')
                ips.append(hosts[cam_id][0])
                sns.append(hosts[cam_id][1])
                macs.append(hosts[cam_id][2])
        table = pd.DataFrame({'IP': ips, 'SN': sns, 'MAC': macs})
        self.cam_info.insert(tk.END, table)
        self.cam_info['state'] = 'disabled'


class FirefoxWindow(object):
    def __init__(self, ip, window_id, position):
        print(f"Запуск {ip}")
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(680, 730)
        self.driver.set_window_position(position[0], position[1])
        self.driver.get(ip)
        self.ip = ip
        self.id = window_id

    def get(self, new_ip):
        self.ip = new_ip
        self.driver.get(new_ip)


class StartThreadFlash:
    def __init__(self, name, target, *args):
        global THREAD_POOL

        self.name = name
        self.target = target
        self.args = args

        while THREAD_POOL > THREAD_POOL_MAX - 1:
            time.sleep(random.uniform(0.5, 2))
        print(f'* * * thread FLASH \033[32m START \033[0m {self.name}')
        thread = threading.Thread(target=self.target, name=self.name, args=self.args)
        self.thread = thread
        thread.start()

    def join(self):
        self.thread.join()


class StartThread:
    def __init__(self, name, target, *args):
        self.name = name
        self.target = target
        self.args = args

        print(f'* * * thread \033[32m START \033[0m {self.name}')
        thread = threading.Thread(target=self.target, name=self.name, args=self.args)
        self.thread = thread
        thread.start()

    def join(self):
        self.thread.join()


def on_closing_main():
    stopAllThreads()
    main_window.destroy()


def on_closing_thread(thread_window):
    for thread in threading.enumerate():
        if thread.getName() == 'showThreadWindow':
            thread.do_run = False
    thread_window.destroy()


def on_closing_info(info_window):
    for thread in threading.enumerate():
        if thread.getName() == 'showInfoWindow':
            thread.do_run = False
    info_window.destroy()


def plusTHREADPOOL():
    global THREAD_POOL_MAX
    if THREAD_POOL_MAX < 10:
        THREAD_POOL_MAX += 1
        m_window.thread_pool.configure(text=str(THREAD_POOL_MAX))


def minusTHREADPOOL():
    global THREAD_POOL_MAX
    if THREAD_POOL_MAX > 2:
        THREAD_POOL_MAX -= 1
        m_window.thread_pool.configure(text=str(THREAD_POOL_MAX))


def open_file():
    global FILE
    global FILE_FOLDER
    file = filedialog.askopenfile(mode='r', filetypes=[('Bin Files', '*.bin')])
    if file:
        FILE = os.path.abspath(file.name)
        m_window.text_filepath.delete(1.0, tk.END)
        FILE_FOLDER = re.split(r'\\', FILE)[-2]
        m_window.text_filepath.insert(tk.END, 'Folder: ' + FILE_FOLDER + '\n' + 'Path: ' + FILE)
        logger_cam.info(f'FILE FOLDER: {FILE_FOLDER}\n                             FILE: {FILE}')
        # print(FILE_FOLDER[-2])
        # print(f'{FILE}')


def showThreadButton():
    find_thread = None
    for thread in threading.enumerate():
        if thread.name == f'showThreadWindow':
            find_thread = thread
    if find_thread is None:
        thread_window = tk.Toplevel(main_window)
        t_window = ThreadWindow(thread_window)
        thread_window.protocol("WM_DELETE_WINDOW", lambda: on_closing_thread(thread_window))
        StartThread('showThreadWindow', showThreadWindow, thread_window, t_window)


def showInfoButton():
    find_thread = None
    for thread in threading.enumerate():
        if thread.name == f'showInfoWindow':
            find_thread = thread
    if find_thread is None:
        info_window = tk.Toplevel(main_window)
        i_window = CamInfoWindow(info_window)
        info_window.protocol("WM_DELETE_WINDOW", lambda: on_closing_info(info_window))
        StartThread('showInfoWindow', showInfoWindow, info_window, i_window)


def showThreadWindow(thread_window, t_window):
    t = threading.currentThread()
    while getattr(t, "do_run", True) and thread_window.state() == 'normal':
        t_window.show_threads()
        time.sleep(0.5)


def showInfoWindow(info_window, i_window):
    t = threading.currentThread()
    while getattr(t, "do_run", True) and info_window.state() == 'normal':
        i_window.update_info()
        time.sleep(2)


def stopAllThreads():
    for thread in threading.enumerate():
        print(f'* * * thread \033[31m STOP \033[0m {thread.getName()}')
        thread.do_run = False


def stopCheckButton():
    for thread in threading.enumerate():
        if thread.getName() == 'thread_mikrotik_ether_status':
            print(f'* * * thread \033[31m STOP \033[0m {thread.getName()}')
            thread.do_run = False


def resetAllFlash():
    for cam_id in range(1, 23):
        getattr(m_window, f'cam_{cam_id}_rec_flash').configure(bg=COLOR_OFF)
        hosts[cam_id][1] = ''
        hosts[cam_id][2] = ''


def checkAllFlash():
    for cam_id in range(1, 23):
        getattr(m_window, f'cam_{cam_id}_checkbox_value').set(True)


def unCheckAllFlash():
    for cam_id in range(1, 23):
        getattr(m_window, f'cam_{cam_id}_checkbox_value').set(False)
        getattr(m_window, f'cam_{cam_id}_checkbox_value').set(False)


def resetOneFlash(cam_id):
    getattr(m_window, f'{cam_id}_rec_flash').configure(bg=COLOR_OFF)
    getattr(m_window, f'{cam_id}_checkbox_value').set(False)


def makeExcelFile():
    ips = []
    sns = []
    macs = []
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    for cam_id in hosts:
        if hosts[cam_id][1] != '' and hosts[cam_id][2] != '':
            # print(f'{hosts[cam_id][1]}')
            ips.append(hosts[cam_id][0])
            sns.append(hosts[cam_id][1])
            macs.append(hosts[cam_id][2])
    try:
        df = pd.DataFrame({'IP': ips, 'SN': sns, 'MAC': macs})
        df.to_excel(f'./cameras_info_{dt_string}_{FILE_FOLDER}.xlsx')
        logger_cam.info(f'make file ./cameras_info_{dt_string}_{FILE_FOLDER}.xlsx')
        print(pd.read_excel(f'./cameras_info_{dt_string}_{FILE_FOLDER}.xlsx'))
        # logger_cam.info(pd.read_excel(f'./cameras_info_{dt_string}_{FILE_FOLDER}.xlsx'))
        for cam_id in range(1, 23):
            hosts[cam_id][1] = ''
            hosts[cam_id][2] = ''
        try:
            os.system(f'start excel.exe cameras_info_{dt_string}_{FILE_FOLDER}.xlsx')
        except Exception:
            print(f'\033[31m Can not run file cameras_info_{dt_string}_{FILE_FOLDER}.xlsx \033[0m')
    except PermissionError:
        print(f'\033[31m Can not open file cameras_info_{dt_string}_{FILE_FOLDER}.xlsx \033[0m')


def checkURL(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except ConnectionError:
        return False
    else:
        return True


def ftpUpload(ftp_obj, path, ftype='TXT'):
    if ftype == 'RSC':
        with open(path) as fobj:
            ftp_obj.storlines('STOR ' + path, fobj)
    else:
        with open(path, 'rb') as fobj:
            ftp_obj.storbinary('STOR ' + path, fobj, 1024)


def thread_mikrotik_ether_status():
    def out_true(text):
        return "\033[42m {}\033[0m".format(text)

    def out_false(text):
        return "\033[41m {}\033[0m".format(text)

    t = threading.currentThread()
    while getattr(t, "do_run", True):
        status_string = ""
        status_cnt = 0
        try:
            cl.connect('192.168.3.1', username='admin', password='')
            for ether in range(1, 23):
                command = f"put [/interface ethernet get ether{ether} value-name=running]"
                (stdin, stdout, stderr) = cl.exec_command(command)
                time.sleep(0.1)
                for line in stdout.readlines():
                    if line[0:-2] == "true":
                        ethers_status.append(True)  # print(line, end = '')
                        status_cnt += 1
                    elif line[0:-2] == "false":
                        ethers_status.append(False)
            cl.close()
            for cam_id in range(1, 23):
                cam_ip = hosts.get(cam_id)[0]
                if i == 11:
                    status_string = status_string + "\n"
                if ethers_status[cam_id - 1]:
                    getattr(m_window, f'cam_{cam_id}_rec_ping').configure(bg=COLOR_ON)
                    status_string = status_string + out_true(f"{cam_id}-{ethers_status[cam_id - 1]} ")

                    if getattr(m_window, f'cam_{cam_id}_rec_web').cget("bg") == COLOR_OFF:
                        find_thread = None
                        for thread in threading.enumerate():
                            if thread.name == f"thread_web_ping_{cam_ip}_{cam_id}":
                                find_thread = thread
                        if find_thread is None:
                            time.sleep(random.random())
                            StartThread(f"thread_web_ping_{cam_ip}_{cam_id}", thread_camera_check_web, cam_ip, cam_id)
                elif not ethers_status[cam_id - 1]:
                    getattr(m_window, f'cam_{cam_id}_rec_ping').configure(bg=COLOR_OFF)
                    status_string = status_string + out_false(f"{cam_id}-{ethers_status[cam_id - 1]} ")
        except Exception as er:
            print(f'\n~~~\nSSH CONNECT ERROR\n\n{er}\n~~~\n')
        print(f'\n* * * Active ports: \033[32m {status_cnt} \033[0m')
        # print(status_string)
        ethers_status.clear()
        time.sleep(20)


def thread_camera_check_web(host, cam_id):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        if checkURL(f'http://{host}/'):
            # print(f'=== WEB PING === {host} \033[32m UP \033[0m')
            getattr(m_window, f'cam_{cam_id}_rec_web').configure(bg=COLOR_ON)

            if getattr(m_window, f'cam_{cam_id}_rec_flash').cget("bg") == COLOR_OFF and getattr(m_window, f'cam_{cam_id}_checkbox_value').get() is True:
                find_thread = None
                for thread in threading.enumerate():
                    if thread.name == f'thread_cam_flash_{host}_{cam_id}':
                        find_thread = thread
                if find_thread is None:
                    # print(f'flash {host}')
                    StartThreadFlash(f'thread_cam_flash_{host}_{cam_id}', thread_cam_flash, host, cam_id)

            time.sleep(10)
        else:
            getattr(m_window, f'cam_{cam_id}_rec_web').configure(bg=COLOR_OFF)
            time.sleep(10)
    print(f'* * * thread \033[31m STOP \033[0m {t.getName()}')


def thread_cam_flash(host, cam_id):
    global THREAD_POOL
    THREAD_POOL += 1
    t = threading.currentThread()
    start_time = time.time()
    try:
        find_pos = False
        box = []
        box_num = ''
        current_position = ''
        while not find_pos:
            for position in windows_pos_table:
                print(f'{cam_id}- box: {position} {windows_pos_table[position][0]}')
                time.sleep(1)
                if not windows_pos_table[position][0]:
                    find_pos = True
                    windows_pos_table[position][0] = True
                    # print(f'{position} free')
                    box = [windows_pos_table[position][1], windows_pos_table[position][2]]
                    box_num = windows_pos_table[position][0]
                    current_position = position
                    break
        driver = FirefoxWindow(f"http://{host}/", cam_id, box)
        try:
            if RESET_MODE or RESET_MSVK_MODE:
                cam_reset(driver)
            elif MSVK_MODE:
                web_instructions_msvk(driver)
            elif TEST_MODE:
                print('CAM_FLASH')
                time.sleep(random.randint(15, 25))
                driver.driver.close()
                windows_pos_table[current_position][0] = False
            else:
                web_instructions(driver, cam_id, box_num)
            time.sleep(1)
            # time.sleep(random.randint(5, 10))
            getattr(m_window, f'cam_{cam_id}_rec_flash').configure(bg=COLOR_ON)
            getattr(m_window, f'cam_{cam_id}_checkbox_value').set(False)
            new_time = time.time() - start_time
            now_time = time.ctime(time.time())
            print(f"--- Flash {host} %s seconds in %s ---" % (new_time, now_time))
            print("\n")
            THREAD_POOL -= 1
            print(f'* * * thread \033[31m STOP \033[0m {t.getName()}')
        except Exception as er:
            print(f'\n~~~\nWEB ERROR {host}\n\n{er}\n~~~\n')
            getattr(m_window, f'cam_{cam_id}_rec_flash').configure(bg='black')
            getattr(m_window, f'cam_{cam_id}_checkbox_value').set(False)
            THREAD_POOL -= 1
            print(f'* * * thread \033[31m STOP \033[0m {t.getName()}')
    except Exception as er:
        print(f'\n~~~\nSite not exist..  {host}\n\n{er}\n~~~\n')
        getattr(m_window, f'cam_{cam_id}_rec_flash').configure(bg='black')
        getattr(m_window, f'cam_{cam_id}_checkbox_value').set(False)
        THREAD_POOL -= 1
        print(f'* * * thread \033[31m STOP \033[0m {t.getName()}')


def web_instructions(window, cam_id, box_num):
    print(f"Дроплист языка {window.ip}")
    WebDriverWait(window.driver, 5).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, ".ui-custom-select-inputbox")))
    window.driver.find_element(By.CSS_SELECTOR, ".ui-custom-select-inputbox").click()
    print(f"Ввод языка {window.ip}")
    window.driver.find_element(By.CSS_SELECTOR, ".ui-custom-select-inputbox").send_keys("russ")
    print(f"Выбор языка {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".ui-custom-select-item")))
    window.driver.find_element(By.CSS_SELECTOR, ".ui-custom-select-item").click()
    print(f"Далее {window.ip}")
    try:
        WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Next")))
        window.driver.find_element(By.LINK_TEXT, "Next").click()
        time.sleep(0.500)
    except TimeoutException:
        WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Следующий шаг")))
        window.driver.find_element(By.LINK_TEXT, "Следующий шаг").click()
        time.sleep(0.500)

    print(f"Дроплист времени {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "time_zone_date_format")))
    window.driver.find_element(By.ID, "time_zone_date_format").click()
    print(f"Выбор времени {window.ip}")
    dropdown = window.driver.find_element(By.ID, "time_zone_date_format")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//option[. = 'День-Месяц-Год']")))
    dropdown.find_element(By.XPATH, "//option[. = 'День-Месяц-Год']").click()
    # print(f"? {window.ip}")
    # WebDriverWait(window.driver, 5).until(
    #     ec.visibility_of_element_located((By.CSS_SELECTOR, "#time_zone_date_format > option:nth-child(3)")))
    # window.driver.find_element(By.CSS_SELECTOR, "#time_zone_date_format > option:nth-child(3)").click()
    print(f"Синхронизация {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "syncPCBtn")))
    window.driver.find_element(By.ID, "syncPCBtn").click()
    print(f"Далее {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Следующий шаг")))
    window.driver.find_element(By.LINK_TEXT, "Следующий шаг").click()

    print(f"Ввод пароля {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.NAME, "newpwd")))
    window.driver.find_element(By.NAME, "newpwd").send_keys("admin2020")
    print(f"Клик подтверждения пароля {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.NAME, "newpwdcfm")))
    window.driver.find_element(By.NAME, "newpwdcfm").click()
    print(f"Ввод подтверждения пароля {window.ip}")
    window.driver.find_element(By.NAME, "newpwdcfm").send_keys("admin2020")
    print(f"Клик галка почты {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "devInit_mail_enable")))
    window.driver.find_element(By.ID, "devInit_mail_enable").click()
    print(f"Далее {window.ip}")
    try:
        WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Следующий шаг")))
        window.driver.find_element(By.LINK_TEXT, "Следующий шаг").click()
    except TimeoutException:
        WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Сохранить")))
        window.driver.find_element(By.LINK_TEXT, "Сохранить").click()

    print(f"Галка P2P {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.NAME, "access_check")))
    window.driver.find_element(By.NAME, "access_check").click()
    print(f"Ок {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "OK")))
    window.driver.find_element(By.LINK_TEXT, "OK").click()
    print(f"Далее {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Следующий шаг")))
    window.driver.find_element(By.LINK_TEXT, "Следующий шаг").click()

    print(f"Галка автообновление {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.NAME, "autocheck_check")))
    window.driver.find_element(By.NAME, "autocheck_check").click()
    print(f"Сохранить {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Сохранить")))
    window.driver.find_element(By.LINK_TEXT, "Сохранить").click()

    print(f"Ввод логина {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "login_user")))
    window.driver.find_element(By.ID, "login_user").value = ""
    window.driver.find_element(By.ID, "login_user").send_keys("admin")
    print(f"Клик пароля {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "login_psw")))
    window.driver.find_element(By.ID, "login_psw").click()
    print(f"Ввод пароля {window.ip}")
    window.driver.find_element(By.ID, "login_psw").send_keys("admin2020")

    print(f"Вход {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Вход")))
    window.driver.find_element(By.LINK_TEXT, "Вход").click()
    print(f"Настройки {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Настройки\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Настройки\')]").click()
    window.driver.execute_script("window.scrollTo(0,0)")
    time.sleep(2)
    print(f"Сеть {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Сеть\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Сеть\')]").click()
    time.sleep(0.500)
    print(f"TCP/IP {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'TCP/IP\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'TCP/IP\')]").click()
    time.sleep(1.500)

    print(f"Достаем MAC-адрес {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "NN_macadd")))
    mac = ""
    for number in range(6):
        time.sleep(0.2)
        elem = (
            window.driver.find_element(By.ID, "NN_macadd").find_elements(By.TAG_NAME, "input")[number]).get_attribute(
            "value")
        mac = mac + elem + ":"
    mac = mac[0:-1].upper()
    hosts[cam_id][2] = mac

    print(f"Информация {window.ip}")
    WebDriverWait(window.driver, 5).until(
        ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Информация\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Информация\')]").click()
    time.sleep(0.250)

    print(f"Версия {window.ip}")
    WebDriverWait(window.driver, 5).until(
        ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Версия\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Версия\')]").click()

    print(f"Достаем SN {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "v_serialnumber")))
    time.sleep(0.1)
    sn = window.driver.find_element(By.ID, "v_serialnumber").get_attribute("textContent")
    hosts[cam_id][1] = sn
    logger_cam.info(f'IP: {window.ip}   SN: {sn}    MAC: {mac}')
    print(f"Система {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Система\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Система\')]").click()
    time.sleep(1)

    print(f"Обновление системы {window.ip}")
    WebDriverWait(window.driver, 5).until(
        ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Обновление системы\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Обновление системы\')]").click()

    print(f"Выбор файла {window.ip}")
    time.sleep(0.250)
    window.driver.find_element(By.ID, "upg_upgrade").send_keys(FILE)

    print(f"Обновить {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "upg_update")))
    window.driver.find_element(By.ID, "upg_update").click()

    while not check_reboot(window):
        time.sleep(5)

    print(f"Close {window.ip}")
    windows_pos_table[box_num][0] = False
    window.driver.close()


def web_instructions_msvk(window):
    # print(f"Дроплист языка {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".ui-custom-select-inputbox")))
    window.driver.find_element(By.CSS_SELECTOR, ".ui-custom-select-inputbox").click()
    # print(f"Ввод языка {window.ip}")
    window.driver.find_element(By.CSS_SELECTOR, ".ui-custom-select-inputbox").send_keys("russ")
    # print(f"Выбор языка {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".ui-custom-select-item")))
    window.driver.find_element(By.CSS_SELECTOR, ".ui-custom-select-item").click()
    # print(f"Далее {window.ip}")
    try:
        WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Next")))
        window.driver.find_element(By.LINK_TEXT, "Next").click()
        time.sleep(0.500)
    except TimeoutException:
        WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Следующий шаг")))
        window.driver.find_element(By.LINK_TEXT, "Следующий шаг").click()
        time.sleep(0.500)

    # print(f"Дроплист времени {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "time_zone_date_format")))
    window.driver.find_element(By.ID, "time_zone_date_format").click()
    # print(f"Выбор времени {window.ip}")
    dropdown = window.driver.find_element(By.ID, "time_zone_date_format")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//option[. = 'День-Месяц-Год']")))
    dropdown.find_element(By.XPATH, "//option[. = 'День-Месяц-Год']").click()
    # print(f"? {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#time_zone_date_format > option:nth-child(3)")))
    window.driver.find_element(By.CSS_SELECTOR, "#time_zone_date_format > option:nth-child(3)").click()
    # print(f"Синхронизация {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "syncPCBtn")))
    window.driver.find_element(By.ID, "syncPCBtn").click()
    # print(f"Следующий шаг {window.ip}")
    try:
        WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Следующий шаг")))
        window.driver.find_element(By.LINK_TEXT, "Следующий шаг").click()
        time.sleep(0.500)
    except TimeoutException:
        WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Следующий шаг")))
        window.driver.find_element(By.LINK_TEXT, "Следующий шаг").click()
        time.sleep(0.500)

    # print(f"Ввод пароля {window.ip}")
    WebDriverWait(window.driver, 15).until(ec.visibility_of_element_located((By.NAME, "newpwd")))
    window.driver.find_element(By.NAME, "newpwd").send_keys("synergo2020")
    # print(f"Клик подтверждения пароля {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.NAME, "newpwdcfm")))
    window.driver.find_element(By.NAME, "newpwdcfm").click()
    # print(f"Ввод подтверждения пароля {window.ip}")
    window.driver.find_element(By.NAME, "newpwdcfm").send_keys("synergo2020")
    # print(f"Клик галка почты {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "devInit_mail_enable")))
    window.driver.find_element(By.ID, "devInit_mail_enable").click()
    # print(f"Далее {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Следующий шаг")))
    window.driver.find_element(By.LINK_TEXT, "Следующий шаг").click()
    time.sleep(0.500)

    # print(f"Галка P2P {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.NAME, "access_check")))
    window.driver.find_element(By.NAME, "access_check").click()
    # print(f"Ок {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "OK")))
    window.driver.find_element(By.LINK_TEXT, "OK").click()
    # print(f"Далее {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Следующий шаг")))
    window.driver.find_element(By.LINK_TEXT, "Следующий шаг").click()
    time.sleep(0.500)

    # print(f"Галка автообновление {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.NAME, "autocheck_check")))
    window.driver.find_element(By.NAME, "autocheck_check").click()
    # print(f"Сохранить {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Сохранить")))
    window.driver.find_element(By.LINK_TEXT, "Сохранить").click()
    time.sleep(0.500)

    # print(f"Ввод логина {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "login_user")))
    window.driver.find_element(By.ID, "login_user").value = ""
    # time.sleep(0.500)
    window.driver.find_element(By.ID, "login_user").send_keys("admin")
    # time.sleep(0.500)
    # print(f"Клик пароля {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "login_psw")))
    window.driver.find_element(By.ID, "login_psw").click()
    # time.sleep(0.500)
    # print(f"Ввод пароля {window.ip}")
    window.driver.find_element(By.ID, "login_psw").send_keys("synergo2020")
    # time.sleep(0.500)

    # print(f"Вход {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Вход")))
    window.driver.find_element(By.LINK_TEXT, "Вход").click()
    time.sleep(3)
    # print(f"Настройки {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Настройки\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Настройки\')]").click()
    time.sleep(2)

    # print(f"Система {window.ip}")
    window.driver.execute_script("window.scrollTo(0,0)")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Система\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Система\')]").click()
    time.sleep(1)

    # print(f"Общие настройки {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Общие настройки\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Общие настройки\')]").click()
    time.sleep(1)

    # print(f"Дата/Время {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#page_generalConfig > .u-tab > li:nth-child(2)")))
    window.driver.find_element(By.CSS_SELECTOR, "#page_generalConfig > .u-tab > li:nth-child(2)").click()
    time.sleep(1)

    # print(f"Галка NTP {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "gen_NTPEnable")))
    window.driver.find_element(By.ID, "gen_NTPEnable").click()

    # print(f"Ввод IP {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.ID, "gen_NTPServer")))
    window.driver.find_element(By.ID, "gen_NTPServer").click()
    time.sleep(0.5)
    window.driver.find_element(By.ID, "gen_NTPServer").send_keys(Keys.CONTROL + 'a')
    time.sleep(0.5)
    window.driver.find_element(By.ID, "gen_NTPServer").send_keys("172.16.100.6")

    # print(f"Сохранить {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Сохранить")))
    window.driver.find_element(By.LINK_TEXT, "Сохранить").click()
    time.sleep(0.500)

    # print(f"Ок {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "OK")))
    window.driver.find_element(By.LINK_TEXT, "OK").click()
    time.sleep(0.500)

    # print(f"Сеть {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Сеть\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Сеть\')]").click()
    time.sleep(0.500)

    # print(f"TCP/IP {window.ip}")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'TCP/IP\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'TCP/IP\')]").click()
    time.sleep(0.500)

    # print(f"Set IP {window.ip}")
    element = window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_IP > .u-input:nth-child(1)")
    actions = ActionChains(window.driver)
    actions.double_click(element).perform()
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#NN_IPV4_IP > .u-input:nth-child(1)")))
    window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_IP > .u-input:nth-child(1)").send_keys("172")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#NN_IPV4_IP > .u-input:nth-child(3)")))
    window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_IP > .u-input:nth-child(3)").send_keys("16")
    element = window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_IP > .u-input:nth-child(5)")
    actions = ActionChains(window.driver)
    actions.double_click(element).perform()
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#NN_IPV4_IP > .u-input:nth-child(5)")))
    window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_IP > .u-input:nth-child(5)").send_keys("100")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#NN_IPV4_IP > .u-input:nth-child(7)")))
    window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_IP > .u-input:nth-child(7)").send_keys("2")

    # print(f"Set gateway {window.ip}")
    element = window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_DG > .u-input:nth-child(1)")
    actions = ActionChains(window.driver)
    actions.double_click(element).perform()
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#NN_IPV4_DG > .u-input:nth-child(1)")))
    window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_DG > .u-input:nth-child(1)").send_keys("172")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#NN_IPV4_DG > .u-input:nth-child(3)")))
    window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_DG > .u-input:nth-child(3)").send_keys("16")
    element = window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_DG > .u-input:nth-child(5)")
    actions = ActionChains(window.driver)
    actions.double_click(element).perform()
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#NN_IPV4_DG > .u-input:nth-child(5)")))
    window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_DG > .u-input:nth-child(5)").send_keys("100")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#NN_IPV4_DG > .u-input:nth-child(7)")))
    window.driver.find_element(By.CSS_SELECTOR, "#NN_IPV4_DG > .u-input:nth-child(7)").send_keys("6")
    WebDriverWait(window.driver, 5).until(ec.visibility_of_element_located((By.LINK_TEXT, "Сохранить")))
    window.driver.find_element(By.LINK_TEXT, "Сохранить").click()

    time.sleep(5)
    window.driver.close()


def cam_reset(window):
    window.driver.find_element(By.ID, "login_user").send_keys("admin")
    if RESET_MODE:
        window.driver.find_element(By.ID, "login_psw").send_keys("admin2020")
    elif RESET_MSVK_MODE:
        window.driver.find_element(By.ID, "login_psw").send_keys("synergo2020")
    window.driver.find_element(By.LINK_TEXT, "Вход").click()
    WebDriverWait(window.driver, 5).until(ec.element_to_be_clickable((By.XPATH, "//span[contains(.,\'Настройки\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Настройки\')]").click()
    time.sleep(2)
    window.driver.execute_script("window.scrollTo(0,0)")
    WebDriverWait(window.driver, 5).until(
        ec.element_to_be_clickable((By.XPATH, "//span[contains(.,\'Система\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'Система\')]").click()
    time.sleep(0.250)
    WebDriverWait(window.driver, 5).until(
        ec.element_to_be_clickable((By.XPATH, "//span[contains(.,\'По умолчанию\')]")))
    window.driver.find_element(By.XPATH, "//span[contains(.,\'По умолчанию\')]").click()
    WebDriverWait(window.driver, 5).until(ec.element_to_be_clickable((By.LINK_TEXT, "Сброс данных")))
    window.driver.find_element(By.LINK_TEXT, "Сброс данных").click()
    WebDriverWait(window.driver, 5).until(ec.element_to_be_clickable((By.ID, "d_f_pwd")))
    window.driver.find_element(By.ID, "d_f_pwd").click()
    WebDriverWait(window.driver, 5).until(ec.element_to_be_clickable((By.ID, "d_f_pwd")))
    if RESET_MODE:
        window.driver.find_element(By.ID, "d_f_pwd").send_keys("admin2020")
    elif RESET_MSVK_MODE:
        window.driver.find_element(By.ID, "d_f_pwd").send_keys("synergo2020")
    WebDriverWait(window.driver, 5).until(ec.element_to_be_clickable((By.LINK_TEXT, "Сохранить")))
    window.driver.find_element(By.LINK_TEXT, "Сохранить").click()
    window.driver.close()


def check_reboot(window):
    try:
        WebDriverWait(window.driver, 2).until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,\'Перезагрзка..., ждите\')]")))
        return True
    except Exception:
        check_reboot(window)


def startCheckButton():
    if FILE != '' or RESET_MODE or TEST_MODE or MSVK_MODE or RESET_MSVK_MODE:
        StartThread(f'thread_mikrotik_ether_status', thread_mikrotik_ether_status)
    else:
        print('Choose file!')


def test_button():
    hosts[7][1] = '6G04C05PAGF4A8B'
    hosts[7][2] = 'AA:BB:CC:DD:EE:HH'


def isUpToDate(fileName, url):
    with open(fileName, "r") as f:
        file = f.read()
    urlcode = requests.get(url).text.replace('\r', '')

    e_file = file.encode('utf-8')
    localhash = hashlib.sha256(e_file).hexdigest()

    e_urlcode = urlcode.encode('utf-8')
    urlhash = hashlib.sha256(e_urlcode).hexdigest()
    if localhash == urlhash:
        return True
    else:
        return False


def update(path, url):
    # put __file__ in path to update current file
    for i in tqdm(range(1), desc="Downloading Updates..."):
        urllib.request.urlretrieve(url, path)


def checkForUpdates(path, url):
    if not isUpToDate(path, url):
        print('Found new version! Restart app after download update!')
        update(path, url)
        return True
    else:
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--reset':
            print('RESET MODE')
            RESET_MODE = True
        if sys.argv[1] == '--test':
            print('TEST MODE')
            TEST_MODE = True
        if sys.argv[1] == '--msvk':
            print('MSVK MODE')
            MSVK_MODE = True
        if sys.argv[1] == '--resetmsvk':
            print('RESET MSVK MODE')
            RESET_MSVK_MODE = True
    main_window = tk.Tk()
    font_arial = Font(family='Arial', size=11, weight=tk.font.BOLD)
    m_window = MainWindow(main_window)

    main_window.protocol("WM_DELETE_WINDOW", on_closing_main)
    main_window.mainloop()
