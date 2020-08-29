from django.contrib import admin
from .models import (
    Quiz,
    Question,
    Option,
    Record,
    Response,
)
# Register your models here.

class RecordAdmin(admin.ModelAdmin):
    list_display = ['quiz' , 'questions', 'key']


class OptionAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'option']

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option, OptionAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Response)
