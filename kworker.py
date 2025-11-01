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
                "45.3.34.128:3129",
                "65.111.26.44:3129",
                "209.50.161.98:3129",
                "65.111.22.43:3129",
                "104.207.49.163:3129",
                "154.213.162.218:3129",
                "65.111.14.154:3129",
                "45.3.62.176:3129",
                "216.26.228.3:3129",
                "45.3.35.197:3129",
                "216.26.241.231:3129",
                "104.207.43.218:3129",
                "65.111.6.28:3129",
                "65.111.5.27:3129",
                "65.111.0.221:3129",
                "45.3.43.178:3129",
                "216.26.250.73:3129",
                "216.26.228.58:3129",
                "216.26.253.118:3129",
                "65.111.5.177:3129",
                "209.50.166.214:3129",
                "104.167.19.10:3129",
                "104.207.57.188:3129",
                "65.111.2.202:3129",
                "65.111.31.76:3129",
                "45.3.54.29:3129",
                "216.26.245.158:3129",
                "209.50.166.92:3129",
                "209.50.191.121:3129",
                "45.3.52.164:3129",
                "104.207.59.53:3129",
                "104.207.63.24:3129",
                "65.111.22.86:3129",
                "216.26.235.144:3129",
                "104.207.33.235:3129",
                "65.111.29.173:3129",
                "154.213.166.251:3129",
                "216.26.240.252:3129",
                "216.26.233.51:3129",
                "45.3.37.190:3129",
                "65.111.25.17:3129",
                "154.213.160.94:3129",
                "209.50.171.201:3129",
                "104.207.39.248:3129",
                "104.207.35.245:3129",
                "209.50.186.237:3129",
                "216.26.235.132:3129",
                "154.213.166.175:3129",
                "216.26.245.159:3129",
                "209.50.171.176:3129",
                "209.50.186.232:3129",
                "45.3.38.163:3129",
                "216.26.228.131:3129",
                "45.3.51.169:3129",
                "45.3.55.22:3129",
                "65.111.9.161:3129",
                "216.26.255.24:3129",
                "209.50.190.88:3129",
                "45.3.41.128:3129",
                "104.207.33.247:3129",
                "216.26.247.115:3129",
                "104.207.37.39:3129",
                "216.26.250.109:3129",
                "65.111.24.191:3129",
                "45.3.55.160:3129",
                "104.167.19.214:3129",
                "45.3.52.225:3129",
                "65.111.0.155:3129",
                "45.3.37.46:3129",
                "209.50.176.164:3129",
                "216.26.246.160:3129",
                "209.50.189.176:3129",
                "216.26.229.36:3129",
                "45.3.36.111:3129",
                "209.50.176.229:3129",
                "104.207.58.187:3129",
                "104.207.37.140:3129",
                "65.111.28.46:3129",
                "209.50.172.5:3129",
                "65.111.22.133:3129",
                "209.50.164.94:3129",
                "104.207.53.122:3129",
                "216.26.236.8:3129",
                "104.207.48.99:3129",
                "65.111.24.209:3129",
                "104.207.44.167:3129",
                "65.111.28.189:3129",
                "209.50.190.201:3129",
                "216.26.236.80:3129",
                "216.26.232.121:3129",
                "65.111.23.218:3129",
                "65.111.10.60:3129",
                "209.50.173.201:3129",
                "45.3.53.59:3129",
                "216.26.235.63:3129",
                "193.56.28.88:3129",
                "216.26.248.207:3129",
                "45.3.33.63:3129",
                "209.50.187.31:3129",
                "104.207.61.97:3129",
            ]



            Select_Proxy = random.choice(List_Proxy)

            browser = playwright.chromium.launch(proxy={"server": Select_Proxy, "username": "nyabik7003@gmail.com", "password": "Waluyo@1997"}, headless=headless, args=[
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
