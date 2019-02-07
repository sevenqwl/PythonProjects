from django.contrib import admin
from Info_test import models

# Register your models here.

class PositionsRelationAdmin(admin.ModelAdmin):
    list_display = ('ip', 'position', 'description')

class PhoneConfigurationOptionsAdmin(admin.ModelAdmin):
    list_display = ('platform', 'Sip1_Enable', 'Sip1_AuthPassword', 'Sip1_RegistrarServer', 'Sip1_UseOutboundProxy', 'Sip1_OutboundProxy', 'Sip2_Enable', 'Sip2_AuthPassword', 'Sip2_RegistrarServer', 'Sip2_UseOutboundProxy', 'Sip2_OutboundProxy')


admin.site.register(models.PositionsRelation, PositionsRelationAdmin)
admin.site.register(models.PhoneConfigurationOptions, PhoneConfigurationOptionsAdmin)
