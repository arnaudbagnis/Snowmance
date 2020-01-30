from django.contrib import admin
# Register your models here.
from app.models.category import Category
from app.models.person import Person
from app.models.tag import Tag
from app.models.visitor import Visitor

admin.site.register(Category)
admin.site.register(Person)
admin.site.register(Tag)
admin.site.register(Visitor)
