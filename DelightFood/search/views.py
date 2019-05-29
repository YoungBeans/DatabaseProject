from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, "search/index.html")

def result(request):
    return render(request, "search/result.html")