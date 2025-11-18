Automated UART Interface Enumeration • Baud-Rate Validation • Controlled Authentication Test

This repository contains a Python-based automation tool designed for authorized IoT security assessments.
The script detects USB-UART adapters, validates baud rates, captures UART output, and performs safe, controlled authentication-key injection for debugging-interface testing on embedded devices.

This tool is useful for IoT Pentesters, hardware security researchers, and embedded device testers who need to streamline UART-based security assessments.

🔧 Features

✔ Auto-detect USB-to-UART adapters (CH341A, CP2102, FTDI, PL2303)
✔ Enumerate and validate baud rates automatically
✔ Capture boot logs and console output
✔ Generate random authentication keys for safe testing
✔ Perform controlled login attempts (authorized lab environments only)
✔ Detect shell prompts (#, $, >) to confirm access
✔ Clean UART session handling using pyserial

📁 Project Structure
uart-auto-enum-and-login/
│
├── uart_auto_connect.py      # Main automation script
├── README.md                 # Documentation
└── requirements.txt          # Dependencies

📌 Requirements

Python 3.8+

pyserial library

Install dependencies:

pip install -r requirements.txt


Contents of requirements.txt:

pyserial
