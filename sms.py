
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



'''
# Prints the complete response
print str(response)

# Sample successful output
# (202,
#       {
#               u'message': u'message(s) queued',
#               u'message_uuid': [u'b795906a-8a79-11e4-9bd8-22000afa12b9'],
#               u'api_id': u'b77af520-8a79-11e4-b153-22000abcaa64'
#       }
# )

# Prints only the status code
print str(response[0])

# Sample successful output
# 202

# Prints the message details
print str(response[1])

# Sample successful output
# {
#       u'message': u'message(s) queued',
#       u'message_uuid': [u'b795906a-8a79-11e4-9bd8-22000afa12b9'],
#       u'api_id': u'b77af520-8a79-11e4-b153-22000abcaa64'
# }

# Print the message_uuid
print str(response[1]['message_uuid'])

# Sample successful output
# [u'b795906a-8a79-11e4-9bd8-22000afa12b9']

# Print the api_id
print str(response[1]['api_id'])

# Sample successful output
# b77af520-8a79-11e4-b153-22000abcaa64

'''


'''
import plivo, plivoxml
from flask import Flask, request

app = Flask(__name__)

@app.route("/receive_sms/", methods=['GET','POST'])
def receive_sms():
    # Sender's phone numer
    from_number = request.values.get('From')
    # Receiver's phone number - Plivo number
    to_number = request.values.get('To')
    # The text which was received
    text = request.values.get('Text')

    # Print the message
    print 'Message received - From: %s, To: %s, Text: %s' % (from_number, to_number, text)

    return 'Message received - From: %s, To: %s, Text: %s' % (from_number, to_number, text)
if __name__ == '__main__':
    app.run(debug=True)
'''