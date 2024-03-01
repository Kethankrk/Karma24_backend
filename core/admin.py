from django.contrib import admin
from .models import User, UserProfile, Workspace, Todo, Message, Forum


admin.site.register([User, UserProfile, Workspace, Todo, Message, Forum])
