from eas_prediction import PredictClient
import requests

def ali_predictor(data,ali_link,ali_token):

    url1=ali_link[:ali_link.index('.com')+4]
    url2=ali_link[ali_link.index('/api/predict/')+13:]
    client = PredictClient(url1,url2)
    client.set_token(ali_token)
    client.init()
    request = data.data
    resp = client.predict(request)

    output = resp.content

    return output