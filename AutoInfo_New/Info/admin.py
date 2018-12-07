from django.contrib import admin
from Info import models

# Register your models here.

class PositionsRelationAdmin(admin.ModelAdmin):
    list_display = ('ip','position', 'description')


admin.site.register(models.PositionsRelation, PositionsRelationAdmin)
