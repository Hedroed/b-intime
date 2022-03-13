import max7219
from machine import Pin, SPI
import network
import time
import urequests
from sentry import SentryClient
import ujson
import ufont
# synchronize with ntp
# need to be connected to wifi
import ntptime
from machine import RTC
rtc = RTC()

ESSID = ""
PASSWD = ""

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ESSID, PASSWD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def init_display():
    spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
    display = max7219.Matrix8x8(spi, Pin(15), 8)
    display.brightness(0)

    return display

display = init_display()
display.fill(0)
display.text('time', 0, 0, 1)
display.text('ratp', 32, 0, 1)
display.show()

do_connect()

sentry = SentryClient('5646158', 'a14fd69cf7ef4586a2a1fc5004eef45a')

def main():

    slow_mode = False
    cnt = 1000
    wt = []
    while True:

        if cnt >= 31:
            cnt = 0
            wt = []

            try:
                ntptime.settime()
            except OSError:
                # NTP timeout
                pass
            d = rtc.datetime()
            h = d[4]
            m = d[5]
            display.fill(0)
            display.text("%02d%02d" % ((h+1)%24, m), 0, 0, 1)

            lwt = []
            try:
                res = urequests.get('http://apixha.ixxi.net/APIX?keyapp=FvChCBnSetVgTKk324rO&cmd=getNextStopsRealtime&stopArea=383&line=20&&direction=40&apixFormat=json')
            except OSError:
                # network error
                continue

            except Exception as e:
                display.text('E001', 32, 0, 1)
                display.show()
                sentry.send_exception(e)
                raise e

            try:
                data = ujson.loads(res.text)
            except ValueError:
                # error in json parsing
                continue

            except Exception as e:
                display.text('E002', 32, 0, 1)
                display.show()
                sentry.send_exception(e)
                raise e

            if 'nextStopsOnLines' in data and len(data['nextStopsOnLines']) and 'nextStops' in data['nextStopsOnLines'][0]:
                stops = data['nextStopsOnLines'][0]['nextStops']

                for s in reversed(stops):
                    waiting_time = s['waitingTime']
                    if waiting_time is not None and ( len(lwt) < 3 or waiting_time >= 240 ):
                        t = str(waiting_time // 60)
                        lwt.append(t)

                wt = lwt[::-1][:3]

                if len(wt) == 0:
                    slow_mode = True

                else:
                    slow_mode = False
                    if len(wt) >= 1:
                        ufont.draw_number(display, 33, 0, wt[0])

                    if len(wt) == 2:
                        if len(wt[1]) == 2:
                            ufont.draw_number(display, 44, 0, wt[1])
                        else:
                            ufont.draw_number(display, 46, 0, wt[1])
                            
                    elif len(wt) == 3:
                        w = 30 - (len(wt[0]) * 4 + len(wt[1]) * 4 + len(wt[2]) * 4)  # 30 is len with margin
                        ufont.draw_number(display, 32 + len(wt[0]) * 4 + w // 2, 0, wt[1])
                        ufont.draw_number(display, 62 - len(wt[2]) * 4, 0, wt[2])

            else:
                slow_mode = True

        display.hline(33,7,cnt,1)
        cnt += 1

        display.show()

        if slow_mode:
            time.sleep(4)
        else:
            time.sleep(1)

try:
    main()
except Exception as e:
    sentry.send_exception(e)
    raise e
