from django import forms
from django.contrib.auth.models import User
from .models import Account

#フォームクラス作成
class Contact_Form(forms.Form):
    Name=forms.CharField(label="名前")
    Tell=forms.IntegerField(label="電話番号")
    Mail=forms.EmailField(label="メールアドレス")
    Birthday=forms.DateField(label="生年月日")
    website=forms.URLField(label="webサイト")
    FreeText=forms.CharField(widget=forms.Textarea,label="備考")

class AccountForm(forms.ModelForm):
    #パスワード入力：非表示対応
    password=forms.CharField(widget=forms.PasswordInput(), label="パスワード")

    class Meta():
        #ユーザー認証
        model=User
        #フィールド指定
        fields=('username','email','password')
        #フィールド名指定
        labels={'username':"ユーザーID", 'email':"メール"}
