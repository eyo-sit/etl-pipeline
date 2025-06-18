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


#Connect to socket and wait for messages from clients
#Send messages to validate() thread
#When clients indicate that they are done; Exit
def ingest(conxext, out_q):
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5555")
    print("socket binded to port 5555")

    # put the socket into listening mode
    print("socket is listening")

    count = 0
    while True:
            #  Wait for next request from client
        message = socket.recv()
#         print("Received request: %s" % message, flush=True)
        if message == b"DONE":
            count+=1
            if count == 5:
                print("End of communication")
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

    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print("Done!")
