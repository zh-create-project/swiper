from django.shortcuts import render
from .logic import send_verify_code
"""手机注册"""
def get_verify_code(request):
    phonenumber = request.GET.get('phonenumber')
    send_verify_code(phonenumber)


"""短信验证登录"""
def login(request):
    pass

"""获取个人资料"""
def get_profile(request):
    pass

"""修改个人资料"""
def modify_profile(request):
    pass

"""头像上传"""
def upload_avatar(request):
    pass



