/*
   B-intime V2 C++
*/

// Two modules MAX7219 4 in 1 connected in series to get 32×16 LED dotmatrix
#include <Redgick_MatrixMAX72XX.h>  // https://github.com/redgick/Redgick_GFX
Redgick_MatrixMAX72XX matrix;

#include <ESPNtpClient.h> // https://github.com/gmag11/ESPNtpClient/
#include <ESP8266WiFi.h>
#include <WiFiManager.h>  // https://github.com/tzapu/WiFiManager
#include <asyncHTTPrequest.h>  // https://github.com/boblemaire/asyncHTTPrequest + https://github.com/me-no-dev/ESPAsyncTCP
#include <ArduinoJson.h> // https://github.com/bblanchon/ArduinoJson

#define UPDATE_INTERVAL 1000
#define ONBOARDLED 2 // Built in LED
#define WIDTH 32

// globals
Screen screen(WIDTH, 16, MONOCHROME); // with, height, colors);
asyncHTTPrequest request;
DynamicJsonDocument doc(4096);

const PROGMEM char* ntpServer = "fr.pool.ntp.org";

static boolean syncEventTriggered = false; // True if a time even has been triggered
NTPEvent_t ntpEvent; // Last triggered event

static boolean sync_ok = false;
static char progress = 0;
static int ratp[3] = {};
static size_t ratp_size = 0;

Bitmap wifi_icon = Bitmap(7,7,"0x7d04e00100");

Bitmap font_8x8_characters[11] = {
  Bitmap(8, 8, "0x3c666e7666663c00"), // 48=0
  Bitmap(8, 8, "0x1818381818187e00"), // 49=1
  Bitmap(8, 8, "0x3c66060c30607e00"), // 50=2
  Bitmap(8, 8, "0x3c66061c06663c00"), // 51=3
  Bitmap(8, 8, "0x060e1e667f060600"), // 52=4
  Bitmap(8, 8, "0x7e607c0606663c00"), // 53=5
  Bitmap(8, 8, "0x3c66607c66663c00"), // 54=6
  Bitmap(8, 8, "0x7e660c1818181800"), // 55=7
  Bitmap(8, 8, "0x3c66663c66663c00"), // 56=8
  Bitmap(8, 8, "0x3c66663e06663c00"), // 57=9
  Bitmap(8, 8, "0x3c66060c18001800"), // 58=?
};
Font* font_8x8 = new Font(48, 58, ':', font_8x8_characters);

void print_8x8(Screen* sc, uint16_t x, uint16_t y, String s) {
  int offset = 0;
  for (int i = 0; i < s.length(); i++) {
    Bitmap bitmap = font_8x8->getBitmap(s[i]);
    sc->drawBitmap(x + offset, y, bitmap, 1);
    offset += bitmap.width;
  }
}

void processSyncEvent (NTPEvent_t ntpEvent) {
    switch (ntpEvent.event) {
        case timeSyncd:
        case partlySync:
            if(!sync_ok) {
              // hack force request at first sync
              progress = 100;
            }
            sync_ok = true;
        case syncNotNeeded:
        case accuracyError:
            Serial.printf ("[NTP-event] %s\n", NTP.ntpEvent2str (ntpEvent));
            break;
        default:
            break;
    }
}

void get_ratp() {
  if(request.readyState() == 0 || request.readyState() == 4){
    request.open("GET", "http://apixha.ixxi.net/APIX?keyapp=FvChCBnSetVgTKk324rO&cmd=getNextStopsRealtime&stopArea=383&line=20&&direction=40&apixFormat=json");
    request.send();
  }
}

void request_callback(void* optParm, asyncHTTPrequest* request, int readyState){
    if(readyState == 4){
        String res = request->responseText();
        //Serial.println(res);

        DeserializationError error = deserializeJson(doc, res);

        if (error) {
          Serial.print(F("deserializeJson() failed: "));
          Serial.println(error.f_str());
          return;
        }

        int list_len = 0;
        int wait_list[6] = {};

        JsonObject root_0 = doc["nextStopsOnLines"][0];
        //for (JsonObject root_0_nextStop : root_0["nextStops"].as<JsonArray>()) {
        //  int root_0_nextStop_waitingTime = root_0_nextStop["waitingTime"]; // 0, 360, 780, 900, 1260, 1680
        //  const char* root_0_nextStop_nextStopTime = root_0_nextStop["nextStopTime"];
        //  Serial.println(root_0_nextStop_waitingTime);
        //  Serial.println(root_0_nextStop_nextStopTime);
        //}

        JsonArray root_0_nextStops = root_0["nextStops"].as<JsonArray>();
        for (int idx = root_0_nextStops.size(); idx > 0; idx--) {
          JsonObject root_0_nextStop = root_0_nextStops[idx-1];
        
          int waitingTime = root_0_nextStop["waitingTime"]; // 0, 360, 780, 900, 1260, 1680
          //const char* nextStopTime_string = root_0_nextStop["nextStopTime"];

          if(list_len < 3 || waitingTime >= 240) {
            wait_list[list_len] = waitingTime / 60;
            list_len++;
          }
        }
        //Serial.print("result ");
        //for (int idx = 0; idx < list_len; idx++) {
        //  Serial.print(wait_list[idx]);
        //  Serial.print(" ");
        //}
        //Serial.println();

        ratp_size = min(3, list_len);
        for (int idx = 0; idx < ratp_size; idx++) {
          ratp[idx] = wait_list[list_len - 1 - idx];
        }        
    }
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  pinMode (ONBOARDLED, OUTPUT); // Onboard LED
  digitalWrite (ONBOARDLED, HIGH); // Switch off LED
  
  // Display initialization
  matrix.init();
  matrix.intensity(0);

  // screen message
  screen.print(1, 1, "B in");
  screen.print(5, 8, "time");
  matrix.display(screen.getBuffer());

  NTP.onNTPSyncEvent ([] (NTPEvent_t event) {
      ntpEvent = event;
      syncEventTriggered = true;
  });

  // Connecting to a wifi network using WiFiManager
  WiFiManager wifiManager;
  //wifiManager.erase(); // remove settings for testing
  wifiManager.setClass("invert"); // dark theme
  wifiManager.autoConnect("b-intime");

  // Connection acquired

  NTP.setTimeZone (TZ_Europe_Paris);
  // NTP.setInterval (600);
  // NTP.setNTPTimeout (NTP_TIMEOUT);
  // NTP.setMinSyncAccuracy (5000);
  // NTP.settimeSyncThreshold (3000);
  NTP.begin (ntpServer);

  //request.setDebug(true);
  request.onReadyStateChange(request_callback);

  get_ratp();
  
  //screen.print(27, 0, "c");
  screen.drawBitmap(24, 1, wifi_icon, 1);
  matrix.display(screen.getBuffer());
}

void debug_status() {
  Serial.print (NTP.getTimeDateStringUs ()); Serial.print (" ");
  Serial.print ("WiFi is ");
  Serial.print (WiFi.isConnected () ? "connected" : "not connected"); Serial.print (". ");
  Serial.print ("Uptime: ");
  Serial.print (NTP.getUptimeString ()); Serial.print (" since ");
  Serial.println (NTP.getTimeDateString (NTP.getFirstSyncUs ()));
  Serial.printf ("Free heap: %u\n", ESP.getFreeHeap ());
}

void loop() {
  static int next_round = 0;

  if (syncEventTriggered) {
      syncEventTriggered = false;
      processSyncEvent (ntpEvent);
  }

  if(millis() > next_round ) {
    next_round = millis() + UPDATE_INTERVAL;  

    if(sync_ok) {
      screen.clear();

      char strBuffer[6];
      time_t moment = time (NULL);
      tm* local_tm = localtime (&moment);
      strftime (strBuffer, sizeof(strBuffer), "%H%M", local_tm);
      print_8x8(&screen, 0, 0, strBuffer);
      //screen.print(1, 1, strBuffer);

      switch (ratp_size) {
        case 3:
          screen.print(22, 8, String(ratp[2]));
        case 2:
          screen.print(11, 8, String(ratp[1]));
        case 1:
          screen.print(1, 8, String(ratp[0]));
        default:
            break;
      }

      screen.setPixel(progress, 15, 1);
      screen.setPixel(progress+1, 15, 1);
      screen.setPixel(progress+2, 15, 1);
      if(progress == 28) {
        screen.setPixel(0, 15, 1);
      }
      if (progress == 29) {
        screen.setPixel(0, 15, 1);
        screen.setPixel(1, 15, 1);
      }
    } else {
      // /!\ no screen clear
      screen.setPixel((WIDTH >> 1) + progress, 15, 1);
      screen.setPixel((WIDTH >> 1) - 1 - progress, 15, 1);
    }

    progress += 1;

    if(!sync_ok && progress % 5 == 0) {
      debug_status();
    }

    if(progress >= 30) {
      progress = 1;
      debug_status();
      get_ratp();
    }

    matrix.display(screen.getBuffer());
  }

  delay(0);
}
