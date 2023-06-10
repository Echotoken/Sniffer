import pymysql
import json

def write_sql(sql):
    with open("../configuration.json", "r") as f:
        json_data = json.load(f)
    db = pymysql.connect(host=json_data["database"]["server"],
                user=json_data["database"]["username"],
                password=json_data["database"]["password"],
                database=json_data["database"]["database"])
    cursor = db.cursor()

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        db.close()