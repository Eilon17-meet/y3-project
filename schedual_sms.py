from apscheduler.schedulers.background import BackgroundScheduler
from sms import *
sched = BackgroundScheduler()
'''
@sched.scheduled_job('interval', seconds=3)
def timed_job():
    print('This job is run every three seconds.')
'''
def schedule_sms(day_of_week,hour,minute,src,dst,text):
    @sched.scheduled_job('cron', day_of_week=day_of_week, hour=hour, minute=minute)
    def scheduled_job():
        send_sms(src, dst, text)
    sched.start()

hour=14
minute=57
schedule_sms('mon-fri',hour,minute,'Boost','972533329274','Test sched msg at {}:{}'.format(hour,minute))
#schedule_sms('mon-fri',14,51,'Boost','972533329274','Test sched msg')



while True: pass