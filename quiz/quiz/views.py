from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.db.models import Q

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

class Search(View):
    def get(self,request):
        query = request.GET.get('q')
        # if query[0] == '#':
        #     query = query[1:]
        #     tag = get_object_or_404(Tag, slug=query)
        #     # Filter posts by tag name
        #     articles = Article.objects.filter(tags=tag)
        #     common_tags = Article.tags.most_common()[:4]
        #     context = {
        #         'articles':articles,
        #         'common_tags':common_tags,
        #         'profiles':{},
        #     }
        if query[0] == '@':
            query = query[1:]
            user = User.objects.filter(Q(username__icontains = query))
            length = len(user)
            context = {
                'articles':{},
                'users':user,
                'length' : length
            }
        else:
            if query:
                quizes = Quiz.objects.filter(Q(title__icontains = query)).order_by("-timestamp")
            else:
                quizes = Quiz.objects.all().order_by("-timestamp")[:10]
            length = len(quizes)
            context = {
                        'quizes' : quizes,
                        'profiles':{},
                        'length' : length

            }
        return render(request,'searchresult.html', context)


def autoCompleteView(request):
    if 'term' in request.GET:
        term=request.GET.get('term')
        qs = User.objects.filter(username__icontains=term)
        users = []
        if qs:
            for user in qs:
                users.append(user.username)
        else:
            s='username not found'
            users.append(s)
        return JsonResponse(users, safe=False)

def searchAutoComplete(request):
    if 'term' in request.GET:
        term=request.GET.get('term')
        # if term[0]=='#':
        #     qs = Tag.objects.filter(Q(name__icontains = term[1:]))
        #     q = []
        #     if len(qs)>5:
        #         for _ in range(5):
        #             q.append('#'+qs[_].name)
        #     else:
        #         for _ in qs:
        #             q.append('#'+_.name)

        if term[0]=='@':
            qs = User.objects.filter(Q(username__icontains = term[1:]))
            q = []
            if len(qs)>5:
                for _ in range(5):
                    q.append('@'+qs[_].username)
            else:
                for _ in qs:
                    q.append('@'+_.username)

        else:
            qs = Quiz.objects.filter(Q(title__icontains = term)).order_by("-timestamp")
            q = []
            if len(qs)>5:
                for _ in range(5):
                    q.append(qs[_].title)
            else:
                for _ in qs:
                    q.append(_.title)
        return JsonResponse(q[:5], safe=False)
