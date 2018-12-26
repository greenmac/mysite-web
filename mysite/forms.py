from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='帳號', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'請輸入帳號'}))
    password = forms.CharField(label='密碼', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'請輸入密碼'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('帳號或密碼不正確')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='帳號', max_length=30, min_length=3, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'請輸入3-30位元的帳號'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'請輸入Email'}))
    password = forms.CharField(label='密碼', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'請輸入6位元以上密碼'}))
    password_again = forms.CharField(label='再輸入一次密碼', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再輸入一次密碼'}))

    def clean_username(self): # _改用大寫不會作用, 會報錯
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('帳號已存在')
        return username

    def clean_email(self): # _改用大寫不會作用, 會報錯
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email已存在')
        return email

    def clean_password_again(self): # _改用大寫不會作用, 會報錯
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('兩次密碼輸入不一致')
        return password_again