import os
import time
import sys
import logging

from LMs import LM_main
from KMs import KM_main
from DTs import DT_main
from NNs.NNs import NN_main

from utils.load_initialization_attack_pool import  Data_input, Data_common
from MLaaS_Querier.choose_predictor import mlaas_predict
from utils.utils import write_sql


link1 = ""
link2 = ""
sig1 = sys.argv[1]
sig2 = sys.argv[2]
sig3 = sys.argv[3]
sig4 = sys.argv[4]
attack_name = sys.argv[5]
sam_type = sys.argv[6]
sam_name = sys.argv[7]
feat_range = sys.argv[8]
cloud_name = sys.argv[9]
if cloud_name == "Alinyun":
    link1 = sys.argv[10]
    link2 = sys.argv[11]
    if sys.argv[12] == "-":
        feat_num = 0
    else:
        feat_num = sys.argv[12]
else:
    link1 = sys.argv[10]
    if sys.argv[11] == "-":
        feat_num = 0
    else:
        feat_num = sys.argv[11]


Predictor = mlaas_predict(cloud_name, link1, link2).predictor

sam_num = 30
if sam_name == "-":
    data = Data_input(sam_num, Predictor, feat_num, feat_range)
else:
    data = Data_common(sam_num, Predictor, sam_name)


Result_Flag = False

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='../mlaas_log/'+attack_name+'.txt',
                filemode='w')
logging.info('start detection...\n')


if sig1 == "1":     #DTs

    number = 10
    member = 4
    Min, Max = -0.01, 0.01
    threshold = 0.0001
    old_time = time.time()
    d_t, d_n, d_p = DT_main(data, Predictor, number, member, Min, Max, threshold)

    sql1 = "update mlaas_result set tree_num='{}' where mlaas_name='{}'".format(d_n, attack_name)
    sql3 = "update mlaas_result set tree_conf='{}' where mlaas_name='{}'".format(d_p, attack_name)
    current_time = time.time()
    temp = float(str(current_time - old_time))
    time1 = int(temp*1000)
    if time1 < 1:
        time1 = 1
    
    sql2 = "update mlaas_result set tree_time='{}' where mlaas_name='{}'".format(time1, attack_name)

    write_sql(sql1)
    write_sql(sql2)
    write_sql(sql3)

    if d_t:
        Result_Flag = True
        sql4 = "update mlaas_result set type='{}' where mlaas_name='{}'".format('Decision Tree', attack_name)
        write_sql(sql4)
    


if (not Result_Flag) and (sig2 == "1"):     #KMs
    old_time = time.time()
    r_t, r_p, r_n = KM_main(data.data, Predictor)

    sql1 = "update mlaas_result set svm_num='{}' where mlaas_name='{}'".format(r_n, attack_name)
    sql3 = "update mlaas_result set svm_conf='{}' where mlaas_name='{}'".format(r_p,  attack_name)
    current_time = time.time()
    temp=float(str(current_time - old_time))
    time1=int(temp*1000)
    if time1 < 1:
        time1 = 1
    sql2 = "update mlaas_result set svm_time='{}' where mlaas_name='{}'".format(time1, attack_name)

    write_sql(sql1)
    write_sql(sql2)
    write_sql(sql3)

    if r_t:
        Result_Flag = True
        sql4 = "update mlaas_result set type='{}' where mlaas_name='{}'".format('Kernel Model', attack_name)
        write_sql(sql4)




if (not Result_Flag) and (sig3 == "1"):     #LMs
    old_time = time.time()
    l_t, l_n, l_p = LM_main(Predictor, data)

    sql1 = "update mlaas_result set linear_num='{}' where mlaas_name='{}'".format(l_n, attack_name)
    sql3 = "update mlaas_result set linear_conf='{}' where mlaas_name='{}'".format(l_p, attack_name)
    current_time = time.time()
    temp=float(str(current_time - old_time))
    time1=int(temp*1000)
    if time1 < 1:
        time1 = 1
    sql2 = "update mlaas_result set linear_time='{}' where mlaas_name='{}'".format(time1, attack_name)

    write_sql(sql1)
    write_sql(sql2)
    write_sql(sql3)

    if l_t:
        Result_Flag = True
        sql4 = "update mlaas_result set type='{}' where mlaas_name='{}'".format('Linear Model', attack_name)
        write_sql(sql4)



if (not Result_Flag) and (sig4 == "1"):     #NNs
    old_time = time.time()
    type_nn, n_n = NN_main(log, Predictor, data)
    sql1 = "update mlaas_result set nn_num='{}' where mlaas_name='{}'".format(n_n, attack_name)
    current_time = time.time()
    temp=float(str(current_time - old_time))
    time1=int(temp*1000)
    if time1 < 1:
        time1 = 1
    sql2 = "update mlaas_result set nn_time='{}' where mlaas_name='{}'".format(time1, attack_name)

    write_sql(sql1)
    write_sql(sql2)

    if not (d_t or r_t or l_t):
        sql4 = "update mlaas_result set type='{}' where mlaas_name='{}'".format('Neural Network', attack_name)
        write_sql(sql4)



logging.info('The experiment ended')