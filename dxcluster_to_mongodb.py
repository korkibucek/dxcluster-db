import telnetlib
import pymongo
import re
from datetime import datetime

DXCLUSTER_HOST = "ve7cc.net"
DXCLUSTER_PORT = 7373

# Update the MongoDB connection string with your own credentials and database information
MONGODB_CONNECTION_STRING = "mongodb+srv://username:password@cluster0.mongodb.net/myDatabase?retryWrites=true&w=majority"

# Regular expression to match the dxcluster output format
dxcluster_pattern = re.compile(r"^DX de (.*?)-#:\s+(\d+\.\d+)\s+(.*?)\s+(CW)\s+(\d+) dB (\d+) WPM (CQ|NCDXF BCN|BEACON)\s+(\d{4}Z)$")

def connect_to_mongodb(connection_string):
    client = pymongo.MongoClient(connection_string)
    db = client["dxcluster"]
    collection = db["spots"]
    return collection

def store_data_in_mongodb(collection, data):
    try:
        collection.insert_one(data)
        print(f"Data stored: {data}")
    except Exception as e:
        print(f"Error storing data: {e}")

def parse_dxcluster_line(line):
    match = dxcluster_pattern.match(line)
    if match:
        groups = match.groups()
        data = {
            "source": groups[0],
            "frequency": float(groups[1]),
            "call_sign": groups[2],
            "mode": groups[3],
            "signal_strength": int(groups[4]),
            "speed": int(groups[5]),
            "type": groups[6],
            "time": datetime.strptime(groups[7], "%H%MZ"),
        }
        return data
    else:
        return None

def main():
    # Connect to MongoDB
    mongodb_collection = connect_to_mongodb(MONGODB_CONNECTION_STRING)

    # Connect to the dxcluster
    telnet = telnetlib.Telnet(DXCLUSTER_HOST, DXCLUSTER_PORT)

    # Read data from the dxcluster
    while True:
        try:
            line = telnet.read_until(b"\n").decode("utf-8").strip()
            print(f"Received: {line}")

            data = parse_dxcluster_line(line)
            if data:
                store_data_in_mongodb(mongodb_collection, data)

        except Exception as e:
            print(f"Error: {e}")
            break

    telnet.close()

if __name__ == "__main__":
    main()
