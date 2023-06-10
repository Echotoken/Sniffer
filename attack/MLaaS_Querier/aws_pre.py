import boto3, re, sys, math, json, os, sagemaker, urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sagemaker.predictor import csv_serializer
import requests

def aws_predictor(data,link):
    request_data = data.data
    sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=link)
    endpoint_name = 'test'
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        Body=bytes(request_data, 'utf-8')
    )
    return response['Body'].read().decode('utf-8')

def aws_predictor2(data,link):
    url = link
    request_data = data.data
    resp = requests.post(url, data=request_data)
    output = resp.content

    return output