
import plivo

def send_sms(src,dst,text,url=None):
    

    auth_id = "MAZGRIZDI2YMQYZDC4NT"
    auth_token = "MDI0MzhhZGNiMTg4ZDhhZGQ1ZWNmMTk5ZmE1ODUx"

    if type(dst)==list:
        dst=''.join(number + '<' for number in dst)[:-1]

    p = plivo.RestAPI(auth_id, auth_token)

    params = {
        'src': src,     #'Boost', # Sender's phone number with country code
        'dst' : dst,    #'972526937304<972533329274', # Receiver's phone Number with country code
        'text' : text,  #u"Thanks for working with us!", # Your SMS Text Message - English
        'url' : url,    # 'http://boosts.co/receive_sms/'
    }

    response = p.send_message(params)


from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
'''
@sched.scheduled_job('interval', seconds=3)
def timed_job():
    print('This job is run every three seconds.')
'''
sched.start()
def schedule_sms(day_of_week,hour,minute,src,dst,text):
    @sched.scheduled_job('cron', day_of_week=day_of_week, hour=hour, minute=minute)
    def scheduled_job():
        send_sms(src, dst, text)
if __name__ == '__main__':
    hour=16
    minute=3
    schedule_sms('mon-fri',hour,minute,'Boost','972533329274','Test sched msg at {}:{}'.format(hour,minute))
    minute+=2
    schedule_sms('mon-fri',hour,minute,'Boost','972533329274','Test sched msg at {}:{}'.format(hour,minute))
    #schedule_sms('mon-fri',14,51,'Boost','972533329274','Test sched msg')
    while True: pass
    


