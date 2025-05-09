from django.contrib import admin

# Models
from .models.user import User

# Register your models here.
# Necessário registrar os models criados aqui
admin.site.register(User)