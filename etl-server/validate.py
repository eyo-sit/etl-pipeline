from queue import Queue
import pandas as pd
import matplotlib.pyplot as plt
import os
from unpackage import unpackage
from soda.scan import Scan
import psycopg2
from config import load_stage_config
from connect import connect
from datetime import datetime
import json

sensor_data = []
columns = ['unix_timestamp','track_id','sensor_id','latitude','longitude','altitude','radiometric_intensity']
sensor_df = pd.DataFrame(columns=columns)

## Scan()

def soda_scan(out_q):

    scan = Scan()
    scan.set_data_source_name("etl_stage")
    scan.add_configuration_yaml_file(file_path="soda/configuration.yml")
    scan.add_sodacl_yaml_files("soda/checks.yml")
    
    scan.execute()
#     print(scan.get_logs_text())
    if scan.has_check_fails() :
        print("Some tests failed")
    else: 
       print("Tests did not fail")
    scan_results = scan.get_scan_results()
    checks = scan_results.get("checks")
    queries = scan_results.get("queries")
    with open("logs/sodaresult.txt", "a") as f:
       f.write("%s\n" % datetime.now())
#        f.write(scan.get_logs_text())
    with open("logs/resultex.json", "w") as f:
       json.dump(checks, f)

#     for check in checks:
#             if check.get("outcome") == "fail":
#                 diag = check.get("diagnostics")
#                 blocks = diag.get("blocks")
#                 first_block = blocks[0]
#                 query_name = first_block.get("failingRowsQueryName")
#                 sql
#                 with open("logs/sodaresultex.txt", "a") as f:
#                     f.write(check.get("name") + ": ")
#                     f.write(query_name)
#                     f.write(query_name + "\n")
    out_q.put("bleh")

    


## Process
## Determine which sensor the message is from
## parse message for missing values and correct to sql null value
## Insert into the table for that sensor
## Either create or append to csv for that sensor
def process(cursor, data_message):
    input_dict = unpackage(data_message)
    data = {k: v for k, v in input_dict.items() if v != ''}
    table = 'missile_tracks_sensor_'
    table += data.get('sensor_id')
    columns = ', '.join(data.keys())
    sql = "INSERT INTO " + table + " ( " + columns + " ) " + " VALUES ( " 
    if "unix_timestamp" in data:
        sql += data.get("unix_timestamp") 
    if "track_id" in data:
        sql += ", " + data.get("track_id") 
    if "sensor_id" in data:
        sql += ", " + data.get("sensor_id")
    if "latitude" in data:
        sql += ", " + data.get("latitude") 
    if "longitude" in data:
        sql += ", " + data.get("longitude") 
    if "altitude" in data:
        sql += ", " + data.get("altitude") 
    if "radiometric_intensity" in data:
        sql += ", " + data.get("radiometric_intensity") 
    sql += " )"
    cursor.execute(sql)

    #check if sensor has an active csv file
    file = location + file_template + data.get("sensor_id") + '.csv'
    print(file)

    isDirExist = os.path.exists(location)
    if isDirExist is True:  
        isFileExist = os.path.exists(file)
        #if it does
        if isFileExist is True:
            #append
#             with open(file) as f:
#                f.write(data_message)
            print("File exists!")

        #if not 
        else:
            #create and append
            print("File does not exist!")
#             with open(file) as f:
#                f.write(data_message)
    else:
            #create and append
            print("Directory does not exist")
#             with open(file) as f:
#                f.write(data_message)

###Validate()
## Initialize connection to staging database
## Send each message to process()
## if batch size is fulfilled or if end of message
##      run validation on batch
## Notify clean()
file_template = 'tmp_sensor_'
location = 'tmp/'
def validate(in_q, out_q):
    global sensor_df
    global table_template

    batch_size = 0
    config = load_stage_config()
    conn = connect(config)
    conn.autocommit = True
    cursor = conn.cursor()
    open("logs/sodaresult.txt",'w').close()
    while True:
        # Get some data
        data_message = in_q.get()
        if data_message == b"DONE":
            print("validation complete", flush=True)
            out_q.put("DONE")
            break
        else:
            # Process the data
            batch_size += 1
            process(cursor, data_message)


    # when a certain amount has been entered run soda
            if batch_size >= 90:
                batch_size = 0                
                soda_scan(out_q)
                # send to clean
#             else:
#                 print("Batch size is %s" % batch_size)
