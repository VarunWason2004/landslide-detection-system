import requests
import time
import csv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# === Configuration ===
ESP32_IP = "http://192.168.137.24"  # Replace with your ESP32 IP
CSV_FILE = "landslide_data.csv"

# Email settings
SENDER_EMAIL = "rocketnaman27@gmail.com"
SENDER_PASSWORD = "ipcvnzzvpbrjxwid"  # Replace with your 16-char Gmail App Password
RECEIVER_EMAIL = "varunwason1@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port (more reliable than 587 STARTTLS)

# === Functions ===

def initialize_csv():
    """Create the CSV file with headers if it doesn’t exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Humidity", "Temperature", "Soil_Moisture", "Vibration"])
        print(f"✅ Created new data file: {CSV_FILE}")

def save_to_csv(data):
    """Append one line of sensor data to the CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            timestamp,
            data["humidity"],
            data["temperature"],
            data["soil_moisture"],
            data["vibration"]
        ])
    print(f"💾 Saved data at {timestamp}")

def send_email_alert(subject, message, retries=3):
    """Send an email alert with automatic retry on failure."""
    for attempt in range(1, retries + 1):
        try:
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = RECEIVER_EMAIL
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)

            print(f"📧 Email alert sent successfully: {subject}")
            return True

        except Exception as e:
            print(f"❌ Attempt {attempt}/{retries} - Failed to send email: {e}")
            time.sleep(5)  # Wait before retrying

    print("🚫 All retry attempts failed. Email not sent.")
    return False

def main():
    initialize_csv()
    last_alert_time = 0  # to prevent spam
    alert_cooldown = 60  # seconds between alerts

    while True:
        try:
            response = requests.get(ESP32_IP + "/")
            if response.status_code == 200:
                data = response.json()

                print(f"Humidity: {data['humidity']} %, "
                      f"Temp: {data['temperature']} °C, "
                      f"Soil Moisture: {data['soil_moisture']}, "
                      f"Vibration: {data['vibration']}")

                save_to_csv(data)

                current_time = time.time()
                alert_message = ""

                # Check danger conditions
                if data["vibration"] == 1:
                    alert_message += "⚠️ VIBRATION DETECTED! Possible rockfall!\n"
                if data["soil_moisture"] > 700:
                    alert_message += "⚠️ HIGH SOIL MOISTURE! Risk of landslide!\n"

                # Send alert if needed and cooldown passed
                if alert_message and (current_time - last_alert_time > alert_cooldown):
                    send_email_alert("🚨 Landslide Warning Alert!", alert_message)
                    last_alert_time = current_time

            else:
                print(f"⚠️ ESP32 responded with status: {response.status_code}")

        except requests.exceptions.ConnectionError:
            print("🌐 Could not connect to ESP32. Retrying...")
        except Exception as e:
            print("❌ Error in main loop:", e)

        time.sleep(2)  # Poll every 2 seconds

# === Run Script ===
if __name__ == "__main__":
    # Quick test of email system before main loop (optional)
    # send_email_alert("Test Email", "✅ This is a test of the landslide alert system.")
    main()
