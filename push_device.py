from pyfcm import FCMNotification
from util import prepend_proj

# read api key
with open(prepend_proj('api_key.txt')) as file:
    api_key = file.readline()

push_service = FCMNotification(api_key=api_key)


# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

def notify_device(device_id, image_link, painting_name):
    data_message = {
        'result': image_link,
        'painting-name': painting_name
    }

    result = push_service.notify_single_device(registration_id=device_id, data_message=data_message)

    print result
    print 'Sent out fcm message { message=' + str(data_message) + ' }'
