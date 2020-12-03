# accounts.forms.py
import re
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from accounts.models import SiwesInformation, SupervisorInformation

User = get_user_model()



Session = (
    ('', 'Select Year'),
    ('2018/2019', '2018/2019'),
)

college = (
    ('', 'Select College'),
    ('COLLEGE OF SCIENCE', 'Science'),
    ('COLLEGE OF TECHNOLOGY', 'Technology')
)

Level = (
    ('', 'Select Level'),
    ('300', '300'),
    ('400','400')
)

Department = (
    ('', 'Select Dept'),
    ('Chemistry', 'Chemistry'),
    ('Industrial Chemistry', 'Industrial Chemistry'),
    ('Physics', 'Physics'),
    ('Geophysics', 'Geophysics'),
    ('Geology', 'Geology'),
    ('Computer Science', 'Computer Science'),
    ('Mathematics', 'Mathematics'),
    ('Environmental Management Toxicology', 'Environmental Sci'),
    ('Petroleum Engineering', 'Petroleum Engr'),
    ('Chemical Engineering','Chemical Engr'),
    ('Electrical Electronics Engineering', 'Elect/Elect Engr'),
    ('Mechanical Engineering', 'Mechanical Engr'),
    ('Marine Engineering', 'Marine Engr')
)

sdept = ('Chemistry', 'Industrial Chemistry', 'Physics', 'Geophysics', 'Geology', 'Computer Science', 'Mathematics', 'Environmental Management Toxicology')
tdept = ('Petroleum Engineering', 'Chemical Engineering', 'Electrical Electronics Engineering', 'Mechanical Engineering', 'Marine Engineering')

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('matric_no',  'full_name', 'email', 'session', 'College', 'department', 'level','image')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['matric_no', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


    def clean_matric_no(self):
        a = self.cleaned_data.get('matric_no')
        matric_no = a.upper()
        qs = User.objects.filter(matric_no=matric_no)
        if qs.exists():
            raise forms.ValidationError("Matriculation Number Already Taken")
        else:
            if not re.search("^COS/.*\\d{4}.*/2016$", matric_no) or re.search("^COS/.*\\d{4}.*/2017$", matric_no) or re.search("^COT/.*\\d{4}.*/2015$", matric_no) or re.search("^COT/.*\\d{4}.*/2016$", matric_no):
                raise forms.ValidationError("Invalid Matriculation Number")
        return matric_no

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_level(self):
        College = self.cleaned_data.get('College')
        level   = self.cleaned_data.get('level')
        if not re.search("^CO.*CE$", College) and level == '300':
            raise forms.ValidationError("Recheck College and Level Fields")
        else:
            if not re.search("^CO.*GY$", College) and level == '400':
                raise forms.ValidationError("Recheck College and Level Fields")
        return level

    def clean_department(self):
        College     = self.cleaned_data.get('College')
        department  = self.cleaned_data.get('department')
        if not re.search("^CO.*CE$", College) and department in sdept:
            raise forms.ValidationError("Recheck College and Department Fields")
        else:
            if not re.search("^CO.*GY$", College) and department in tdept:
                raise forms.ValidationError("Recheck College and Department Fields")
        return department

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email', 'full_name', 'matric_no',
            'session', 'email', 'College',
             'department', 'level','image',
             )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'matric_no',  'full_name', 'email',
            'session', 'College', 'department',
            'level','image','password'
            )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'matric_no',  'full_name', 'email',
             'session', 'College', 'department',
             'level','image','password', 'is_active', 'admin'
             )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class EditSiwesForm(forms.ModelForm):
    """A form for updating siwes information. Includes all the fields on
    the SiwesInformation model.
    """

    class Meta:
        model = SiwesInformation
        fields = (
            'bankName', 'accountNo', 'sort_code', 'phoneNo',
            'industryName', 'industryAddress',
             'industrySupervisorname',
             'industrySupervisorPhoneno'
             )
