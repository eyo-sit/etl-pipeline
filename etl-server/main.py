from connect import connect
import time
import zmq
from _thread import *
import threading
from unpackage import unpackage
from validate import validate
from store import store
from clean import clean
from report import report
from queue import Queue
import os



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
            out_q.put(unpackage(message))


if __name__ == '__main__':
    print("working", flush=True);
    #Set up socket
    #connect to target database
    conn = connect(
            os.environ["DB_HOST"],
            os.environ["DB_NAME"],
            os.environ["DB_USER"],
            os.environ["DB_PASS"],
            os.environ.get("DB_PORT", "5432"),
            )
    cursor = conn.cursor()
    exit
    context = zmq.Context()

    ingestToValidateQ = Queue()
    validateToCleanQ = Queue()
    cleanToReportQ = Queue()
    reportToStoreQ = Queue()


    t1 = threading.Thread(target=ingest, args=(context, ingestToValidateQ,))
    t2 = threading.Thread(target=validate, args=(ingestToValidateQ,validateToCleanQ,))
#     t3 = threading.Thread(target=clean, args=(validateToCleanQ, cleanToReportQ,))
#     t4 = threading.Thread(target=report, args=(cleanToReportQ, reportToStoreQ,))
#     t5 = threading.Thread(target=store, args=(reportToStoreQ,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Done!")
