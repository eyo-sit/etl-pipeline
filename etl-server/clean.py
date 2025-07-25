from queue import Queue
import os

curr_count = 0
last_cleaned = 0

def csv_to_df():
    pass
#     csv_list
   ## grab all csvs that end with the latest round _[]_last_cleaned.csv 
   ##put in list
   ##loop through list and import to df
       ##df = pd.read_csv
       ##add datafram to list
   ## return list


def clean(in_q, out_q):
    file_template = 'tmp_sensor_'

    location = 'tmp/'
    count = 1
    while True:
        data_message = in_q.get()

        if data_message == "DONE":
            print("Cleaning done", flush=True)
            break
        else:
            #clean data
            if data_message == "fail":
                print("Cleaning", flush=True)
                csv_cleanup(in_q)

                print("Done Cleaning round", flush=True)
                print("Sending signal to store", flush=True)
            elif data_message == "pass":
            ## if data doesn't need to be cleaned still message clean to send to target database
                print("Not cleaning", flush=True)
                csv_cleanup(in_q)
                print("Done Cleaning round", flush=True)
                print("Sending signal to store", flush=True)
            else:
                temp = count % 100000
                if temp == 0:
                    print("Cleaning expected pass or fail and received " + data_message)
                    print(temp)
                else:
                    count += 1
                in_q.put(data_message)
                

def csv_cleanup(in_q):
    global curr_count
    print("Cleaning up csv", flush=True)
    #Get all csvs
    for i in range(1,6):
        file = "tmp/tmp_sensor_" + str(i) + ".csv"
        fileExists = os.path.exists(file)
        if fileExists is True:
            os.rename(file, "tmp/tbcsensor_" + str(i)  + "_" + str(curr_count) + ".csv")
    curr_count+=1
    print("Letting validate know to continue", flush=True)
    in_q.put("CONTINUE")
    #change names of csv, forcing validate to make new file
    #send message to validate to continue
    #load csv into panda dataframe

