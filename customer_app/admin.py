from django.contrib import admin
from .models import Domain, ExpirationDate, UpdatedDate, CreationDate, Email

admin.site.register(Domain)
admin.site.register(ExpirationDate)
admin.site.register(UpdatedDate)
admin.site.register(CreationDate)
admin.site.register(Email)

