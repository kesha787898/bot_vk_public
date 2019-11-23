import vk_api
import time
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import urllib
import clust
from skimage.io import imsave
import skimage
import io
from skimage.io import imread
import numpy as np
print('started')
VK_TOKEN = 'aa6f5b99fb937048d8b70d1df8daf5eec20ad91cac353cbb662158355c34cdf1f9882f1432b9951a46dfc'
GROUP_ID = 188659573


class stater:
    img=None
    state=0

def log(event):
    print('------------------------')
    print(time.ctime())
    print(event.type)
    print(event.object)
    print('------------------------')

def write_msg(text, id, vk):
    vk.method('messages.send', {'user_id': id, 'message': text, 'random_id': int(time.time() * 100000)})

def logic():
    try:
        state=stater()
        vk = vk_api.VkApi(token=VK_TOKEN)
        longpoll = VkBotLongPoll(vk, GROUP_ID)
        n = 0
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                request = event.object['message']
                log(event)
                if state.state == 0:
                    state0(request,vk,state)
                elif state.state == 1:
                    state1(request,vk,state)
                elif state.state == 2:
                    state2(request,vk,state)
    except Exception as e:
        print(e)



def state0(request,vk,state):
    write_msg("Hi,Send me a photo pls", request['from_id'], vk)
    state.state += 1

def state1(request,vk,state):
    if request['attachments'] and request['attachments'][-1]['type'] == 'photo':
        img = urllib.request.urlopen(request['attachments'][-1]['photo']['sizes'][-1]['url']).read()
        img = skimage.img_as_float(imread(io.BytesIO(img)))
        state.img=img
        write_msg("How much colors should i save?", request['from_id'], vk)
        state.state+= 1
    else:
        write_msg("It is not photo!,send me another!", request['from_id'], vk)

def state2(request,vk,state):
    if request['text'].isdigit():
        n = int(request['text'])
        if (n > len(np.unique(state.img, axis=0))) or (n == 0):
            write_msg("It is bad number,send me another", request['from_id'], vk)
        else:
            write_msg("Please wait", request['from_id'], vk)
            rez = clust.clust(state.img, n)
            upload = vk_api.VkUpload(vk)
            imsave("test.png", rez)
            ph = upload.photo_messages("./test.png")
            ph = 'photo' + str(ph[-1]['owner_id']) + '_' + str(ph[-1]['id'])
            vk.method('messages.send',
                      {'user_id': request['from_id'], 'message': 'Hi', 'attachment': ph,
                       'random_id': int(time.time() * 100000)})
            write_msg("Thank for your waiting,bye", request['from_id'], vk)
            state.state = 0
    else:
        write_msg("It is not number!", request['from_id'], vk)


def vk_main():
    while True:
        logic()




if __name__ == '__main__':
    vk_main()
