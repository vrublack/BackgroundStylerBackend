from pyfcm import FCMNotification

# read api key
with open('api_key.txt') as f:
    api_key = f.readline()[-1]

push_service = FCMNotification(api_key=api_key)


# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

def notify_device(device_id, image_link):
    message_title = "Image successfully rendered"
    message_body = image_link
    result = push_service.notify_single_device(registration_id=device_id, message_title=message_title,
                                               message_body=message_body)
