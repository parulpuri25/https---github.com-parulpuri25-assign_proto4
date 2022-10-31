import serialize_pb2, requests
import numpy as np
from numpy import byte, fromstring
import time

batch_request_data = serialize_pb2.requested_query()

id = input('Enter the id for RFW to be searched')
benchmarktype = input('Enter the benchmark type from one of the following:\n 1. DVD\n 2.NDBench ')
metric = input('Choose the workloadmetric to be queried \n''1. CPUUtilization_Average\n 2. NetworkIn_Average\n 3. NetworkOut_Average\n'
               ' 4. MemoryUtilization_Average\n')
batch_id = int(input('Enter the Batch Id (from which batch you want the data to start from in integer: \n'))
batch_unit = int(input('Enter the number of samples you want in one batch in integer:\n '))
batch_size = int(input('Enter the number of batches to be returned in integer:\n '))
datasettype= input('Enter the benchmark type from one of the following:\n 1. testing\n 2.training \n')
data_anayltics=input('Enter the data anayltics to be performed on the samples recieved from the following \n 1. 10p\n2. 50p\n 3. 90p\n 4. 99p\n 5.MAX \n 6. MIN\n 7. AVERAGE\n 8. STANDARD \n')
batch_request_data.RFW_ID = id
batch_request_data.benchmarktype = benchmarktype
batch_request_data.workloadmetric = metric
batch_request_data.batch_id = batch_id
batch_request_data.batchunit = batch_unit
batch_request_data.batch_size = batch_size
batch_request_data.dataset_type=datasettype
batch_request_data.data_analytics=data_anayltics
#res = requests.get("http://127.0.0.1:5000/get_batches?", headers={'Content-Type': 'application/protobuf'},
#                   data=batch_request_data.SerializeToString(),verify=False)


#data_response=" "
#while data_response == "":
#    try:
data_response = requests.get("http://127.0.0.1:5000/get_batches?", headers={'Content-Type': 'application/protobuf'},
                   data=batch_request_data.SerializeToString(),verify=False)
 #       break
#    except:
 #       print("Connection refused by the server..")
  #      print("Let me sleep for 5 seconds")
   #     print("ZZzzzz...")
    #    time.sleep(5)
     #   print("Was a nice sleep, now let me continue...")
      #  continue

query_response = serialize_pb2.query_response.FromString(data_response.content)



file = open('Proto_File', "wb")
file.write(data_response.content)
file.close()

print(query_response)
