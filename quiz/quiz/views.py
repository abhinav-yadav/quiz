from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from core.models import (
    Quiz,
    Record,
)

class Home(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            quizes = Quiz.objects.all()[:5]
            context = {
                'quizes' : quizes,
            }
            return render(request,'homepage.html', context)
        else:
            return render(request,'index.html')



def about(request):
    return render(request,'about.html')


class Setting(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return render(request,'settings.html')
        else:
            return redirect('account_login')


class Activity(View):
    def get(self, request):
        return redirect('completed')

class Completed(View):
    def get(self, request):
        records = Record.objects.filter(user = request.user).distinct('quiz')
        context = {
            'records' : records,
        }
        return render(request,'completed.html',context)

class Created(View):
    def get(self, request):
        quizes = Quiz.objects.filter(author = request.user)
        context = {
            'quizes' : quizes,
        }
        return render(request, 'created.html', context)
