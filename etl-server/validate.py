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
    print("Running soda scan", flush=True)

    ## init soda scan
    scan = Scan()
    scan.set_data_source_name("etl_stage")
    scan.add_configuration_yaml_file(file_path="soda/configuration.yml")
    scan.add_sodacl_yaml_files("soda/checks.yml")
    
    scan.execute()
#     print(scan.get_logs_text())
    
    ## let clean know if it needs to run
    if scan.has_check_fails() :
        print("Some tests failed", flush=True)
        out_q.put("fail")
    else: 

        ## if data doesn't need to be cleaned still message clean to send to target database
       print("Tests did not fail", flush=True)
       out_q.put("pass")
    scan_results = scan.get_scan_results()
    checks = scan_results.get("checks")
    queries = scan_results.get("queries")
    scan_output = scan.get_logs_text()

    ## write to scan logs
    with open("logs/sodaresult.txt", 'a') as f:
       f.write("**********%s**********\n" % datetime.now())
       f.write(scan_output)
       f.write("\n")
#        f.write(scan.get_logs_text())
    ##this could be used to tell clean() what to focus on/how to be more effiencent
    with open("logs/resultex.json", 'w') as f:
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
    print("Done scanning round")

    


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

    isDirExist = os.path.exists(location)
    isFileExist = os.path.exists(file)
    #if it does
    if isFileExist is True:
        #append
        with open(file, 'a') as f:
           f.write(data_message.decode() + "\n")
#             print("File exists!", flush=True)

    #if not 
    else:
        #create and append
#             print("File does not exist!", flush=True)
        print("Created file", flush=True)
        print(file, flush=True)
        with open(file, "a") as f:
           f.write(data_message.decode())
    print("Wrote to file", flush=True)

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
    ##Overwrite log and sensor dataframes
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    open("logs/sodaresult.txt",'w').close()
    print("Starting validation", flush=True)
    while True:
        # Get some data
        data_message = in_q.get()
        if data_message == b"DONE":
            #clean remaining data
            if batch_size != 0:
                print("Leftover batch size is " + str(batch_size), flush=True)
                batch_size = 0                
                soda_scan(out_q)
                result = out_q.get()
                while result != "CONTINUE":
                        out_q.put(result)
                        print("Validation recived " + result)
            else:
                print("Batch is empty")

            print("validation complete", flush=True)
            out_q.put("DONE")
            break
        else:
            # Process the data
            batch_size += 1
            process(cursor, data_message)


    # when a certain amount has been entered run soda
            if batch_size >= 90:
                print("Batch size reached, cleaning", flush=True)
                batch_size = 0                
                soda_scan(out_q)
                conn.commit()
                cursor.close()
                conn.close()
                while True:
                    print("waiting for cleaning", flush=True)
                    result = out_q.get()
                    if result == "CONTINUE":
                        print("Continuing validation", flush=True)
                        print("Clearing staging database", flush=True)
                        try:
                            print("Connecting to database", flush=True)
                            conn = connect(config)
                            conn.autocommit = True
                            cursor = conn.cursor()
                            print("Executing truncating", flush=True)
                            cursor.execute("DELETE FROM missile_tracks_sensor_1;")
                            print("Executed truncating", flush=True)
                            cursor.close()
                            conn.close()
                        except:
                            print("Error cleaning database")
#                             result = cursor.execute("TRUNCATE missile_tracks_sensor_2")
#                             conn.commit()
#                             print(result, flush=True)
#                             result = cursor.execute("TRUNCATE missile_tracks_sensor_3")
#                             conn.commit()
#                             print(result, flush=True)
#                             result = cursor.execute("TRUNCATE missile_tracks_sensor_4")
#                             conn.commit()
#                             print(result, flush=True)
#                             result = cursor.execute("TRUNCATE missile_tracks_sensor_5")
#                             conn.commit()
#                             print(result, flush=True)
                        print("Cleared staging database", flush=True)
                        break
                    else:
                        print("Validation expected CONTINUE but recieved: " + result)
                        out_q.put(result)
                conn = connect(config)
                conn.autocommit = True
                cursor = conn.cursor()
                # send to clean
#             else:
#                 print("Batch size is %s" % batch_size)
