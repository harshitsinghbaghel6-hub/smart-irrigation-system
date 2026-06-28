/*
 * Smart Irrigation System — ESP32 Firmware
 * ==========================================
 * Reads soil moisture sensor and controls water pump
 * via relay based on configurable threshold.
 *
 * Hardware:
 *   - ESP32 Dev Module
 *   - FC-28 Soil Moisture Sensor → GPIO 34
 *   - 5V Relay Module            → GPIO 2
 *
 * Author: Harshit Singh | PSIT Kanpur
 */

// ── Pin Configuration ──────────────────────────
#define SOIL_SENSOR_PIN   34    // Analog input from soil sensor
#define RELAY_PIN          2    // Relay control (LOW = pump ON)
#define LED_PIN           13    // Built-in LED (status indicator)

// ── Threshold Settings ─────────────────────────
#define DRY_THRESHOLD     30    // Below this % → pump ON
#define WET_THRESHOLD     70    // Above this % → pump OFF
#define READ_INTERVAL   5000    // Read every 5 seconds (ms)

// ── Global Variables ───────────────────────────
int   moistureRaw    = 0;
float moisturePct    = 0.0;
bool  pumpStatus     = false;
long  lastReadTime   = 0;

// ── Calibration values (adjust for your sensor) ─
const int DRY_VALUE  = 4095;   // Raw value in air (dry)
const int WET_VALUE  =  800;   // Raw value in water (wet)


void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN,   OUTPUT);

  // Start with pump OFF
  digitalWrite(RELAY_PIN, HIGH);
  digitalWrite(LED_PIN,   LOW);

  Serial.println("=================================");
  Serial.println("  Smart Irrigation System v1.0  ");
  Serial.println("  PSIT Kanpur — Harshit Singh   ");
  Serial.println("=================================");
  Serial.println("FORMAT: MOISTURE_PCT,PUMP_STATUS");
  Serial.println("---------------------------------");
}


void loop() {
  long now = millis();

  if (now - lastReadTime >= READ_INTERVAL) {
    lastReadTime = now;

    // Read sensor
    moistureRaw = analogRead(SOIL_SENSOR_PIN);

    // Convert raw to percentage (0% = dry, 100% = wet)
    moisturePct = map(moistureRaw, DRY_VALUE, WET_VALUE, 0, 100);
    moisturePct = constrain(moisturePct, 0.0, 100.0);

    // Pump control logic
    if (moisturePct < DRY_THRESHOLD && !pumpStatus) {
      pumpON();
    } else if (moisturePct >= WET_THRESHOLD && pumpStatus) {
      pumpOFF();
    }

    // Send data over Serial (read by Python dashboard)
    Serial.print(moisturePct, 1);
    Serial.print(",");
    Serial.println(pumpStatus ? "ON" : "OFF");

    // Debug info
    Serial.print("  Raw: ");    Serial.print(moistureRaw);
    Serial.print("  Pct: ");    Serial.print(moisturePct);
    Serial.print("%  Pump: ");  Serial.println(pumpStatus ? "ON" : "OFF");
  }
}


void pumpON() {
  pumpStatus = true;
  digitalWrite(RELAY_PIN, LOW);    // LOW activates relay
  digitalWrite(LED_PIN,   HIGH);
  Serial.println("[ALERT] Soil DRY — Pump ACTIVATED");
}


void pumpOFF() {
  pumpStatus = false;
  digitalWrite(RELAY_PIN, HIGH);   // HIGH deactivates relay
  digitalWrite(LED_PIN,   LOW);
  Serial.println("[INFO]  Moisture OK — Pump STOPPED");
}
