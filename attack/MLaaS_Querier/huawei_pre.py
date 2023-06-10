# coding=utf-8
import requests
from apig_sdk import signer
import json
import numpy as np

def huawei_predictor(data, huawei_link):
    sig = signer.Signer()

    with open("../configuration.json", "r") as f:
        json_data = json.load(f)

    sig.Key = json_data['MLaaS']['Huawei_Key']
    sig.Secret = json_data['MLaaS']['Huawei_Secret']

    request_data = data.data
    json_data = {
        "data":
            {
                "req_data": request_data.tolist()
            }
    }
    json_data = json.dumps(json_data)

    r = signer.HttpRequest("POST",
                           huawei_link,
                           {"x-stage": "RELEASE", "Content-Type":"application/json"},
                           json_data)


    sig.Sign(r)
    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)

    
    try:
        proba_list = json.loads(resp.content)['data']['resp_data']
        proba_array = np.array(proba_list)
        
        return proba_array
    except:
        print(resp)
        print(resp.content)
        print(resp.text)
        print(type(resp.text))

        return 0
   

