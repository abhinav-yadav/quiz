from django.urls import path
from .views import (
    Test,
    CreateQuiz,
    CreateQuestion,
    AttemptQuiz,
    Result,
    RecordResponse,
)

app_name = 'core'

urlpatterns = [
    path('test/', Test.as_view(), name='test'),
    path('create/', CreateQuiz.as_view(), name = 'create'),
    path('create/<slug>/', CreateQuestion.as_view(), name = 'create_questions'),
    path('attempt/<slug>/', AttemptQuiz.as_view(), name = 'attempt_quiz'),
    path('result/<slug>/<id>/', Result.as_view(), name = 'quiz_result'),
    path('record_response/', RecordResponse.as_view(), name = 'ajax_record_response'),
]
