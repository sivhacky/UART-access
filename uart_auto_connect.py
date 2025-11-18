#!/usr/bin/env python3
import serial
import serial.tools.list_ports
import time
import random
import string

# ---------------------------------------------------
# CONFIGURATIONS (modify based on your test environment)
# ---------------------------------------------------

BAUD_RATES = [115200, 57600, 38400, 19200, 9600]
TIMEOUT = 2
LOGIN_PROMPTS = ["login:", "Login:", "username:"]
PASSWORD_PROMPTS = ["Password:", "password:"]
DEVICE_KEYWORD = ["#", ">", "$"]   # signs of shell access

# ---------------------------------------------------
# GENERATE RANDOM AUTH KEY (for authorized lab use)
# ---------------------------------------------------

def generate_random_key(length=10):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# ---------------------------------------------------
# FIND UART DEVICE (USB-UART adapter)
# ---------------------------------------------------

def detect_uart_adapter():
    ports = serial.tools.list_ports.comports()

    for port in ports:
        if "USB" in port.description or "UART" in port.description or "CH341" in port.description:
            print(f"[+] UART Adapter detected: {port.device}")
            return port.device
    
    print("[-] No UART-to-USB adapter detected.")
    return None

# ---------------------------------------------------
# TRY CONNECTING WITH DIFFERENT BAUD RATES
# ---------------------------------------------------

def try_baud_rates(device):
    for baud in BAUD_RATES:
        try:
            print(f"[+] Trying baud rate: {baud}")
            ser = serial.Serial(device, baudrate=baud, timeout=TIMEOUT)
            time.sleep(1)

            output = ser.read(200).decode(errors="ignore")
            if output.strip():
                print(f"[+] Possible valid baud rate detected: {baud}")
                ser.close()
                return baud
        
            ser.close()
        except Exception as e:
            print(f"[-] Error at baud {baud}: {e}")
            continue

    print("[-] No valid baud rate found.")
    return None

# ---------------------------------------------------
# AUTOMATIC LOGIN ATTEMPT (AUTHORIZED TESTING ONLY)
# ---------------------------------------------------

def attempt_login(device, baud):
    print("[+] Opening UART session...")
    ser = serial.Serial(device, baudrate=baud, timeout=TIMEOUT)
    time.sleep(1)

    random_key = generate_random_key()
    print(f"[+] Generated session key: {random_key}")

    buffer = ser.read(300).decode(errors="ignore")
    print("[UART OUTPUT INITIAL]:")
    print(buffer)

    # Detect a login prompt
    if any(p in buffer for p in LOGIN_PROMPTS):
        print("[+] Login prompt detected. Sending test username...")
        ser.write(b"root\n")
        time.sleep(1)

    buffer = ser.read(300).decode(errors="ignore")
    if any(p in buffer for p in PASSWORD_PROMPTS):
        print("[+] Password prompt detected. Sending random key (test)...")
        ser.write((random_key + "\n").encode())
        time.sleep(1)

    buffer = ser.read(500).decode(errors="ignore")
    print("[UART OUTPUT AFTER LOGIN]:")
    print(buffer)

    # Shell detection
    if any(sign in buffer for sign in DEVICE_KEYWORD):
        print("[+] Root / shell access detected (authorized environment).")
    else:
        print("[-] Shell not acquired. Device may require correct credentials.")

    ser.close()

# ---------------------------------------------------
# MAIN WORKFLOW
# ---------------------------------------------------

if __name__ == "__main__":
    print("[*] UART Auto-Connect Script Started...\n")

    uart_device = detect_uart_adapter()
    if not uart_device:
        exit()

    baud = try_baud_rates(uart_device)
    if not baud:
        exit()

    attempt_login(uart_device, baud)

    print("\n[*] Script Completed.")
