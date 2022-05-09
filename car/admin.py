from typing import Callable
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Response)
admin.site.register(Advice)
admin.site.register(Sale)
admin.site.register(Event)