import re
import shutil
import subprocess
import socket
import string
import os
import json
import random
import requests
import traceback
import numpy as np
import heapq
import time
import tkinter as tk
import multiprocessing as mp
from tkinter import simpledialog, messagebox, filedialog
from playwright.sync_api import sync_playwright
from multiprocessing import Pool
from datetime import datetime

def check_internet(host="8.8.8.8", port=53, timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
        return True
    except socket.error:
        return False

def check_internet2(host="8.8.8.8", port=53, timeout=5):
    while True:
        try:
            socket.setdefaulttimeout(timeout)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
            print("-----------------------------------------------")
            print("Internet Connected...")
            return True
        except (socket.timeout, socket.gaierror, socket.herror, OSError) as e:
            print("-----------------------------------------------")
            print(f"Internet Disconnected... (Error: {e})")
            time.sleep(5)

def Load_Domain_File(Domain_File="Domain.txt", Backup_Domain_File="Domain2.txt"):
    try:
        with open(Domain_File, "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        
        if not lines:
            try:
                shutil.copy(Backup_Domain_File, Domain_File)
                with open(Domain_File, "r") as file:
                    lines = [line.strip() for line in file if line.strip()]

                if not lines:
                    return None, None, None
            except FileNotFoundError:
                return None, None, None

        random.shuffle(lines)
        SetDomain = lines.pop(0)
        with open(Domain_File, "w") as file:
            file.write("\n".join(lines) + "\n" if lines else "")

        return SetDomain
    except FileNotFoundError:
        print(f"File {Domain_File} tidak ditemukan. Tidak ada Domain yang tersedia.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    return None, None


def process_description(headless):

    GetIP_URL = "http://ip-api.com/json/"
    try:
        GetIP_Response = requests.get(GetIP_URL, timeout=5)
    
        if GetIP_Response.status_code == 200:
            GetIP_Data = GetIP_Response.json()
    
            GetIP = GetIP_Data.get('query', 'Unknown IP')
            Timezone = GetIP_Data.get('timezone', 'Unknown Timezone')

        else:
            print("Gagal mendapatkan data IP.")
    except requests.RequestException as e:
        print(f"Error saat menghubungi server: {e}")


    try:
        with sync_playwright() as playwright:

            List_Proxy = [
                "216.26.229.234:3129",
                "65.111.5.113:3129",
                "45.3.46.227:3129",
                "216.26.228.113:3129",
                "65.111.6.30:3129",
                "45.3.49.32:3129",
                "154.213.161.24:3129",
                "45.3.40.4:3129",
                "65.111.27.91:3129",
                "65.111.29.163:3129",
                "193.56.28.165:3129",
                "154.213.162.241:3129",
                "104.207.50.144:3129",
                "65.111.9.250:3129",
                "209.50.170.18:3129",
                "104.207.61.9:3129",
                "104.207.62.240:3129",
                "104.207.46.203:3129",
                "65.111.6.191:3129",
                "65.111.29.255:3129",
                "154.213.163.49:3129",
                "104.207.37.1:3129",
                "45.3.37.158:3129",
                "45.3.32.6:3129",
                "45.3.50.171:3129",
                "45.3.55.119:3129",
                "65.111.4.205:3129",
                "65.111.27.134:3129",
                "104.207.51.156:3129",
                "216.26.242.102:3129",
                "65.111.31.193:3129",
                "209.50.184.230:3129",
                "104.207.61.199:3129",
                "104.207.32.11:3129",
                "65.111.26.2:3129",
                "104.207.43.185:3129",
                "65.111.8.113:3129",
                "104.207.47.117:3129",
                "45.3.37.159:3129",
                "216.26.234.154:3129",
                "104.207.33.19:3129",
                "45.3.46.220:3129",
                "216.26.230.243:3129",
                "209.50.162.96:3129",
                "216.26.243.89:3129",
                "45.3.39.71:3129",
                "104.207.62.77:3129",
                "154.213.164.145:3129",
                "65.111.28.17:3129",
                "65.111.25.197:3129",
                "216.26.248.132:3129",
                "45.3.52.194:3129",
                "65.111.5.248:3129",
                "216.26.227.93:3129",
                "209.50.160.194:3129",
                "209.50.180.57:3129",
                "209.50.191.85:3129",
                "104.207.43.139:3129",
                "154.213.164.198:3129",
                "104.207.55.199:3129",
                "65.111.4.72:3129",
                "45.3.37.11:3129",
                "65.111.7.88:3129",
                "216.26.234.131:3129",
                "104.207.52.65:3129",
                "104.207.38.162:3129",
                "209.50.182.170:3129",
                "209.50.185.197:3129",
                "216.26.230.249:3129",
                "216.26.227.227:3129",
                "65.111.4.197:3129",
                "104.207.40.5:3129",
                "45.3.33.66:3129",
                "216.26.232.160:3129",
                "65.111.0.146:3129",
                "209.50.165.133:3129",
                "45.3.44.110:3129",
                "209.50.164.35:3129",
                "65.111.2.214:3129",
                "209.50.176.177:3129",
                "104.207.34.186:3129",
                "65.111.26.234:3129",
                "65.111.21.184:3129",
                "45.3.39.158:3129",
                "216.26.243.43:3129",
                "209.50.170.233:3129",
                "104.207.34.21:3129",
                "104.207.50.10:3129",
                "65.111.6.20:3129",
                "45.3.32.0:3129",
                "45.3.39.56:3129",
                "65.111.11.179:3129",
                "216.26.252.85:3129",
                "104.207.33.247:3129",
                "104.207.32.237:3129",
                "45.3.36.98:3129",
                "209.50.169.105:3129",
                "216.26.243.243:3129",
                "216.26.241.49:3129",
                "216.26.245.63:3129",
            ]

            Select_Proxy = random.choice(List_Proxy)

            browser = playwright.chromium.launch(proxy={"server": Select_Proxy, "username": "desagayau7@gmail.com", "password": "Waluyo@1997"}, headless=headless, args=[
                "--start-maximized"
            ])

            SetUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/109.0.0.0 Safari/537.36"
            SetDomain = Load_Domain_File()
            context = browser.new_context(user_agent=SetUserAgent, locale="en-US", timezone_id=Timezone, viewport={"width": 1920, "height": 1080})

            print(f"Public IP: {GetIP} | Timezone: {Timezone} | User-Agents: {SetUserAgent}")

            found = set()
            count = 0
            while count < 1:

                page = context.new_page()
                print("-----------------------------------------------")
                print(f"Set Domain: {SetDomain}")
                page.goto(SetDomain)

                page.wait_for_timeout(10000)
                page.keyboard.press("End")

                links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
                for link in links:
                    if "https://www.zoomeye.ai/searchResult?q=" in link:
                        found.add(link)
                

                OUTPUT_FILE = "Domain2.txt"
                try:
                    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                        existing = set(line.strip() for line in f if line.strip())
                except FileNotFoundError:
                    existing = set()
                
                all_links = existing.union(found)
                
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    for link in sorted(all_links):
                        f.write(link + "\n")

                html_content = page.content()
                
                ip_port_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}\b"
                matches = re.findall(ip_port_pattern, html_content)
                
                unique_matches = sorted(set(matches))
                
                result_text = '\n'.join(unique_matches)

                with open("IP-PORT.txt", "a") as f:
                    f.write(f"{result_text}\n")

                page.wait_for_timeout(5000)

                print("-----------------------------------------------")
                print(f"Auto Redirect: {page.url}")
                for tab in context.pages:
                    if tab != page:
                        tab.close()
                count += 1

            print("-----------------------------------------------")
            print("Waiting for internet disconnection...")
            context.clear_cookies()
            context.close()
            browser.close()

            print("-----------------------------------------------")
            print("Internet disconnected. Exiting program...")
            print("-----------------------------------------------\n")


    except Exception as e:
        print(f"An error occurred {e}")

def run_browser(max_tabs=1, headless=True):
    try:
        check_internet2()
        print("-----------------------------------------------")
        print("Launching Browser...")
        print("-----------------------------------------------")
        with mp.Pool(processes=max_tabs) as pool:
            for _ in range(max_tabs):
                pool.apply_async(process_description, (True,))
                time.sleep(5)
            pool.close()
            pool.join()

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    root = tk.Tk()
    root.withdraw()

    run_browser(max_tabs=1)

if __name__ == "__main__":
    main()
