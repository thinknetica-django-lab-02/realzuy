from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime

from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'subscriptions', 'avatar', 'phone_number']


class ProfileFormset(
    forms.inlineformset_factory(User, Profile,
                                fields=['birth_date',
                                        'subscriptions',
                                        'avatar',
                                        'phone_number'],
                                can_delete=False,
                                widgets={'birth_date': forms.SelectDateWidget(
                                    years=range(1920, 2020)), })):

    def __init__(self, *args, **kwargs):
        self.__initial = kwargs.pop('initial', [])
        super(ProfileFormset, self).__init__(*args, **kwargs)

    def clean(self):
        super(ProfileFormset, self).clean()

        for form in self.forms:
            try:
                birth_date = form.cleaned_data['birth_date']
            except Exception:
                raise forms.ValidationError('')

            if relativedelta(datetime.now(), birth_date).years < 18:
                raise ValidationError('Возвраст должен быть больше 18 лет')
