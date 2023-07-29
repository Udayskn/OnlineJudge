from django.contrib import admin

# Register your models here.
from home.models import Problem,TestCase
admin.site.register(Problem)
admin.site.register(TestCase)