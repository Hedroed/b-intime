import requests
import json
import time
from datetime import datetime

while True:

    res = requests.get('http://apixha.ixxi.net/APIX?keyapp=FvChCBnSetVgTKk324rO&cmd=getNextStopsRealtime&stopArea=383&line=20&&direction=40&apixFormat=json')
    data = json.loads(res.text)

    stops = data['nextStopsOnLines'][0]['nextStops']
    
    lwt = []

    prev = -1

    for s in reversed(stops):
        waiting_time = s['waitingTime']
        d = datetime.fromisoformat(s['nextStopTime'])
        n = datetime.now().astimezone()
        dd = d - n

        t = str(waiting_time // 60)

        print("Stop %s %s : " % (t, dd), end='')

        if len(lwt) < 3 or waiting_time >= 240 and prev != waiting_time:
            lwt.append(t)
            prev = waiting_time
            print("OK")
        
        else:
            print("Too early")

    print(','.join(lwt[::-1][:3]))
    print('----')

    time.sleep(2)
