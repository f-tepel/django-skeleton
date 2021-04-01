from django.contrib import admin
from .models import Patient


class PatientAdmin(admin.ModelAdmin):
  pass


admin.site.register(Patient, PatientAdmin)
