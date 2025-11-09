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
                "154.213.163.238:3129",
                "65.111.31.177:3129",
                "209.50.180.53:3129",
                "216.26.228.80:3129",
                "209.50.167.5:3129",
                "216.26.251.22:3129",
                "216.26.252.231:3129",
                "209.50.190.10:3129",
                "104.207.43.134:3129",
                "104.207.40.64:3129",
                "45.3.37.141:3129",
                "65.111.25.16:3129",
                "65.111.27.26:3129",
                "65.111.22.225:3129",
                "45.3.33.78:3129",
                "104.207.32.50:3129",
                "209.50.180.51:3129",
                "209.50.178.229:3129",
                "65.111.2.124:3129",
                "209.50.160.131:3129",
                "45.3.32.49:3129",
                "45.3.37.15:3129",
                "209.50.190.58:3129",
                "209.50.163.226:3129",
                "216.26.240.106:3129",
                "216.26.254.64:3129",
                "45.3.32.21:3129",
                "209.50.168.205:3129",
                "154.213.161.52:3129",
                "104.207.35.228:3129",
                "209.50.177.214:3129",
                "45.3.36.68:3129",
                "216.26.230.167:3129",
                "209.50.191.97:3129",
                "104.207.40.28:3129",
                "104.207.54.45:3129",
                "65.111.29.16:3129",
                "104.207.62.237:3129",
                "216.26.250.55:3129",
                "216.26.224.18:3129",
                "65.111.27.10:3129",
                "209.50.167.20:3129",
                "65.111.4.204:3129",
                "45.3.49.169:3129",
                "104.207.56.202:3129",
                "154.213.166.142:3129",
                "216.26.236.122:3129",
                "104.207.42.45:3129",
                "216.26.236.56:3129",
                "209.50.161.233:3129",
                "209.50.171.133:3129",
                "209.50.177.166:3129",
                "209.50.181.160:3129",
                "154.213.162.230:3129",
                "209.50.160.86:3129",
                "216.26.237.123:3129",
                "45.3.38.166:3129",
                "209.50.177.84:3129",
                "65.111.20.51:3129",
                "45.3.49.164:3129",
                "65.111.10.73:3129",
                "104.207.35.81:3129",
                "209.50.185.214:3129",
                "209.50.182.186:3129",
                "65.111.24.74:3129",
                "65.111.30.180:3129",
                "154.213.163.44:3129",
                "216.26.249.237:3129",
                "65.111.25.110:3129",
                "65.111.22.118:3129",
                "209.50.188.112:3129",
                "45.3.47.207:3129",
                "104.167.25.198:3129",
                "216.26.226.77:3129",
                "104.207.53.171:3129",
                "104.207.32.229:3129",
                "209.50.169.84:3129",
                "65.111.9.223:3129",
                "216.26.245.232:3129",
                "65.111.20.58:3129",
                "45.3.40.157:3129",
                "216.26.233.186:3129",
                "216.26.249.109:3129",
                "216.26.229.156:3129",
                "209.50.180.222:3129",
                "65.111.8.65:3129",
                "209.50.183.110:3129",
                "216.26.253.229:3129",
                "209.50.174.177:3129",
                "45.3.43.163:3129",
                "45.3.34.247:3129",
                "216.26.234.233:3129",
                "104.207.44.50:3129",
                "45.3.52.85:3129",
                "65.111.31.105:3129",
                "104.207.38.30:3129",
                "209.50.175.20:3129",
                "216.26.247.15:3129",
                "45.3.50.158:3129",
                "216.26.236.198:3129",
            ]



            Select_Proxy = random.choice(List_Proxy)

            browser = playwright.chromium.launch(proxy={"server": Select_Proxy, "username": "mancingb652@gmail.com", "password": "Waluyo@1997"}, headless=headless, args=[
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
                

                OUTPUT_FILE = "/opt/apache-tomcat-6.0.35/webapps/ROOT/images/Domain2.txt"
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
