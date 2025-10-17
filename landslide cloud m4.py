import requests
import time
import csv
import os
from datetime import datetime

ESP32_IP = "http://192.168.137.52"  # Replace with your ESP32 IP
CSV_FILE = "landslide_data.csv"

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

def main():
    initialize_csv()
    while True:
        try:
            response = requests.get(ESP32_IP + "/")
            if response.status_code == 200:
                data = response.json()

                # Print live data
                print(f"Humidity: {data['humidity']} %, "
                      f"Temp: {data['temperature']} °C, "
                      f"Soil Moisture: {data['soil_moisture']}, "
                      f"Vibration: {data['vibration']}")

                # Save data locally
                save_to_csv(data)

                # Example alerts
                if data["vibration"] == 1:
                    print("⚠️ VIBRATION DETECTED! Possible rockfall!")
                if data["soil_moisture"] > 25:
                    print("⚠️ HIGH SOIL MOISTURE! Risk of landslide!")

            else:
                print("Error: Bad response", response.status_code)

        except Exception as e:
            print("Error:", e)

        # Adjust sampling frequency here
        time.sleep(1)  # every second

if __name__ == "__main__":
    main()
