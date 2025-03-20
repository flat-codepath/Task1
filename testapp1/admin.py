from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization,SubOrganization,Admin,User, Teacher,Student,Subject,Class,Section

# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(SubOrganization)
class SubOrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(Subject)
class  SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class CustomUserAdmin(UserAdmin):
       fieldsets = UserAdmin.fieldsets + (('working organization', {"fields": ['sub_organization','role']}),)
       

@admin.register(Class) 
class ClassAdmin(admin.ModelAdmin):
    pass

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass



@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    pass





@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
