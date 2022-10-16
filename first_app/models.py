from django.db import models
#ユーザー認証
from django.contrib.auth.models import User

#モデルクラスを作成する
class People(models.Model):
    Name=models.CharField(max_length=100)
    Tell=models.IntegerField(blank=True, null=True)
    Mail=models.EmailField(max_length=100)
    Birthday=models.DateField()
    website=models.URLField()
    FreeText=models.TextField()

#ユーザーアカウントのモデルクラス
class Account(models.Model):
    #ユーザー認証のインスタンス(1vs1関係)
    #ユーザー(ユーザー名、パスワード、メールアドレス)
    user=models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Company(models.Model):
    name=models.CharField(max_length=256)
    industory=models.CharField(max_length=256)
    location=models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name=models.CharField(max_length=256)
    age=models.PositiveIntegerField()
    company=models.ForeignKey(Company,related_name="Employees",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Tokopade(models.Model):
    number=models.IntegerField(null=True)
    tournament=models.CharField(max_length=256,null=True)
    name=models.CharField(max_length=256,null=True)
    date=models.DateField(null=True)

    def __str__(self):
        return self.tournament

class Player(models.Model):
    name=models.CharField(max_length=256)
    ranking=models.PositiveIntegerField(null=True)
    point=models.PositiveIntegerField(null=True)
    tokopade=models.ForeignKey(Tokopade,related_name="Players",on_delete=models.CASCADE)

    def __str__(self):
        return self.name
