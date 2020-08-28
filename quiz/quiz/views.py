from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

class Home(View):
    def get(self, request):
        test = "hell no"
        context = {
            'test':test,
        }
        return render(request,'home.html',context)
