from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from core.models import (
    Quiz,
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
