import sys
from grpc_requests import StubClient
from replication_pb2 import DESCRIPTOR
import json

from datetime import datetime
import psycopg2
from psycopg2.extras import LogicalReplicationConnection
from psycopg2.extras import StopReplication


service_descriptor = DESCRIPTOR.services_by_name['Replicator']


client = StubClient.get_by_endpoint(
    "localhost:50051", service_descriptors=[service_descriptor, ])
assert client.service_names == ["Replicator"]
replicator = client.service("Replicator")
# Function to keep consuming data from postgres till message is 'stop_repl'
def consume(msg):
    print(msg.payload)
    
    if 'stop_repl' in msg.payload: 
        raise StopReplication()
    else:
        data_request = []
        
        
        count = 0
        jsontest = msg.payload.split('\n')
        for line in jsontest: #for each line start for client streaming
            count += 1
            print(len(line))
            print('<********* ', count, ' *********>')
            appendData= {"partofquery": line}
            print(json.dumps(appendData))
            
            data_request.append({"partofquery": line})
            
            if line == '}\n':
                break #break whil end of json 
        print("Requested Data ", data_request) 
        result = replicator.Replicate(data_request) #send to Replicate grpc
        print(result["status"], " Status")
    msg.cursor.send_feedback(flush_lsn =msg.data_start) #start from msg.start when data is incoming
###
#create wal2json connection 
my_connection  = psycopg2.connect(
                   "dbname='college' host='localhost' user='postgres' password='rugved123'" ,
                   connection_factory = LogicalReplicationConnection)
cur = my_connection.cursor()
cur.drop_replication_slot('test_slot2')
cur.create_replication_slot('test_slot2', output_plugin = 'wal2json')
cur.start_replication(slot_name = 'test_slot2', options = {'pretty-print' : 1}, decode= True)

###
try:
    while True:
        data_request = []
        count = 0
       
        try:
            cur.consume_stream(consume)
        except StopReplication :
            print('stopping replication' )
       
except KeyboardInterrupt:
    print('Interrupted')





