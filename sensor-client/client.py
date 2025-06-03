import zmq
import os
import csv
from datetime import datetime 
import time

if __name__ == '__main__':
    time.sleep(10)
    server_host = os.environ.get("SERVER_HOST", "etl-server")
    server_port = os.environ.get("SERVER_PORT", "5555")
    sensor_id = os.environ.get("SENSOR_ID", "unknown")

    context = zmq.Context()

    socket = context.socket(zmq.PUSH)
    socket.connect(f"tcp://{server_host}:{server_port}")

    path = '/data/missile_tracks_sensor_'  + sensor_id + '.csv'

    count = 0
    first_row = True
    previous_ts = None
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if first_row:
                first_row = False
                continue
            current_ts = datetime.fromtimestamp(int(row[0]))

            if previous_ts is not None:
                delay = (current_ts - previous_ts).total_seconds()
                time.sleep(max(delay, 0))

            socket.send(bytes(','.join(row), 'UTF-8'))
            previous_ts = current_ts
            if count == 50:
                break
            count+=1

    socket.send(b"DONE")
