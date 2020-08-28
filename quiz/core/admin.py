from django.contrib import admin
from .models import (
    Quiz,
    Question,
    Option,
    Record,
    Response,
)
# Register your models here.

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Record)
admin.site.register(Response)
