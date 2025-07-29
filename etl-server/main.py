import time
import zmq
from _thread import *
import threading
from validate import validate
from store import store
from clean import clean
from report import report
from queue import Queue
import os


work_in_progress = False
#Connect to socket and wait for messages from clients
#Send messages to validate() thread
#When clients indicate that they are done; Exit
def ingest(conxext, out_q):
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5555")
    print("socket binded to port 5555", flush=True)

    # put the socket into listening mode
    print("socket is listening", flush=True)

    count = 0
    while True:
            #  Wait for next request from client
#         print("Waiting for message", flush=True)
        message = socket.recv()
#         print("Received request: %s" % message, flush=True)
#         print("Message received", flush=True)
        if message == b"DONE":
            count+=1
            if count == 5:
                print("End of communication", flush=True)
                out_q.put(b"DONE")
                break
        #  Do some 'work'
        else:
            out_q.put(message)


##Thread creation
##Pass interthread communication method: queues
##Initialize socket to communicate with sensors
##Wait for threads to close
if __name__ == '__main__':
    if work_in_progress is True:
        context = zmq.Context()
        print("Not able to run server: under-development", flush=True)
        socket = context.socket(zmq.PULL)
        socket.bind("tcp://*:5555")
        count = 0
        while True:
                #  Wait for next request from client
    #         print("Waiting for message", flush=True)
            message = socket.recv()
    #         print("Received request: %s" % message, flush=True)
    #         print("Message received", flush=True)
            if message == b"DONE":
                count+=1
                if count == 5:
                    print("End of communication", flush=True)
                    break
            #  Do some 'work'
    else:
        print("working", flush=True);
        #Set up socket
        #connect to target database
        context = zmq.Context()

        #set up interprocess communication
        ingestToValidateQ = Queue()
        validateToCleanQ = Queue()
        cleanToReportQ = Queue()
        reportToStoreQ = Queue()


        t1 = threading.Thread(target=ingest, args=(context, ingestToValidateQ,))
        t2 = threading.Thread(target=validate, args=(ingestToValidateQ,validateToCleanQ,))
        t3 = threading.Thread(target=clean, args=(validateToCleanQ, cleanToReportQ,))
    #     t4 = threading.Thread(target=report, args=(cleanToReportQ, reportToStoreQ,))
    #     t5 = threading.Thread(target=store, args=(reportToStoreQ,))
        
        print("Starting ingestion thread", flush=True)
        t1.start()
        print("Starting validation thread", flush=True)
        t2.start()
        print("Starting cleaning thread", flush=True)
        t3.start()
        t1.join()
        print("Ingestion thread completed", flush=True)
        t2.join()
        print("Validation thread completed", flush=True)
        t3.join()
        print("Cleaning thread completed", flush=True)
    print("Done!")
