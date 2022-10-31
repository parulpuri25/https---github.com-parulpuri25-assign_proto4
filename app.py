import  requests
from rfw import RFWresponse
import serialize_pb2
from flask import Flask,request


app = Flask(__name__)
@app.route('/get_batches', methods=['GET'])
def get_batches():
    requested_batches = serialize_pb2.requested_query.FromString(request.data) 
    query_response = serialize_pb2.query_response()
    object = RFWresponse(requested_batches.RFW_ID, requested_batches.benchmarktype, requested_batches.workloadmetric,
                                 requested_batches.batchunit, requested_batches.batch_id, requested_batches.batch_size,requested_batches.dataset_type, requested_batches.data_analytics)
    result = object.binary_serialization()

    query_response.RFW_ID = result['rfw_id']
    query_response.last_batch_ID = result['last_batch_id']
    datasamples = result['batches']
    query_response.analytics_response=result['analytics']

    
    print(datasamples)
    for sample in datasamples:
        serialized_batch = serialize_pb2.batches()
        arrayofsamples = []
        for i in range(0, len(sample)):
            arrayofsamples.append(sample[list(sample.keys())[i]])
        serialized_batch.requested_samples[:] = arrayofsamples
        query_response.sample_data.append(serialized_batch)

    print(query_response)

    if query_response is not None and query_response.last_batch_ID is not None:
        searlized_batch_res = query_response.SerializeToString()
        return searlized_batch_res
if __name__ == '__main__':
    app.run

