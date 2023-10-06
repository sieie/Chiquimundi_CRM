from django.contrib import admin
from .models import User, Lead, Agent, UserProfile, Category, Articulo, Proforma

admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(Articulo)
admin.site.register(Proforma)