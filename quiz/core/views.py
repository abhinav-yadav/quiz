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
    Option,
    Response,
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
        for i in questions:
            questions_order.append(i.id)
        # # resume feature
        # try:
        #     record = Record.objects.filter(quiz=quiz, user=request.user).latest('timestamp')
        #     if datetime.now()-record.timestamp:

        record = Record(user = request.user, quiz=quiz, questions=questions_order)
        key =[]
        for i in questions:
            options = Option.objects.filter(question=i)
            for option in options:
                if option.answer:
                    key.append(option.option)
        record.key = key
        record.save()

        context ={
            'questions' : questions,
            'quiz' : quiz,
        }
        return render(self.request, 'core/quiz_attempt.html', context)

    def post(self, request, slug):
        form = request.POST
        answers =[]
        for key,value in form.items():
            if key != 'csrfmiddlewaretoken' and key != 'button':
                answers.append(value)
        quiz = get_object_or_404(Quiz, slug = slug)
        record = Record.objects.filter(quiz=quiz, user=request.user).latest('timestamp')
        correct_count = 0
        for i in range(len(record.key)):
            if record.key[i] == answers[i]:
                correct_count +=1
        response = Response(record = record, answers = answers, total_questions = quiz.get_total_no_of_questions(), correct = correct_count )
        response.save()
        return redirect('core:quiz_result', slug = quiz.slug, id=record.id)


class Result(View):
    def get(self, request, slug, id):
        quiz = get_object_or_404(Quiz, slug = slug)
        record = get_object_or_404(Record, id = id)
        questions = Question.objects.filter(quiz = quiz)
        response = get_object_or_404(Response, record = record)
        context ={
            'quiz' : quiz,
            'record' : record,
            'questions' : questions,
            'response' : response,
        }
        return render(self.request, 'core/result.html', context)
