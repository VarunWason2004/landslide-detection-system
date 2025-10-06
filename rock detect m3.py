import requests
import time

ESP32_IP = "http://192.168.137.197"  # Replace with the IP from Serial Monitor

def main():
    while True:
        try:
            response = requests.get(ESP32_IP + "/")
            if response.status_code == 200:
                data = response.json()
                print(f"Humidity: {data['humidity']} %, "
                      f"Temp: {data['temperature']} °C, "
                      f"Soil Moisture: {data['soil_moisture']}, "
                      f"Vibration: {data['vibration']}")

                # Example alarms
                if data['vibration'] == 1:
                    print("⚠️ VIBRATION DETECTED! Possible rockfall!")
                if data['soil_moisture'] > 700:
                    print("⚠️ HIGH SOIL MOISTURE! Risk of landslide!")

            else:
                print("Error: Bad response", response.status_code)

        except Exception as e:
            print("Error:", e)

        time.sleep(2)

if __name__ == "__main__":
    main()
