# 🌍 Landslide Detection System

This is an **IoT-based Landslide Detection System** that keeps track of **vibration**, **soil moisture**, **humidity**, and **temperature** using an ESP32 microcontroller.
Whenever the system senses unusual or risky conditions, it automatically sends an **email alert** and activates a **buzzer alarm**.
The main idea is to give early warnings and reduce damage in landslide-prone areas.

---

## 📸 Overview

This project combines both hardware and software parts.
It uses different sensors connected to an ESP32 board, which sends live data to a Python script running on a computer.
The script stores all readings in a CSV file and also sends an email alert if something abnormal is detected.

**Main Components:**

* **ESP32** – acts as the brain of the project, handling Wi-Fi communication and sensor readings
* **DHT11 sensor** – measures the temperature and humidity of the surroundings
* **Soil Moisture Sensor** – checks how wet the soil is, which helps detect heavy saturation
* **Vibration Sensor** – detects any shaking or sudden movement in the ground
* **Buzzer** – gives a local warning sound when danger is detected
* **Python Script** – saves the readings and handles the email alerts

---

## ⚙️ Features

* Real-time monitoring of all environmental parameters
* Stores sensor data in a CSV file for record keeping
* Sends email alerts when danger is detected
* Activates a buzzer when vibration or high soil moisture is found
* Uses a simple web server to send data from ESP32 to Python

---

## 🧠 System Architecture

```
[Sensors] → [ESP32 Web Server] → [Python Script]
                   ↓
              [CSV Logging]
                   ↓
            [Email Alert System]
```

---

## 🧩 Hardware Requirements

| Component                 | Quantity | Description                               |
| ------------------------- | -------- | ----------------------------------------- |
| ESP32                     | 1        | Microcontroller with built-in Wi-Fi       |
| DHT11                     | 1        | Temperature & Humidity sensor             |
| Soil Moisture Sensor      | 1        | Detects moisture or water content in soil |
| Vibration Sensor          | 1        | Detects tremors or shocks                 |
| Buzzer                    | 1        | Produces warning sound                    |
| Jumper Wires & Breadboard | -        | For making the circuit connections        |

---

## 💻 Software Requirements

* **Arduino IDE** (for uploading code to ESP32)
* **Python 3.8 or newer**
* Required Python libraries:

  ```bash
  pip install requests smtplib
  ```

---

## 🧱 Project Structure

```
Landslide-Detection-System/
│
├── esp32_code/
│   └── landslide_esp32.ino
│
├── python_script/
│   └── landslide_monitor.py
│
├── landslide_data.csv
│
└── README.md
```

---

## 🚀 Setup & Usage

### 🪛 1. Upload ESP32 Code

1. Open the `.ino` file in **Arduino IDE**.
2. Enter your Wi-Fi details:

   ```cpp
   const char* ssid = "Your_WiFi_Name";
   const char* password = "Your_WiFi_Password";
   ```
3. Upload the code to the ESP32.
4. After uploading, open the Serial Monitor to find the ESP32 IP address.

---

### 🐍 2. Run Python Script

1. Open `landslide_monitor.py` and update the settings:

   ```python
   ESP32_IP = "http://<your-esp32-ip>"
   SENDER_EMAIL = "your_email@gmail.com"
   SENDER_PASSWORD = "your_16_digit_app_password"
   RECEIVER_EMAIL = "receiver_email@gmail.com"
   ```
2. Run the script:

   ```bash
   python landslide_monitor.py
   ```
3. Once running, it will:

   * Continuously fetch data from the ESP32
   * Save readings to `landslide_data.csv`
   * Send alerts if danger levels are detected

---

## 📊 Example Output

```
Humidity: 68 %, Temp: 27.1 °C, Soil Moisture: 715, Vibration: 1
💾 Saved data at 2025-11-04 10:42:13
📧 Email alert sent successfully: 🚨 Landslide Warning Alert!
```

---

## ⚠️ Alert Conditions

| Parameter     | Condition | Action                  |
| ------------- | --------- | ----------------------- |
| Vibration     | HIGH      | Buzzer ON + Email Alert |
| Soil Moisture | > 700     | Buzzer ON + Email Alert |

---

## 📧 Email Setup Notes

* Use a **Gmail App Password** (16-digit) instead of your actual Gmail password.
* Make sure **2-Step Verification** is enabled on your Google account.
* Generate a new App Password from your Google Account → Security → App passwords.

---

## 📈 Future Improvements

* Add a rainfall sensor for more accurate detection
* Upload data to an online dashboard (ThingSpeak, Firebase, etc.)
* Develop a mobile app for live monitoring
* Add SMS alerts for instant warnings

---

## 🏁 Author

**Varun Wason**
📧 varunwason1@gmail.com
I really enjoyed building this project as it combines both hardware and software in a meaningful way.
It can be further improved to make a low-cost early warning system for hilly areas.

---


## 📜 License

© 2025 Varun [VARUN WASON]. All rights reserved.

This project is shared publicly for learning and demonstration purposes only.  
You may view and refer to the code, but copying, redistributing, or using it for commercial purposes is not allowed without permission.

