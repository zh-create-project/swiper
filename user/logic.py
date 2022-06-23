import  requests
import random
from django.core.cache import cache
import json
import hashlib
from django.core.cache import cache
from django.http import JsonResponse
# from tasks import send_sms_celery
# from sms import YunTongXin
# from models import User
from swiper import config
from worker import call_by_worker
def gen_verify_code(length=6):
    """生成验证码"""
    return random.randrange(10**(length-1),10**length)

@call_by_worker
def send_verify_code(phonenumber):
    """发送短信"""
    vcode = gen_verify_code(6)
    key = 'VerifyCode-%s'%(phonenumber)
    cache.set(key,vcode)
    sms_cfg = config.HY_SMS_PARAMS.copy()
    sms_cfg['content'] = sms_cfg['content'] % vcode
    sms_cfg['mobile'] = phonenumber
    respnose = requests.post(config.HY_SMS_URL,data=sms_cfg)
    return respnose

# #下面这个函数是API对接的函数，通过接收前端传过来的电话号码，在后端生成随机验证码，然后缓存redis一份，发送验证手机一份
# def sms_view(request):
#     if request.method != 'POST':
#         result = {'code':'10108','error':'please use post'}
#         return JsonResponse(result)
#     json_str = request.body
#     json_obj = json.loads(json_str)
#     phone = json_obj['phone']
#     #生成随机码
#     code = random.randint(1000,9999)#生成区间1000-9999之间的int类型的值
#     print('phone',phone,'code',code)
#
#     #储存随机码 django_redis，代码运行到此处需要保证redis服务器开启，否则代码运行到此处会因为找不到redis服务器停止
#     cache_key = 'sms_%s'%(phone)
#     #检查是否已经有发过的且未过期的验证码，有则不再生成验证码，直接使用，没有则再次生成验证码
#     old_code = cache.get(cache_key)
#     if old_code:
#         return JsonResponse({'code': 10111,'error':'此手机号在一分钟内已进行注册操作，验证码在有效期内'})
#
#     cache.set(cache_key,code,60)#把code存进redis并设置只存储60秒
#
#     #发送随机码,不使用celery版本
#     # res = send_sms(phone,code)
#     try:
#         res = send_sms_celery.delay(phone,code)#celery版本的发送随机码,这里需要使用delay()启动celery版本的发送短信验证码功能，这样传输端才能收到这个消费请求,不使用delay()启动只是单纯的调用发送短信验证码的方法，能够达到注册效果但是失去了celery的意义
#         return JsonResponse({'code': 200})
#     except Exception as e:
#         return JsonResponse({'code':201})
#     # res = json.dumps(res, default=lambda obj: obj.__dict__)
#     # print(type(res))
#     # if (res.get('statusCode') =='000000'):
#     #     return JsonResponse({'code':200})
#     # else:
#     #     return JsonResponse({'code':201})
# def send_sms(phone,code):
#     config = {
#         'accountSid': '8a216da87e7baef8017f29a965481943',
#         'accountToken': '9067cc7dc0a84688870814ca55f98723',
#         'appId': '8a216da87e7baef8017f29a96669194a',
#         'templateId': '1',
#
#     }
#     yun = YunTongXin(**config)  # 拆包操作，把字典拆包进行关键字传参
#     res = yun.run(phone, code)
#     return res
#
# """下面这个函数接收前端的posy请求，对填写的注册信息进行验证，判断是否允许注册，包括用户名验证码的合法性"""
# def post(self, request):
#     # request.post是针对表单的post请求提交的数据，可以用这样的方法取数据，对于application/json这样的数据，需要使用下面的方法取数据
#     json_str = request.body  # request.body可以直接取出请求体中的数据
#     json_str = json.loads(json_str)  # 转换为字典
#     username = json_str['username']  # 这里去数据的方式是强取的，可以使用json_str.get('username')的方式温柔的取出数据
#     email = json_str['email']
#     password_1 = json_str['password_1']
#     password_2 = json_str['password_2']
#     phone = json_str['phone']
#     sms_num = json_str['sms_num']
#     # 参数基本检查，检查密码是否一致
#     if password_1 != password_2:
#         result = {'code': 10100, 'error': 'the password is not same'}
#         return JsonResponse(result)
#     #比对验证码是否一致
#     old_code = cache.get('sms_%s'%(phone))#使用cache.get取redis数据库中的值的时候，由于cache.set在存储值的时候设置了一个有效时间，所以需要在下面校验现在这个值是否在redis数据库中还是存在的
#     if not old_code:
#         result = {'code':10110,'error':'The code is wrong!'}
#         return JsonResponse(result)
#     if int(sms_num) != old_code:
#         result = {'code': 10110, 'error': 'The code is wrong!'}
#         return JsonResponse(result)
#
#
#
#     # 检查验证用户名是否可用
#     old_user = User.objects.filter(username=username)
#     if old_user:
#         result = {'code': 10101, 'error': 'The username is already existed'}
#         return JsonResponse(result)
#     # 向数据库的user_user_profile表插入数据（密码md5存储）
#     p_m = hashlib.md5()
#     p_m.update(password_1.encode())  # 把字符串使用encode()转化成字节串
#     User.objects.create(username=username, nickname=username, password=p_m.hexdigest(), email=email,
#                                phone=phone)
#     result_sucess = {'code': 200, 'username': username, 'data': {}}
#     return JsonResponse(result_sucess)
# """关于字典深拷贝与浅拷贝的区别：
# from copy import copy,deepcopy
# a = [1,2,3]
# b = copy(a)
# c = deepcopy(a)
# 对于上面的语句b是对a的引用，意思是b的变化会影响到a的变化，他们所指向的地址空间是一样的，
# c是对a的值拷贝，不是引用关系，变量c与a的地址不是指向的同一个地址，意思是c的变化不会影响到a的变化
# """
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# def sms_view(phone):
#     # if request.method != 'POST':
#     #     result = {'code':'10108','error':'please use post'}
#     #     return JsonResponse(result)
#     # json_str = request.body
#     # json_obj = json.loads(json_str)
#     phone = phone
#     #生成随机码
#     code = random.randint(1000,9999)#生成区间1000-9999之间的int类型的值
#     print('phone',phone,'code',code)
#
#     #储存随机码 django_redis，代码运行到此处需要保证redis服务器开启，否则代码运行到此处会因为找不到redis服务器停止
#     cache_key = 'sms_%s'%(phone)
#     #检查是否已经有发过的且未过期的验证码，有则不再生成验证码，直接使用，没有则再次生成验证码
#     old_code = cache.get(cache_key)
#     if old_code:
#         return JsonResponse({'code': 10111,'error':'此手机号在一分钟内已进行注册操作，验证码在有效期内'})
#
#     cache.set(cache_key,code,60)#把code存进redis并设置只存储60秒
#
#     #发送随机码,不使用celery版本
#     # res = send_sms(phone,code)
#     try:
#         res = send_sms_celery.delay(phone,code)#celery版本的发送随机码,这里需要使用delay()启动celery版本的发送短信验证码功能，这样传输端才能收到这个消费请求,不使用delay()启动只是单纯的调用发送短信验证码的方法，能够达到注册效果但是失去了celery的意义
#         return JsonResponse({'code': 200})
#     except Exception as e:
#         return JsonResponse({'code':201})
# if __name__ == '__main__':
#     sms_view('18282498593')