from django.contrib import admin
from .models import Owner, SimpleUser, Group, Field, FieldAnswer


admin.site.register(Owner)
admin.site.register(SimpleUser)
admin.site.register(Group)
admin.site.register(Field)
admin.site.register(FieldAnswer)
