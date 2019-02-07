# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AutoexecKeywords(models.Model):
    index_keywords = models.CharField(max_length=100, blank=True, null=True)
    second_keywords = models.CharField(max_length=100, blank=True, null=True)
    third_keywords = models.CharField(max_length=100, blank=True, null=True)
    exclude_index_keywords = models.CharField(max_length=255, blank=True, null=True)
    exclude_second_keywords = models.CharField(max_length=255, blank=True, null=True)
    exclude_third_keywords = models.CharField(max_length=255, blank=True, null=True)
    relationid = models.IntegerField(blank=True, null=True)
    workorder_category = models.CharField(max_length=50, blank=True, null=True)
    workorder_solution = models.CharField(max_length=255, blank=True, null=True)
    finish_time = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'autoexec_keywords'


class AutoexecWorkorder(models.Model):
    workorder_id = models.CharField(max_length=50)
    workorder_submittime = models.CharField(max_length=50, blank=True, null=True)
    workorder_position = models.CharField(max_length=50, blank=True, null=True)
    workorder_email = models.CharField(max_length=50)
    workorder_ip = models.CharField(max_length=50)
    workorder_computer = models.CharField(max_length=50)
    workorder_summary = models.CharField(max_length=255)
    relationid = models.CharField(max_length=255)
    process_user = models.CharField(max_length=50, blank=True, null=True)
    user_status = models.CharField(max_length=50, blank=True, null=True)
    workorder_status = models.CharField(max_length=50, blank=True, null=True)
    workorder_closetime = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'autoexec_workorder'


class Encryptinfo(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    encryptdata = models.CharField(max_length=255, blank=True, null=True)
    function = models.CharField(max_length=50, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'encryptinfo'


class Erpinfo(models.Model):
    mail = models.CharField(max_length=50, blank=True, null=True)
    erp = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'erpinfo'


class Hardwareinfo(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    extension = models.CharField(max_length=50, blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    computer = models.CharField(max_length=50, blank=True, null=True)
    sn = models.CharField(max_length=100, blank=True, null=True)
    ip1 = models.CharField(max_length=50, blank=True, null=True)
    mac1 = models.CharField(max_length=50, blank=True, null=True)
    ip2 = models.CharField(max_length=50, blank=True, null=True)
    mac2 = models.CharField(max_length=50, blank=True, null=True)
    osarch = models.CharField(db_column='OSArch', max_length=50, blank=True, null=True)  # Field name made lowercase.
    os = models.CharField(max_length=100, blank=True, null=True)
    border = models.CharField(max_length=100, blank=True, null=True)
    cpu = models.CharField(max_length=100, blank=True, null=True)
    memory = models.CharField(max_length=50, blank=True, null=True)
    disk = models.CharField(max_length=50, blank=True, null=True)
    partion_c = models.CharField(db_column='partion_C', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nic = models.CharField(max_length=255, blank=True, null=True)
    graphics = models.CharField(max_length=255, blank=True, null=True)
    sound = models.CharField(max_length=255, blank=True, null=True)
    ping_status = models.CharField(max_length=50, blank=True, null=True)
    domain_date = models.DateField(blank=True, null=True)
    domain_time = models.TimeField(blank=True, null=True)
    domain_status = models.CharField(max_length=50, blank=True, null=True)
    domain_status_switch = models.CharField(max_length=50, blank=True, null=True)
    define_status = models.CharField(max_length=50, blank=True, null=True)
    define_scripts_option = models.CharField(max_length=50, blank=True, null=True)
    define_scripts = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=255, blank=True, null=True)
    define_content = models.CharField(max_length=255, blank=True, null=True)
    third_categoryid = models.CharField(max_length=50, blank=True, null=True)
    define_date = models.DateField(blank=True, null=True)
    define_time = models.TimeField(blank=True, null=True)
    domain_status_process_switch = models.CharField(max_length=50, blank=True, null=True)
    userinfo_process_switch = models.CharField(max_length=50, blank=True, null=True)
    exec_process = models.CharField(max_length=50, blank=True, null=True)
    exec_type = models.CharField(max_length=50, blank=True, null=True)
    workorder_id = models.CharField(max_length=50, blank=True, null=True)
    finish_time = models.CharField(max_length=50, blank=True, null=True)
    kbids = models.CharField(max_length=10000, blank=True, null=True)
    kbnums = models.IntegerField(blank=True, null=True)
    kbdate = models.DateField(blank=True, null=True)
    kbtime = models.TimeField(blank=True, null=True)
    scepversion = models.CharField(db_column='SCEPversion', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'hardwareinfo'


class HardwareinfoSettingRecord(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    computer = models.CharField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    mac = models.CharField(max_length=50, blank=True, null=True)
    define_scripts_option = models.CharField(max_length=50, blank=True, null=True)
    define_scripts = models.CharField(max_length=255, blank=True, null=True)
    summary = models.CharField(max_length=255, blank=True, null=True)
    define_content = models.CharField(max_length=255, blank=True, null=True)
    exec_process = models.CharField(max_length=50, blank=True, null=True)
    exec_type = models.CharField(max_length=50, blank=True, null=True)
    capture_logfolder = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'hardwareinfo_setting_record'


class IndexCategory(models.Model):
    index_categoryid = models.CharField(max_length=50, blank=True, null=True)
    index_category = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        
        db_table = 'index_category'


class Kbinfo(models.Model):
    kbid = models.CharField(max_length=50, blank=True, null=True)
    checkstatus = models.CharField(max_length=50, blank=True, null=True)
    checkstatus_users = models.CharField(max_length=50, blank=True, null=True)
    display_status = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        
        db_table = 'kbinfo'


class LoginRecord(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    client_ip = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    login_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'login_record'


class Logininfo(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    computer = models.CharField(max_length=50, blank=True, null=True)
    ip1 = models.CharField(max_length=50, blank=True, null=True)
    mac1 = models.CharField(max_length=50, blank=True, null=True)
    ip2 = models.CharField(max_length=50, blank=True, null=True)
    mac2 = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'logininfo'


class NetworkSegment(models.Model):
    network_segment = models.CharField(max_length=50)
    floor = models.CharField(max_length=50, blank=True, null=True)
    function = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'network_segment'


class Phoneinfo(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    mac = models.CharField(max_length=50, blank=True, null=True)
    sip1 = models.CharField(max_length=50, blank=True, null=True)
    sip1_status = models.CharField(max_length=50, blank=True, null=True)
    sip1_server = models.CharField(max_length=50, blank=True, null=True)
    sip1_outbound = models.CharField(max_length=50, blank=True, null=True)
    sip2 = models.CharField(max_length=50, blank=True, null=True)
    sip2_status = models.CharField(max_length=50, blank=True, null=True)
    sip2_server = models.CharField(max_length=50, blank=True, null=True)
    sip2_outbound = models.CharField(max_length=50, blank=True, null=True)
    update_server = models.CharField(max_length=100, blank=True, null=True)
    ping_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'phoneinfo'


class PhoneinfoSettingRecord(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    extension = models.CharField(max_length=50, blank=True, null=True)
    settingip = models.CharField(max_length=50, blank=True, null=True)
    ping_status = models.CharField(max_length=50, blank=True, null=True)
    exec_type = models.CharField(max_length=50, blank=True, null=True)
    exec_status = models.CharField(max_length=50, blank=True, null=True)
    exec_remarks = models.CharField(max_length=255, blank=True, null=True)
    exec_logs = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'phoneinfo_setting_record'


class SecondCategory(models.Model):
    second_categoryid = models.CharField(max_length=50, blank=True, null=True)
    second_category = models.CharField(max_length=100, blank=True, null=True)
    fatherid = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'second_category'


class SoftwareInstallation(models.Model):
    software = models.CharField(max_length=255, blank=True, null=True)
    switch = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'software_installation'


class SwitchDevice(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    hostname = models.CharField(max_length=50, blank=True, null=True)
    function = models.CharField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    mac = models.CharField(max_length=50, blank=True, null=True)
    sn = models.CharField(db_column='SN', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        
        db_table = 'switch_device'


class Switchinfo(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    hostname = models.CharField(max_length=50, blank=True, null=True)
    function = models.CharField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    port = models.CharField(max_length=50, blank=True, null=True)
    mac = models.CharField(max_length=255, blank=True, null=True)
    sourcemac = models.CharField(max_length=255, blank=True, null=True)
    vlan = models.CharField(max_length=50, blank=True, null=True)
    port_status = models.CharField(max_length=50, blank=True, null=True)
    protocol_status = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'switchinfo'


class SwitchinfoSettingRecord(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    port = models.CharField(max_length=50, blank=True, null=True)
    ping_status = models.CharField(max_length=50, blank=True, null=True)
    exec_type = models.CharField(max_length=50, blank=True, null=True)
    exec_status = models.CharField(max_length=50, blank=True, null=True)
    exec_remarks = models.CharField(max_length=255, blank=True, null=True)
    exec_logs = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'switchinfo_setting_record'


class ThirdCategory(models.Model):
    third_categoryid = models.CharField(max_length=50, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    user_visible = models.CharField(max_length=10, blank=True, null=True)
    third_category = models.CharField(max_length=100, blank=True, null=True)
    define_scripts_option = models.CharField(max_length=50, blank=True, null=True)
    define_scripts = models.CharField(max_length=255, blank=True, null=True)
    define_content = models.CharField(max_length=255, blank=True, null=True)
    exec_process = models.CharField(max_length=50, blank=True, null=True)
    fatherid = models.CharField(max_length=50, blank=True, null=True)
    image_icon = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'third_category'


class User(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'user'


class WindowsUpdate(models.Model):
    ip1 = models.CharField(max_length=50, blank=True, null=True)
    computer = models.CharField(max_length=50, blank=True, null=True)
    mac1 = models.CharField(max_length=50, blank=True, null=True)
    update_date = models.DateField(blank=True, null=True)
    update_time = models.TimeField(blank=True, null=True)
    kbid = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'windows_update'

class PositionsRelation(models.Model):
    ip = models.CharField(max_length=50, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    # area = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        
        db_table = 'positions_relation'


class PhoneConfigurationOptions(models.Model):
    status_choices = (('Enabled', u'启用'),
                      ('Disabled', u'禁用'),
                      )
    boolean_choices = (('true', u'启用'),
                      ('false', u'禁用'),
                      )

    platform = models.CharField(max_length=50, blank=True, null=True)
    Sip1_Enable = models.CharField(choices=status_choices, default='Enabled', max_length=32)
    Sip1_AuthPassword = models.CharField(max_length=50, blank=True, null=True)
    Sip1_RegistrarServer = models.CharField(max_length=50, blank=True, null=True)
    Sip1_UseOutboundProxy = models.CharField(choices=status_choices, default='Enabled', max_length=32)
    Sip1_OutboundProxy = models.CharField(max_length=50, blank=True, null=True)
    Sip1_AutoAnswerEnable = models.CharField(choices=boolean_choices, default='false', max_length=32)
    Sip2_Enable = models.CharField(choices=status_choices, default='Disabled', max_length=32)
    Sip2_AuthPassword = models.CharField(max_length=50, blank=True, null=True)
    Sip2_RegistrarServer = models.CharField(max_length=50, blank=True, null=True)
    Sip2_UseOutboundProxy = models.CharField(choices=status_choices, default='Disabled', max_length=32)
    Sip2_OutboundProxy = models.CharField(max_length=50, blank=True, null=True)
    Sip2_AutoAnswerEnable = models.CharField(choices=boolean_choices, default='false', max_length=32)
    AdminPassword = models.CharField(max_length=50, blank=True, null=True)
    AutopServerAddress = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'phone_configuration_options'


class CeleryTaskRecord(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    task_id = models.CharField(max_length=50, blank=True, null=True)
    task_name = models.CharField(max_length=50, blank=True, null=True)
    args = models.CharField(max_length=255, blank=True, null=True)
    kwargs = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'celery_task_record'