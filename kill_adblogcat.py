import requests
import json
import os
import re
import time
while True:
    try:
        adb = '/work/deploy/res/android-sdk-tinypace/adb'
        status_api = ""
        adb_con = os.popen('%s devices -l' % (adb))
        adb_list = adb_con.readlines()
        udid_dict = {}
        devices = []
        num_con = os.popen('ps -ef|grep logcat|grep -v grep|wc -l')
        num = int(num_con.readlines()[0].strip())
        flag = True
        match_string = re.compile("(^.+)device usb")
        adb_con.close()
        num_con.close()
        if len(adb_list) <= 2:
            continue
        else:
            for device in adb_list:
                devs = match_string.findall(device)
                if len(devs) <= 0:
                    continue
                else:
                    udid_dict["udid"] = devs[0].split()[0]
                    a = devices.append(udid_dict)
            if len(devices) <= 0:
                continue
            else:
                for dict_mobile in devices:
                    json_mobile = json.dumps(dict_mobile)
                    res = requests.session()
                    res1 = res.request("post",status_api,data=json_mobile,headers={"Content-Type":"application/json"},timeout=5)
                    res2 = res1.json()
                    res.close()
                    if res2["isOccupied"] == True:
                        flag = False
                    else:
                        continue
            if flag == True and num >= 2:
                #print(1)
                kill_adb = os.popen("kill -9 `ps -ef|grep logcat|grep -v python|grep -v grep|awk {'print$2'}`")
                kill_adb.close()
    except:
        print("errot!")
    finally:
        time.sleep(600)
