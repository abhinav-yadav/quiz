from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View

from datetime import datetime

from .forms import (
    QuizForm,
    QuestionForm,
    OptionForm,
)
from .models import (
    Quiz,
    Question,
    Record,
)


class Test(View):
    def get(self, request):
        test = "hell no"
        context = {
            'test':test,
        }
        return render(request, 'core/test.html', context)

class CreateQuiz(View):
    def get(self, request):
        quizform = QuizForm(request.GET or None)
        context = {
            'form': quizform,
        }
        return render(request, 'core/create.html',context)

    def post(self, request):
        quizform = QuizForm(request.POST or None)

        if quizform.is_valid():
            quiz = quizform.save(commit = False)
            quiz.author = request.user
            if 'image' in request.FILES:
                quiz.image = request.FILES['image']
            quiz.save()
        else :
            message.error(request,('please correct the below errrors'))
            context = {
                'form' : quizform,
                }
            return render(self.request, 'core/create.html', context)
        return redirect('core:create_questions', slug = quiz.slug)

class CreateQuestion(View):
    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)
        questionform = QuestionForm(request.GET or None)
        optionform = OptionForm(request.GET or None)
        context = {
            'quiz' : quiz,
            'questionform' : questionform,
            'optionform' : optionform,
        }
        return render(self.request, 'core/question_create.html', context)

    # post handel


class AttemptQuiz(View):
    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)
        questions  = Question.objects.filter(quiz=quiz).order_by('?')
        questions_order = []
        # for i in questions:
        #     questions_order.append(i.id)
        # # resume feature
        # try:
        #     record = Record.objects.filter(quiz=quiz, user=request.user).latest('timestamp')
        #     if datetime.now()-record.timestamp:

        record = Record(user = request.user, quiz=quiz, questions=questions_order)
        record.save()

        context ={
            'questions' : questions,
            'quiz' : quiz,
        }
        return render(self.request, 'core/quiz_attempt.html', context)

    def post(self, request, slug):
        context = {
        }
        return redirect('core:create_questions', slug = slug)
