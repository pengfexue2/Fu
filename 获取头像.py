import os
from PIL import Image
import itchat

def getHeadImgs():
    #通过二维码登录微信网页版
    itchat.auto_login()
    #获取微信好友信息列表
    friendList = itchat.get_friends(update=True)

    #这里会用到的微信好友信息如下： User= {'UserName': '@8238e922e8be7356b1750c306cb75768','PYQuanPin': 'TED','NickName': 'TED'}
    #获取用户个人昵称，用于之后文件夹命名、用户头像命名
    if friendList[0]['PYQuanPin']:
        user = friendList[0]['PYQuanPin']
    else:
        user = friendList[0]['NickName']

    #先读取用户本人头像，存储名为用户名称
    selfHead = "{}/{}.jpg".format(os.getcwd(),user)
    with open(selfHead,'wb') as f:
        head = itchat.get_head_img(friendList[0]['UserName'])
        f.write(head)

    #创建文件夹用于存储好友头像
    if not os.path.exists(user):
        os.mkdir(user)

    #工作路径转到新建文件夹中
    os.chdir(user)
    #获取新建文件夹路径
    userspace = os.getcwd()


    #开始读取好友头像写入新建文件夹中
    print("开始读取%d位好友头像..."%(len(friendList)-1))
    for i in range(1,len(friendList)):
        if i % 100 ==0:
            print("已读取%d位好友头像，请耐心等待~"%i)
        try:
            friendList[i]['head_img'] = itchat.get_head_img(userName=friendList[i]['UserName'])
            friendList[i]['head_img_name'] = "%s.jpg" % friendList[i]['UserName']
        except ConnectionError:
            print('Fail to get %s' % friendList[i]['UserName'])

        with open(friendList[i]['head_img_name'],'wb') as f:
            f.write(friendList[i]['head_img'])
    print("读取好友头像完毕！")


    #登出
    itchat.logout()
    #保存头像的文件夹路径和用户本人头像路径返回
    return user, selfHead

def main():
    #获取用户本人名称和用户本人头像路径
    user,self = getHeadImgs()
if __name__=="__main__":
    main()
