from django.contrib import admin
from crm import models
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'qq', 'source')

admin.site.register(models.Customer)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Enrollment)
admin.site.register(models.Tag)
admin.site.register(models.Course)
admin.site.register(models.Branch)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.Payment)
admin.site.register(models.UserProfile)
admin.site.register(models.Role)

