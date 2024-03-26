#!/usr/bin/env python3
"""
    This script contains a function that displays some
    stats about nginx logs stored in mongoDb
"""
import pymongo


if __name__ == '__main__':
    # First try to  connect to the mongo database with pymongo
    server = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

    # Get a count of all the documents in the collection
    x = server.logs.nginx
    docs = x.count_documents({})
    print(f"{docs} logs")

    # Print the http methods alongside a count of their documents
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")

    for method in methods:
        num_of_docs = x.count_documents({"method": methods})
        print(f"\t method {method}: {num_of_docs}")

    # Count and print out the number of get requests with status check
    status_count = x.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_count} status check")
