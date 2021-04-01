from django.contrib import admin
from .models import Company, Whitelabel


class CompanyAdmin(admin.ModelAdmin):
  pass


class WhitelabelAdmin(admin.ModelAdmin):
  pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(Whitelabel, WhitelabelAdmin)
