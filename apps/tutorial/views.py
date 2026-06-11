from django.shortcuts import render

def tutorial_home(request):
    return render(request, 'tutorial/index.html')
