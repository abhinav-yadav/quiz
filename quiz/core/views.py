from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.views import View

from datetime import datetime

from .forms import (
    QuizForm,
    QuestionForm,
    OptionForm,
    optionformset,
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
        return redirect('core:edit_quiz', slug = quiz.slug)



class EditQuiz(View):
    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug)
        questions = Question.objects.filter(quiz=quiz)
        context = {
            'quiz' : quiz,
            'questions' : questions,
        }
        return render(self.request, 'core/quiz_edit.html', context)


class CreateQuestion(View):
    # handle the image of the question
    def get(self, request, slug):
        quiz = get_object_or_404(Quiz, slug = slug)
        questionform = QuestionForm(request.GET or None)
        formset = optionformset(queryset = Option.objects.none())
        context = {
            'questionform' : questionform,
            'formset' : formset,
            'quiz' : quiz,
        }
        html_code = render_to_string('core/question_form.html', context, request = request)
        return JsonResponse({ 'html_code' : html_code })

    def post(self, request, slug):
        data = dict()
        quiz = get_object_or_404(Quiz, slug = slug)
        formset = optionformset(request.POST)
        question = QuestionForm(request.POST)
        if question.is_valid() and formset.is_valid():
            question = question.save(commit=False)
            question.quiz = quiz
            question.save()
            for form in formset:
                option = form.save(commit=False)
                if option.option:
                    option.question = question
                    option.save()
            data['form_is_valid'] = True
            messages.success(request, ('question is created successfully for quiz'.format(quiz.title)))
        else:
            data['form_is_valid'] = False
            context = {
                'quiz' : quiz,
                'questionform' : questionform,
                'formset' : formset,
            }
            data['html_code'] = render_to_string('core/question_form.html', context, request=request)
        return JsonResponse(data)

class DeleteQuestion(View):
    def get(self, request, slug,id):
        question = get_object_or_404(Question, id = id)
        question.delete()
        return redirect('core:create_questions',slug = slug)



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

# attempt quiz if atleast one question exists

        record = Record(user = request.user, quiz=quiz, questions=questions_order)
        key =[]
        for i in questions:
            options = Option.objects.filter(question=i)
            for option in options:
                if option.answer:
                    key.append(option.option)
        record.key = key
        record.save()
        # paginator = Paginator(questions, 1)
        # page = request.GET.get('page')
        # questions = paginator.get_page(page)

        context ={
            'questions' : questions,
            'quiz' : quiz,
        }
        # return render(self.request, 'core/quiz_attempt.html', context)
        return redirect('core:attempt', slug = quiz.slug, id=record.id, index=1)

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

# class AttemptQuiz(View):
#     def get(self, request, slug):
#         quiz = get_object_or_404(Quiz, slug=slug)
#         questions  = Question.objects.filter(quiz=quiz).order_by('?')
#         questions_order = []
#         for i in questions:
#             questions_order.append(i.id)
#         # # resume feature
#         # try:
#         #     record = Record.objects.filter(quiz=quiz, user=request.user).latest('timestamp')
#         #     if datetime.now()-record.timestamp:
#
#
#         record = Record(user = request.user, quiz=quiz, questions=questions_order)
#         key =[]
#         for i in questions:
#             options = Option.objects.filter(question=i)
#             for option in options:
#                 if option.answer:
#                     key.append(option.option)
#         record.key = key
#         record.save()
#
#         answers = [None]*len(key)
#         response = Response(record = record, answers = answers ,total_questions = len(key))
#         response.save()
#         # paginator = Paginator(questions, 1)
#         # page = request.GET.get('page')
#         # questions = paginator.get_page(page)
#         question = questions[0]
#         index = 0
#         context ={
#             'question' : question,
#             'quiz' : quiz,
#             'response' : response,
#             'index' : index,
#             'record' : record,
#         }
#         return render(self.request, 'core/quiz_attempt_1.html', context)
#
#     def post(self, request, slug):
#         record = get_object_or_404(Record, id = request.POST.get('record_id'))
#         response = get_object_or_404(Response, id = request.POST.get('response_id'))
#         index = request.POST.get('index')
#         response.answers[index] = request.POST.get('question_response')
#         response.save()
#         index += 1
#         if index < len(record.questions):
#             question = get_object_or_404(Question, id = record.questions[index])
#             response_data['question'] = question
#             response_data['index'] = index
#             return JsonResponse(response_data)
#         else:
#             print('!@@#########################@@!')
#             pass


class Attempt(View):
    def get(self, request, slug, id, index):
        quiz  = get_object_or_404(Quiz, slug = slug)
        record = get_object_or_404(Record, id = id)
        question = get_object_or_404(Question, id = record.questions[index-1])
        number = len(record.questions)
        index += 1
        context = {
            'quiz' : quiz,
            'record' : record,
            'question' : question,
            'index' : index,
            'number' : number,
        }
        return render(self.request, 'core/attempt.html', context)

    def post(self, request, slug, id, index):
        record = get_object_or_404(Record, id = id)
        for key,value in request.POST.items():
            if key != 'csrfmiddlewaretoken' and key != 'button':
                answer = value
        try :
            response = get_object_or_404(Response, record = record)
            response.answers.append(answer)
        except :
            response = Response(record = record,answers = [answer])
        response.save()
        if index <= len(record.questions):
            return redirect('core:attempt', slug = slug, id=id, index = index)
        else:
            count = 0
            for i in range(len(record.key)):
                if record.key[i] == response.answers[i]:
                    count +=1
            response.correct = count
            response.total_questions = len(record.key)
        response.save()
        return redirect('core:quiz_result', slug = slug, id=record.id)



class RecordResponse(View):
    def post(self, request):
        record = get_object_or_404(Record, id = request.POST.get('record_id'))
        response = get_object_or_404(Response, id = request.POST.get('response_id'))
        index = request.POST.get('index')
        response.answers[index] = request.POST.get('question_response')
        response.save()
        index += 1
        if index < len(record.questions):
            question = get_object_or_404(Question, id = record.questions[index])
            response_data['question'] = question
            response_data['index'] = index
            return JsonResponse(response_data)
        else:
            print('!@@#########################@@!')
            pass



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
