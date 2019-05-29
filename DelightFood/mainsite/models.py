# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Avgprice(models.Model):
    avgid = models.FloatField(primary_key=True)
    food_type = models.ForeignKey('FoodType', models.DO_NOTHING, db_column='food_type', blank=True, null=True)
    rtype_name = models.ForeignKey('ResType', models.DO_NOTHING, db_column='rtype_name', blank=True, null=True)
    unit = models.CharField(max_length=20)
    avgprice = models.FloatField()
    update_date = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'avgprice'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Favourite(models.Model):
    favid = models.FloatField(primary_key=True)
    userid = models.FloatField()
    restid = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='restid')

    class Meta:
        managed = True
        db_table = 'favourite'


class FoodType(models.Model):
    food_type = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = True
        db_table = 'food_type'


class FoodTypes(models.Model):
    typesid = models.FloatField(primary_key=True)
    menuid = models.ForeignKey('Menu', models.DO_NOTHING, db_column='menuid', blank=True, null=True)
    food_type = models.ForeignKey(FoodType, models.DO_NOTHING, db_column='food_type', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'food_types'


class Menu(models.Model):
    menuid = models.FloatField(primary_key=True)
    restid = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='restid')
    name = models.CharField(max_length=20, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'menu'


class Rate(models.Model):
    rateid = models.FloatField(primary_key=True)
    restid = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='restid', blank=True, null=True)
    userid = models.FloatField(blank=True, null=True)
    rate = models.FloatField()

    class Meta:
        managed = True
        db_table = 'rate'


class ResType(models.Model):
    rtype_name = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = True
        db_table = 'res_type'


class Restaurant(models.Model):
    restid = models.FloatField(primary_key=True)
    rtype_name = models.ForeignKey(ResType, models.DO_NOTHING, db_column='rtype_name', blank=True, null=True)
    name = models.CharField(max_length=10)
    tel = models.CharField(max_length=20)
    update_date = models.CharField(max_length=20)
    si = models.CharField(max_length=20)
    gu = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    cnt = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'restaurant'


class UserInfo(models.Model):
    userid = models.FloatField(primary_key=True)
    email = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'user_info'
