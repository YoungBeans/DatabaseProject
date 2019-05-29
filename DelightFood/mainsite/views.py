from django.shortcuts import render

# Create your views here.
def main(request):
    erroType = ''
    erroMsg = ''
    try:
        # error검출하기 위함입니다.
        erroType = 'success'
        erroMsg = 'Success'
    except:
        # error검출하기 위함입니다.
        erroType = 'danger'
        erroMsg = 'faile'
    context = {'erroType':erroType, 'errorMsg':erroMsg}
    return render(request, "mainsite/index.html", context)

def register(request):
    erroType = ''
    erroMsg = ''
    try:
        # error검출하기 위함입니다.
        erroType = 'success'
        erroMsg = 'Success'
    except:
        # error검출하기 위함입니다.
        erroType = 'danger'
        erroMsg = 'faile'
    context = {'erroType':erroType, 'errorMsg':erroMsg}
    return render(request, "mainsite/register.html", context)