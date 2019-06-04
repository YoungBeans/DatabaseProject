from .models import *
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connection

# Create your views here.

# error를 읽고 erroType 과 errorMsg를 딕셔너리 형태로 반환합니다.
def readErroMsg(request):
    erroMsg = ''
    erroType = 'success'
    if request.session.get('msg', False):
        if request.session.get('error', False):
            del request.session['error']
            erroType = 'danger'
        erroMsg = request.session['msg']
        del request.session['msg']
    return {'erroType':erroType, 'errorMsg':erroMsg}

# error : 오류메시지면 True, 성공메시지면 False
# msg : 화면에 출력할 메시지
def setErroMsg(request, error, msg):
    if error:
        request.session['error'] = error
    request.session['msg'] = msg

def main(request):
    try:
        # error를 읽고 erroType 과 errorMsg를 딕셔너리 형태로 반환합니다.
        # erroType : error 메시지면 danger, 성공 메시지면 success
        # errorMsg : 화면에 출력할 결과메시지
        context = readErroMsg(request)
        if request.session.get('member_id', False):
            favors = Favourite.objects.filter(userid=request.session['member_id'])
            context['favors'] = favors
            print("="*30, favors)
    except:
        # error검출하기 위함입니다.
        erroType = 'danger'
        erroMsg = 'mssage error'
        context = {'erroType':erroType, 'errorMsg':erroMsg}
    return render(request, "mainsite/index.html", context)

def register(request):
    erroType = ''
    erroMsg = ''
    try:
        # error검출하기 위함입니다.
        context = readErroMsg(request)
    except:
        # error검출하기 위함입니다.
        erroType = 'danger'
        erroMsg = 'mssage error'
        context = {'erroType':erroType, 'errorMsg':erroMsg}
    return render(request, "mainsite/register.html", context)

def register_fuc(request):
    try:
        UserInfo.objects.create(
            userid = request.POST.get('userid'),
            pw = request.POST.get('pw'),
            tel = request.POST.get('tel'),
            email = request.POST.get('email')
        )
        m = UserInfo.objects.get(userid=request.POST['userid'])
        request.session['member_id'] = m.userid
        setErroMsg(request, False, "Thank you for signing up!!")
        return redirect('home')
    except:
        setErroMsg(request, True, "이미 있는 ID 입니다.!!")
        return redirect('register')
    

    # =================login area===================

def login(request):
    try:
        m = UserInfo.objects.get(userid=request.POST['userid'])
        if m.pw == request.POST['pw']:
            request.session['member_id'] = m.userid
            setErroMsg(request, False, "Login success!!")
            return redirect('home')
        else:
            setErroMsg(request, True, "PW 불일치.!!")
            return redirect('home')
    except:
        setErroMsg(request, True, "ID가 존재하지 않습니다.!!")
        return redirect('home')
    
def logout(request):
    try:
        del request.session['member_id']
        setErroMsg(request, False, "Logout success!!")
    except KeyError:
        pass
    return redirect('home')

def forgot(request) :
    if request.POST.get('findpwd') :
        return render(request, "mainsite/forgotpage.html")
    else :
        return render(request, "mainsite/findid.html")

def findpwd(request) :
    if request.method == "POST" and request.POST.get('tel') :
        connection.cursor()
        rawCursor = connection.connection.cursor()
        u_tel = request.POST.get('tel')
        u_id = request.POST.get('userid')
        try :
            find_pwds = rawCursor.callfunc("userpwdfind", str, [u_tel, u_id])
        finally :
            rawCursor.close()
        context = {'find_pwds' : find_pwds}
        return render(request, 'mainsite/forgotpage.html', context)
    else :
        return render(request, 'mainsite/forgotpage.html')

def findid(request) :
    if request.method == "POST" and request.POST.get('tel') :
        connection.cursor()
        rawCursor = connection.connection.cursor()
        u_tel = request.POST.get('tel')
        try :
            find_ids = rawCursor.callfunc("useridfind", str, [u_tel])
        finally :
            rawCursor.close()
        context = {'find_ids' : find_ids}
        return render(request, 'mainsite/findid.html', context)
    else :
        return render(request, 'mainsite/findid.html')