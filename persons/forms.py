from django import forms
from persons.models import Person, Task


class SignUpForm(forms.ModelForm):
    password_1 = forms.CharField(max_length=255)
    password_2 = forms.CharField(max_length=255)

    class Meta:
        model = Person
        fields = ['email', 'first_name', 'last_name', 'tg_id', 'password_1', 'password_2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'tg_id': 'Телеграм ID',
            'password_1': 'Пароль',
            'password_2': 'Повтор пароля'
        }

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password_1'] != cd['password_2']:
            raise forms.ValidationError('Passwords dont\' match!')
        return cd['password_2']


class CreateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'text', 'status', 'time_end']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'text': 'Текст',
            'status': 'Статус',
            'time_end': 'Дата выполнения'
        }
