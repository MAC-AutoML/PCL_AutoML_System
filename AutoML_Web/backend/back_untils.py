#from _app import models
import time
from tools import API_tools
from  tools.API_tools import get_keyword

uinfo = API_tools.check_user('wudch', 'woodchen')
print(uinfo)
def updata_jobtable(tocken,un,pa):
    #同步云脑数据库job信息
    job = models.User_Job.objects.all().order_by("id")
    job = job.exclude(state="STOPPED").exclude(state="FAIL").exclude(state="SUCCEEDED")
    for jd in job:
        print(jd)
        jd_detail = API_tools.get_jobinfo(jd.jobid,tocken,un,pa)
        if jd_detail["code"] == "S000":
            jd.state = jd_detail["payload"]["jobStatus"]["state"]
            timeStamp2 = int(jd_detail['payload']['jobStatus']["completedTime"])
            if timeStamp2 != 0:
                timeArray2 = time.localtime(timeStamp2 / 1000)
                otherStyleTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray2)
                jd.completedTime = otherStyleTime2
            jd.save()
            print("$$$$$$$$ Update Dataset Success")