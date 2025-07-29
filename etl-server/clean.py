from queue import Queue
import os
import pandas as pd

last_cleaned = 0

def csv_to_df(toClean):
#     csv_list
   ## grab all csvs that end with the latest round _[]_last_cleaned.csv 
   global last_cleaned
   df_list = []
   
   if(toClean):
       print("creating dataframe list")
       for i in range(1,6):
           file = "tmp/tbc_sensor_" + str(i) + "_" + str(last_cleaned) + ".csv"
           fileExists = os.path.exists(file)
           #change names of csv, forcing validate to make new file
           if fileExists is True:
               #TODO clean oldest csv
                print("File: " + file + " found", flush=True)
               ##put in list
                curr_df = pd.read_csv(file)
                df_list.append(curr_df)
                print("File added to dataframe", flush=True)
                os.remove(file)
           else:
                print("File: " + file + " not found", flush=True)
   else:
       print("no dataframes neeeded")
       for i in range(1,6):
           file = "tmp/tbc_sensor_" + str(i) + "_" + last_cleaned + ".csv"
           fileExists = os.path.exists(file)
           #change names of csv, forcing validate to make new file
           if fileExists is True:
                print("File: " + file + " found", flush=True)
                os.remove(file)
           else:
                print("File: " + file + " not found", flush=True)
   ## return list
   last_cleaned += 1
   return df_list


def clean(in_q, out_q):
    file_template = 'tmp_sensor_'

    location = 'tmp/'
    while True:
        data_message = in_q.get()

        if data_message == "DONE":
            print("Cleaning done", flush=True)
            break
        else:
            #clean data
            if data_message == "fail":
                print("Cleaning", flush=True)
                #TODO add csvs to dataframe one for each sensors
                dataframe_list = csv_to_df(True)
                # remove csvs for the current round
                #clean 
                print("Done Cleaning round", flush=True)
                print("Sending signal to store", flush=True)
            elif data_message == "pass":
            ## if data doesn't need to be cleaned still message clean to send to target database
                print("Not cleaning", flush=True)
                #TODO # remove csvs for the current round
                csv_to_df(False)
                print("Done Cleaning round", flush=True)
                print("Sending signal to store", flush=True)
            else:
                in_q.put(data_message)
                

# def csv_cleanup(in_q):
#     global curr_count
#     print("Cleaning up csv", flush=True)
#     #Get all csvs
#     for i in range(1,6):
#         file = "tmp/tmp_sensor_" + str(i) + ".csv"
#         fileExists = os.path.exists(file)
#         #change names of csv, forcing validate to make new file
#         if fileExists is True:
#             os.rename(file, "tmp/tbcsensor_" + str(i)  + "_" + str(curr_count) + ".csv")
#             
#     curr_count+=1
#     print("Letting validate know to continue", flush=True)
#     #send message to validate to continue
#     in_q.put("CONTINUE")
#     #load csv into panda dataframe

