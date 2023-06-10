import os
import time
import torch
import sys
import logging
import json

from local_predictor import local_predict
from utils.load_initialization_attack_pool import Data_local
from utils.utils import write_sql

from KMs import KM_main
from DTs import DT_main
from LMs import LM_main
from NNs.NNs import NN_main

sig1 = sys.argv[1]
sig2 = sys.argv[2]
sig3 = sys.argv[3]
sig4 = sys.argv[4]
exp_name = sys.argv[5]
model_path = sys.argv[6]
sam_name = sys.argv[7]


with open("../configuration.json", "r") as f:
    json_data = json.load(f)
    
# Predictor = local_predict(model_path, json_data["Local"]["Type_groundtruth"]).predictor
Predictor = local_predict(model_path, model_path[7:10]).predictor

sam_num = 30
data = Data_local(sam_num, Predictor, sam_name)

Result_Flag = False

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../local_log/'+exp_name+'.txt',
                filemode='w' )
logging.info('start detection...\n')

if sig1 == "1":

    number = 10
    member = 4
    Min, Max = -0.01, 0.01
    threshold = 0.0001
    old_time = time.time()

    d_t, d_n, d_p = DT_main(data, Predictor, number, member, Min, Max, threshold)
    data.recover_data()

    sql1 = "update local_result set tree_num='{}' where local_name='{}'".format(d_n, exp_name)
    sql3 = "update local_result set tree_conf='{}' where local_name='{}'".format(d_p, exp_name)
    current_time = time.time()
    temp = float(str(current_time - old_time))
    time1 = int(temp*1000)
    if time1 < 1:
        time1 = 1
    sql2 = "update local_result set tree_time='{}' where local_name='{}'".format(time1, exp_name)
    
    write_sql(sql1)
    write_sql(sql2)
    write_sql(sql3)

    if d_t:
        Result_Flag = True
        sql4 = "update local_result set type='{}' where local_name='{}'".format('Decision Tree', exp_name)
        write_sql(sql4)


if (not Result_Flag) and (sig2 == "1"):
    old_time = time.time()

    r_t, r_p, r_n = KM_main(data.data, Predictor)
    data.recover_data()

    sql1 = "update local_result set svm_num='{}' where local_name='{}'".format(r_n,exp_name)
    sql3 = "update local_result set svm_conf='{}' where local_name='{}'".format(r_p,exp_name)
    current_time = time.time()
    temp=float(str(current_time - old_time))
    time1=int(temp*1000)
    if time1 < 1:
        time1 = 1
    sql2 = "update local_result set svm_time='{}' where local_name='{}'".format(time1,exp_name)

    write_sql(sql1)
    write_sql(sql2)
    write_sql(sql3)

    if r_t:
        Result_Flag = True
        sql4 = "update local_result set type='{}' where local_name='{}'".format('Kernel Model', exp_name)
        write_sql(sql4)




if (not Result_Flag) and (sig3 == "1"):
    old_time = time.time()

    l_t, l_n, l_p = LM_main(Predictor, data, sam_name)
    data.recover_data()

    sql1 = "update local_result set linear_num='{}' where local_name='{}'".format(l_n,exp_name)
    sql3 = "update local_result set linear_conf='{}' where local_name='{}'".format(l_p,exp_name)
    current_time = time.time()
    temp=float(str(current_time - old_time))
    time1=int(temp*1000)
    if time1 < 1:
        time1 = 1
    sql2 = "update local_result set linear_time='{}' where local_name='{}'".format(time1,exp_name)

    write_sql(sql1)
    write_sql(sql2)
    write_sql(sql3)

    if l_t:
        Result_Flag = True
        sql4 = "update local_result set type='{}' where local_name='{}'".format('Linear Model', exp_name)
        write_sql(sql4)




if (not Result_Flag) and (sig4 == "1"):
    old_time = time.time()
    type_nn, n_n = NN_main(Predictor, data, sam_name)
    sql1 = "update local_result set nn_num='{}' where local_name='{}'".format(n_n, exp_name)
    current_time = time.time()
    temp=float(str(current_time - old_time))
    time1=int(temp*1000)
    if time1 < 1:
        time1 = 1
    sql2 = "update local_result set nn_time='{}' where local_name='{}'".format(time1, exp_name)

    write_sql(sql1)
    write_sql(sql2)

    if not (d_t or r_t or l_t):
        sql4 = "update local_result set type='{}' where local_name='{}'".format('Neural Network', exp_name)
        write_sql(sql4)



logging.info('The experiment ended')