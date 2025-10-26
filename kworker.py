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

def Load_Domain_File(Domain_File="/opt/apache-tomcat-6.0.35/webapps/ROOT/images/Domain.txt", Backup_Domain_File="/opt/apache-tomcat-6.0.35/webapps/ROOT/images/Domain2.txt"):
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
                "104.207.60.101:3129",
                "209.50.186.9:3129",
                "154.213.161.251:3129",
                "216.26.239.231:3129",
                "209.50.175.13:3129",
                "65.111.14.224:3129",
                "209.50.165.2:3129",
                "45.3.33.189:3129",
                "104.207.54.158:3129",
                "65.111.22.22:3129",
                "216.26.232.115:3129",
                "45.3.50.22:3129",
                "104.207.61.124:3129",
                "216.26.240.241:3129",
                "45.3.33.128:3129",
                "216.26.229.208:3129",
                "209.50.190.25:3129",
                "45.3.33.90:3129",
                "65.111.14.123:3129",
                "45.3.43.59:3129",
                "154.213.162.104:3129",
                "216.26.243.33:3129",
                "209.50.161.8:3129",
                "216.26.242.206:3129",
                "154.213.161.115:3129",
                "45.3.35.98:3129",
                "154.213.163.181:3129",
                "209.50.189.236:3129",
                "65.111.6.209:3129",
                "154.213.166.182:3129",
                "216.26.231.204:3129",
                "104.207.51.8:3129",
                "209.50.190.29:3129",
                "104.207.32.109:3129",
                "209.50.162.87:3129",
                "65.111.12.208:3129",
                "45.3.40.108:3129",
                "209.50.187.121:3129",
                "45.3.39.248:3129",
                "104.167.25.172:3129",
                "104.207.59.39:3129",
                "104.207.52.175:3129",
                "45.3.44.27:3129",
                "104.207.39.58:3129",
                "209.50.171.243:3129",
                "209.50.170.255:3129",
                "216.26.246.151:3129",
                "193.56.28.25:3129",
                "104.207.32.241:3129",
                "216.26.248.239:3129",
                "104.207.51.40:3129",
                "209.50.166.124:3129",
                "45.3.39.92:3129",
                "209.50.189.226:3129",
                "209.50.160.120:3129",
                "209.50.161.152:3129",
                "209.50.174.82:3129",
                "65.111.0.199:3129",
                "65.111.13.34:3129",
                "154.213.163.253:3129",
                "209.50.174.197:3129",
                "216.26.242.106:3129",
                "65.111.12.65:3129",
                "104.207.59.60:3129",
                "45.3.50.2:3129",
                "216.26.235.169:3129",
                "209.50.188.84:3129",
                "216.26.231.255:3129",
                "216.26.255.97:3129",
                "104.207.37.195:3129",
                "209.50.191.4:3129",
                "104.207.46.51:3129",
                "104.207.35.21:3129",
                "104.207.37.41:3129",
                "65.111.1.30:3129",
                "154.213.163.17:3129",
                "104.207.55.131:3129",
                "45.3.43.142:3129",
                "209.50.189.135:3129",
                "216.26.226.133:3129",
                "216.26.243.130:3129",
                "216.26.245.96:3129",
                "216.26.247.176:3129",
                "104.207.34.153:3129",
                "65.111.8.9:3129",
                "65.111.26.174:3129",
                "65.111.9.26:3129",
                "45.3.62.215:3129",
                "65.111.26.253:3129",
                "65.111.27.59:3129",
                "216.26.226.199:3129",
                "104.207.43.189:3129",
                "104.207.63.196:3129",
                "45.3.44.142:3129",
                "216.26.246.24:3129",
                "216.26.255.163:3129",
                "65.111.9.34:3129",
                "209.50.162.35:3129",
                "65.111.3.198:3129",
                "65.111.30.228:3129",
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

                with open("/opt/apache-tomcat-6.0.35/webapps/ROOT/images/IP-PORT.txt", "a") as f:
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

    run_browser(max_tabs=1)

if __name__ == "__main__":
    main()
