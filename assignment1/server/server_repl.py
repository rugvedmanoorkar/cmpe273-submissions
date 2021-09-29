from concurrent import futures
import logging

import grpc

import replication_pb2
import replication_pb2_grpc
from datetime import datetime
import json
import pymongo
from pymongo import MongoClient



class Replicator(replication_pb2_grpc.ReplicatorServicer):

    def Replicate(self, request_iterator, context):
       
        iterator = []
        query = ""
        for reqs in request_iterator:
            print(" *** ITT *** ",reqs )
            iterator.append(reqs.partofquery)
        
        query = json.loads(query.join(iterator))
        #update mongodb ffor every value sent by postgres
        update_db(query['change'], query['change'][0]['kind'])
        return replication_pb2.Response(status="Database updated successfully")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replication_pb2_grpc.add_ReplicatorServicer_to_server(Replicator(), server)
    server.add_insecure_port('[::]:50051')
    print("Replicator is running at port 50051")
    server.start()
    server.wait_for_termination()

def update_db(val, task):
    
    cluster = MongoClient('mongodb+srv://dbUser:dbUserPassword@cluster0.eodt6.mongodb.net/college?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE',connect=False)
    db = cluster["college"]
    collection = db["students"]

    if task == 'insert':
        val = val[0]['columnvalues']
        post = {"postgresid":val[0],"first_name":val[1],"last_name": val[2], "sjsu_id":val[3],"email":val[4],"create_timestamp":val[5],"update_timestamp":datetime.now() }
        collection.insert_one(post)
    elif task == 'delete':
        val = val[0]['oldkeys']['keyvalues']
        collection.delete_one({"postgresid":val[0] })

if __name__ == '__main__':
    logging.basicConfig()
    serve()
