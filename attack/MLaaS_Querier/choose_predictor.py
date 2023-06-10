from MLaaS_Querier.huawei_pre import  huawei_predictor
from MLaaS_Querier.tencent_pre import tencent_predict
from MLaaS_Querier.ali_pre import ali_predictor
from MLaaS_Querier.google_pre import google_predictor
from MLaaS_Querier.aws_pre import aws_predictor

class mlaas_predict:
    def __init__(self,cloud_name,link1,link2):
        self.link1 = link1
        self.link2 = link2
        self.cloud_name = cloud_name
    def predictor(self,data):
        if self.cloud_name == "Google":
            return google_predictor(data, self.link1, self.link2)
        elif self.cloud_name == "Amazon":
            return aws_predictor(data, self.link1)
        if self.cloud_name == 'Huawei':
            return huawei_predictor(data, self.link1)
        elif self.cloud_name == 'Tencent':
            return tencent_predict(data, self.link1)
        elif self.cloud_name == 'Aliyun':
            return ali_predictor(data, self.link1, self.link2)