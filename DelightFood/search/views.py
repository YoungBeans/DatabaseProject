from mainsite.models import *
from django.db.models import Avg, Max, Min, Sum, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.db import connection

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

# Create your views here.
def main(request):
    restaurant_list = Restaurant.objects.all()

    paginator = Paginator(restaurant_list, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    context = readErroMsg(request)
    context['contacts'] = contacts
    return render(request, "search/index.html", context)

# 음식점 상세보기
def result(request, pk):
    rest = Restaurant.objects.get(pk=float(pk))
    menu = Menu.objects.filter(restid=float(pk))
    rateAvg = Rate.objects.filter(restid=float(pk)).aggregate(Avg('rate'))
    types={}
    for m in menu:
        foodType = FoodTypes.objects.filter(menuid=m.menuid)
        types[m.name] = foodType
    if rest.cnt == None:
        rest.cnt = 1.0
    else:
        rest.cnt += 1
    rest.save()
    context = {'restaurant':rest, 'menu':menu, 'types':types.items(), 'rateAvg':rateAvg['rate__avg']}
    return render(request, "search/result.html", context)

# 즐겨찾기 추가
def favorite(request, pk):
    favMax = Favourite.objects.all().aggregate(Max('favid'))
    user = UserInfo.objects.get(pk=request.session['member_id'])
    rest = Restaurant.objects.get(pk=float(pk))
    if not Favourite.objects.filter(restid = rest , userid = user):
        if favMax['favid__max'] == None:
            Favourite.objects.create(
                favid = 1.0,
                restid = rest,
                userid = user
            )
        else:
            Favourite.objects.create(
                favid = favMax['favid__max']+1,
                restid = rest,
                userid = user
            )
    else:
        setErroMsg(request, True, "'{}'은/는 이미 추가한 항목입니다.".format(rest.name))
    print("="*30,favMax)
    return redirect('home')

# 즐겨찾기 삭제
def delFavorite(request, pk):
    favor = Favourite.objects.get(favid = float(pk))
    favor.delete()
    return redirect('home')

# 음식점 평점 남기기
def addRate(request):
    rateMax = Rate.objects.all().aggregate(Max('rateid'))
    user = UserInfo.objects.get(pk=request.session['member_id'])
    rest = Restaurant.objects.get(pk=float(request.GET.get('restid')))
    rate = float(request.GET.get('rate'))
    if not Rate.objects.filter(restid = rest , userid = user):
        print("="*30,'error')   
        if rateMax['rateid__max'] == None:
            Rate.objects.create(
                rateid = 1.0,
                restid = rest,
                userid = user,
                rate = rate,
            )
        else:
            Rate.objects.create(
                rateid = rateMax['rateid__max']+1,
                restid = rest,
                userid = user,
                rate = rate,
            )
    else:
        oldRate = Rate.objects.get(restid = rest , userid = user)
        oldRate.rate = rate
        oldRate.save()
        setErroMsg(request, False, "'{}'을/를 재평가 하였습니다.".format(rest.name))
    return redirect('search')
# 검색함수
def searching(request):
    request.session['search'] = request.GET.get('search')   # 검색내용
    request.session['gu'] = request.GET.get('gu')           # 구 옵션내용
    request.session['resType'] = request.GET.get('resType') # 업태 옵션내용
    request.session['option'] = request.GET.get('option')
    return redirect('searching2')

def searching2(request):
    search = request.session['search'] 
    gu = request.session['gu'] 
    resType = request.session['resType'] 
    option = request.session['option']

    context = readErroMsg(request)
    if search == '': # 검색할 내용이 없을때
        if option: # option을 사용했을 때
            if gu == None and resType != None:      # 업태는 선택했으나 구는 선택을 안했을때
                resType_instance = ResType.objects.get(rtype_name = resType)
                restaurant_list = Restaurant.objects.filter(rtype_name=resType_instance) 
            elif gu != None and resType == None:    # 구는 선택했으나 업태는 선택을 안했을때
                restaurant_list = Restaurant.objects.filter(gu__contains = gu) 
            elif gu != None and resType != None:    # 둘다 선택했을 때
                resType_instance = ResType.objects.get(rtype_name = resType)
                restaurant_list = Restaurant.objects.filter(gu__contains = gu, rtype_name=resType_instance) 
            else: # 업태와 구 모두 선택 안했을 때
                return redirect('search')
        else:   # option을 사용안했을 때
            return redirect('search')
    else: # 검색할 내용이 있을때
        if option: # option을 사용했을 때
            if gu == None and resType != None:      # 업태는 선택했으나 구는 선택을 안했을때
                resType_instance = ResType.objects.get(rtype_name = resType)
                restaurant_list = Restaurant.objects.filter(name__contains = search, rtype_name=resType_instance) 
            elif gu != None and resType == None:    # 구는 선택했으나 업태는 선택을 안했을때
                restaurant_list = Restaurant.objects.filter(name__contains = search, gu__contains = gu) 
            elif gu != None and resType != None:    # 둘다 선택했을 때
                resType_instance = ResType.objects.get(rtype_name = resType)
                restaurant_list = Restaurant.objects.filter(name__contains = search, gu__contains = gu, rtype_name=resType_instance) 
            else: # 업태와 구 모두 선택 안했을 때
                restaurant_list = Restaurant.objects.filter(name__contains = search)
        else: # option을 사용안했을 때
           restaurant_list = Restaurant.objects.filter(name__contains = search)

    # =============pagination 내용=============
    paginator = Paginator(restaurant_list, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    context['contacts'] = contacts
    print("="*30,context)
    return render(request, "search/index.html", context)


def foodSearch(request):
    foodTypes = FoodType.objects.all()
    context = {'foodTypes':foodTypes} 
    return render(request, "search/foorSearch.html", context)

def foodSerched(request, pk):
    connection.cursor()
    rawCursor = connection.connection.cursor()
    foodType = FoodType.objects.get(food_type=pk)
    try :
        rawCursor.execute('select * from FOOD_CATEGORYS where food_type = '+'\'' + foodType.food_type + '\'')
        food_s = rawCursor.fetchall()
    finally :
        rawCursor.close()

    # =============pagination 내용=============
    paginator = Paginator(food_s, 10) # Show 10 contacts per page
    page = request.GET.get('page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    context = readErroMsg(request)
    context['contacts'] = contacts
    return render(request, "search/foodSearched.html", context)

def most_look(request) :
    connection.cursor()
    rawCursor = connection.connection.cursor()
    try :
        reslook = rawCursor.callfunc("reslook", int)
    finally :
        rawCursor.close()
    restaurant = Restaurant.objects.filter(cnt = reslook)
    paginator = Paginator(restaurant, 10) # Show 10 contacts per page
    page = request.GET.get('page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    context = readErroMsg(request)
    context['contacts'] = contacts
    return render(request, "search/index.html", context)

def most_favourite(request) :
    connection.cursor()
    rawCursor = connection.connection.cursor()
    resTypes = ResType.objects.all()
    favouritRes = []
    restaurants = []
    try :
        for resType in resTypes :
            favouritRes.append(rawCursor.callfunc("favouritRes", int, [resType.rtype_name]))
    finally :
        rawCursor.close()
    
    for favourit in favouritRes :
        if (favourit is not None) :
            restaurant = Restaurant.objects.get(restid = favourit)
            restaurants.append(restaurant)
    
    paginator = Paginator(restaurants, 10) # Show 10 contacts per page
    page = request.GET.get('page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    context = readErroMsg(request)
    context['contacts'] = contacts
    return render(request, "search/index.html", context)