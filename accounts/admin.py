from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import EmailActivation, Profile

User = get_user_model()
# Register your models here.
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    model = User
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'short_name', 'is_superuser', 'is_staff', 'is_client', 'is_active')
    list_filter = ('is_superuser', 'is_staff', 'is_client', 'is_active')
    fieldsets = (
        ('Personal_Info', {'fields': ('first_name', 'middle_name', 'surname', 'email')}),
       # ('Full name', {'fields': ()}),, 'email', 'password'
        ('Permissions', {'fields': ('password', 'is_superuser', 'is_staff', 'is_client', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'full_name',)
    ordering = ('email', 'first_name', 'surname', 'middle_name')
    filter_horizontal = ()

    

admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    def get_inline_instance(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = EmailActivation


admin.site.register(EmailActivation, EmailActivationAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'age', 'sex', 'phone', 'zip_code', 'country')
    list_filter = ('DOB', 'phone', 'zip_code', 'country')
    fieldsets = (
        ('Personal_Info', {'fields': ('user', 'passport', 'sex', 'marital', 'next_of_kin', 'DOB')}),
        ('Contact', {'fields': ('phone', 'fax', 'address', 'zip_code', 'state_province', 'SSN', 'country')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    search_fields = ('user', 'phonr',)
    ordering = ('user', '-DOB')


admin.site.register(Profile, ProfileAdmin)
