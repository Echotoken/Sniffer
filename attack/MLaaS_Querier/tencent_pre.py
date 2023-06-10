import requests
import json
import numpy as np

def tencent_predict(data, link):

    new_data = data.tolist()
    data_2 = {
                "features":[
                    {
                        "req_data": new_data
                    }
                ]
            }
    json_data = json.dumps(data_2, ensure_ascii=False)
    head = {'content-type': 'application/json'}
    res = requests.post(link, data=json_data, headers=head)


    try:
        proba_list = json.loads(res.content)['result']
        result = []
        for item in proba_list:
            result.append(list(item.values()))
        print(result)
        return np.array(result)
    except:
        print('no service')
        
   