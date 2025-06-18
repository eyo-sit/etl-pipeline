from queue import Queue
import os

def clean(in_q, out_q):
    file_template = 'tmp_sensor_'

    location = 'tmp/'
    print("Hello")
    while True:
        data_message = in_q.get()

        if data_message == "DONE":
            print("Cleaning done")
            break
        else:
            print("Cleaning")
            print("Pulling data from database")
            print("Sending continue signal to validate")
            print("Done Cleaning round")
            print("Sending signal to store")

    #Get all csvs
    #change names of csv, forcing validate to make new file
    #send message to validate to continue
    #load csv into panda dataframe

