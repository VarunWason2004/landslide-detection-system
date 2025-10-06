#include <WiFi.h>
#include <DHT.h>

// Sensor pin setup
#define DHTPIN 2          // GPIO2 for DHT11
#define DHTTYPE DHT11
#define SOIL_PIN 34       // GPIO34 for soil moisture (analog input)
#define VIBRATION_PIN 27  // GPIO27 for vibration sensor (digital input)
#define BUZZER_PIN 25     // GPIO25 for buzzer (digital output)

// Replace with your WiFi credentials
const char* ssid = "Varun";
const char* password = "varung216";

DHT dht(DHTPIN, DHTTYPE);
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(VIBRATION_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Connect to WiFi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi Connected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String request = client.readStringUntil('\r');
    client.flush();

    // Read sensors
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    int soilMoisture = analogRead(SOIL_PIN);
    int vibration = digitalRead(VIBRATION_PIN);

    // Alarm: buzzer ON if vibration or high soil moisture
    if (vibration == HIGH || soilMoisture > 700) {
      digitalWrite(BUZZER_PIN, HIGH);
    } else {
      digitalWrite(BUZZER_PIN, LOW);
    }

    // Send response in JSON format
    String json = "{";
    json += "\"humidity\":" + String(humidity) + ",";
    json += "\"temperature\":" + String(temperature) + ",";
    json += "\"soil_moisture\":" + String(soilMoisture) + ",";
    json += "\"vibration\":" + String(vibration);
    json += "}";

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: application/json");
    client.println("Connection: close");
    client.println();
    client.println(json);
    client.stop();
  }
}

