from queue import Queue
import pandas as pd
import matplotlib.pyplot as plt
from connect import connect
import os

sensor_data = []
columns = ['unix_timestamp','track_id','sensor_id','latitude','longitude','altitude','radiometric_intensity']
sensor_df = pd.DataFrame(columns=columns)

def process(cursor):
    #TODO when a certain amount has been entered run soda
    print("I should process")
    #TODO send to clean

def validate(in_q, out_q):
    global sensor_df
    batch_size = 0
    conn = connect(
            os.environ["STAGE_DB_HOST"],
            os.environ["STAGE_DB_NAME"],
            os.environ["STAGE_DB_USER"],
            os.environ["STAGE_DB_PASS"],
            os.environ.get("STAGE_DB_PORT", "5432"),
            )
    cursor = conn.cursor()

    while True:
        # Get some data
        data = in_q.get()
        # Process the data
        if data == b"DONE":
            print("validation complete", flush=True)
            break
        else:
            batch_size += 1
            #TODO unwrap dict into sql command and insert into stage

            if batch_size >= 100:
                process(cursor)
                batch_size = 0                
                print("reseting dataframe")


