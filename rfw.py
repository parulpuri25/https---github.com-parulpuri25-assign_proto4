import pandas as pd
from itertools import chain

import numpy as np
class RFWresponse:
    def __init__(self, id, benchtype, workloadmetric, batchunit, batchid, batchsize, datasettype, analysis):
        self.id = id
        self.bench_type = benchtype
        
        self.metric = workloadmetric
        self.batch_id = int(batchid)
        self.batch_size = int(batchsize)
        self.batch_unit = int(batchunit)
        self.datasettype= datasettype
        self.analysis=analysis
        self.csv_data = pd.read_csv("https://raw.githubusercontent.com/haniehalipour/Online-Machine-Learning-for-Cloud-Resource-Provisioning-of-Microservice-Backend-Systems/master/Workload%20Data/" + benchtype +"-"+datasettype+ ".csv")
    
    #for analytics of data(percentile,MAX,MIN)    
    def analysis_value(self,lastbatchid,):
        column = self._get_requested_column_data()
        lastbatchid = self.batch_id
        batch_size=self.batch_size
        final_list=[]
        for index in range(0,batch_size):
            new_item = column[ (lastbatchid) * self.batch_unit:(lastbatchid+1)*self.batch_unit].to_list()
            final_list.append(new_item)
            lastbatchid+= 1
            
        new_list=list(chain(*final_list))
        sorted_list=new_list.sort()
        #new_list=pd.Series(final_list)    
        #sorted_list=final_list.sort()
        
        if self.analysis=='10p':
         value=np.percentile(sorted_list,10)
        elif self.analysis=='50p':
         value=np.percentile(sorted_list,50)
        elif self.analysis=='95p':
         value=np.percentile(sorted_list,95)
        elif self.analysis=='99p':
         value=np.percentile(sorted_list,99)  
        elif self.analysis=='MAX':
         value=max(new_list) 
        elif self.analysis=='MIN':
         value=min(new_list)  
        elif self.analysis=='AVERAGE':
          value=np.average(new_list)
        elif self.analysis=='STANDARD':
            value=np.std(new_list)    

        return(value)
    

    #get the requested data batches and finding the last batchid
    def data_batches(self):
        
        batches = []
        requested_column = self._get_requested_column_data()
        lastbatchid = self.batch_id
        
        for index in range(0, self.batch_size):
            batch = requested_column[lastbatchid * self.batch_unit: (lastbatchid + 1) * self.batch_unit].to_dict()
            batches.append(batch)
            lastbatchid += 1
        print(batches)

        return batches, (lastbatchid - 1)
    # to perform binary serialization
    def binary_serialization(self):

        samples = self._number_of_sample_data()
        (batches, lastbatchid) = self.data_batches()
        analytics=self.analysis_value(lastbatchid)

        print({
            "rfw_id": self.id,
            "last_batch_id": lastbatchid,
            "number_of_samples": samples,
            "batches": batches,
            "analytics":analytics,
        })

        return {
            "rfw_id": self.id,
            "last_batch_id": lastbatchid,
            "number_of_samples": samples,
            "batches": batches,
            "analytics":analytics,
        }

    #user input data column
    def _get_requested_column_data(self):
        
        data_column = self.csv_data[self.metric]

        return data_column
    #number of requested columns from user
    def _number_of_sample_data(self):
        return self.batch_size * self.batch_unit
    #analytic value chosen by user    
    def _get_analysis_value(self):
        return self.analysis