from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import forms
from . import models
from django.views.generic import TemplateView, ListView, DetailView
from .forms import AccountForm
from django.contrib.auth import authenticate
from django.urls import reverse
#ログイン、ログアウト処理に利用
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django_pandas.io import read_frame
import pandas as pd

#View関数を任意に定義
class Index(TemplateView):
    #テンプレートファイル連携
    template_name="app_folder_HTML/index.html"
    #変数を渡す
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context["message"]="Get処理"
        return context
    #get処理
    def get(self,request,*args,**kwargs):
        return super().get(request,*args,**kwargs)
    #POST処理
    def post(self,request,*args,**kwargs):
        self.kwargs["message"]="Post処理"
        return render(request, self.template_name,context=self.kwargs)


class FormView(TemplateView):
    #初期変数定義
    def __init__(self):
        self.params={"Message":"情報を入力してください。",
                     "form":forms.Contact_Form(),
                     }

    #GET時の処理を記載
    def get(self,request):
        return render(request, "app_folder_HTML/formpage.html",context=self.params)

    #POST時の処理を記載
    def post(self,request):
        if request.method=="POST":
            self.params["form"]=forms.Contact_Form(request.POST)

            #フォーム入力が有効な場合
            if self.params["form"].is_valid():
                self.params["Message"]="入力情報が送信されました。"

        return render(request,"app_folder_HTML/formpage.html",context=self.params)

#アカウント新規登録
class AccountRegistration(TemplateView):
    def __init__(self):
        self.params={
        "AccountCreate":False,
        "account_form":AccountForm(),
        }

    #Get処理
    def get(self,request):
        self.params["account_form"]=AccountForm()
        self.params["AccountCreate"]=False
        return render(request, "app_folder_HTML/register.html", context=self.params)

    #post処理
    def post(self,request):
        self.params["account_form"]=AccountForm(data=request.POST)

        #フォーム入力の有効検証
        if self.params["account_form"].is_valid():
            #アカウント情報をDB保存
            account=self.params["account_form"].save()
            #パスワードをハッシュ化
            account.set_password(account.password)
            #ハッシュ化パスワード更新
            account.save()

            #アカウント作成情報更新
            self.params["AccountCreate"]=True

        else:
            #フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"app_folder_HTML/register.html", context=self.params)

#ログイン
def Login(request):
    #POST
    if request.method=='POST':
        #フォーム入力のユーザーID・パスワード取得
        ID=request.POST.get('userid')
        Pass=request.POST.get('password')

        #Djangoの認証機能
        user=authenticate(username=ID, password=Pass)

        #ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                #ログイン
                login(request,user)
                #ホームページ遷移
                return HttpResponseRedirect(reverse('home'))
            else:
                #アカウント利用不可
                return HttpResponse("アカウントが有効ではりません")
        #ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")

    #Get
    else:
        return render(request,'app_folder_HTML/login.html')

#ログアウト
@login_required
def Logout(request):
    logout(request)
    #ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))

#ホーム
@login_required
def home(request):
    params={"UserID":request.user,}
    return render(request, "app_folder_HTML/home.html",context=params)


#カンパニーリスト
class CompanyList(ListView):
    #Companyテーブル連携
    model = models.Company
    #レコード情報をテンプレートに渡すオブジェクト
    context_object_name = "company_list"
    #テンプレートファイル連携
    template_name = "app_folder_HTML/company_list.html"

    #条件分岐でレコード表示変更
    def get_queryset(self, **kwargs):
        #初期条件：レコードを全て表示(記載は任意)
        queryset = super().get_queryset(**kwargs)

        #Get処理
        if self.request.method == "GET":
            queryset = models.Company.objects.filter(location="Tokyo").order_by("-name")

        #Post処理
        elif self.request.mothod == "POST":
            queryset = models.Company.objects.filter(location="Osaka")
        return queryset

class CompanyDetail(DetailView):
    #Companyテーブル連携
    model = models.Company
    #レコード情報をテンプレートに渡すオブジェクト
    context_object_name = "company_detail"
    #テンプレートファイル連携
    template_name = "app_folder_HTML/company_detail.html"

#とこパデ
class TokopadeIndex(TemplateView):
    template_name="app_folder_HTML/tokopade_top.html"

class TokopadeResult(TemplateView):
    template_name="app_folder_HTML/tokopade_result.html"

class TokopadeHome(TemplateView):
    template_name="app_folder_HTML/tokopade_base.html"

class TokopadeList(ListView):
    #Tokopadeテーブル連携
    queryset=models.Tokopade.objects.order_by('number')
    #レコード情報をテンプレートに渡すオブジェクト
    context_object_name="tokopade_list"
    #テンプレートファイル連携
    template_name="app_folder_HTML/tokopade_result2.html"

class TokopadeDetail(DetailView):
    #Tokopadeテーブル連携
    model=models.Tokopade
    #レコード情報をテンプレートに渡すオブジェクト
    context_object_name="tokopade_detail"
    #テンプレートファイル連携
    template_name="app_folder_HTML/tokopade_detail.html"

class TokopadePlayer(ListView):
    #テンプレートを指定
    model=models.Player
    #template_name="app_folder_HTML/tokopade_player.html"
    template_name="app_folder_HTML/tokopade_test.html"
    #テンプレートファイル連携

    #利用するモデルを指定

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        print(context)
        return context

class TokopadeRanking(ListView):
    # テンプレートを指定
    template_name = "app_folder_HTML/tokopade_ranking1.html"
    # 利用するモデルを指定
    model = models.Player
   
    def get_context_data(self, **kwargs):  # 追加
        context = super().get_context_data(**kwargs)
        qs = models.Player.objects.all()
        df_player = read_frame(qs)
        #df_player['pc_3dig'] = df_player['postalcode'].str[:3]  # postalcodeから最初の３桁抽出し、新しいpc_3dig列作成
       
        # テンプレートで表示させるためのデータフレームdf_contextを準備
        df_context = pd.DataFrame(columns=['name', 'ranking', 'point', 'tokopade'])
        # df_contextへdf_playerのデータを渡す
        df_context['name'] = df_player['name']
        df_context['ranking'] = df_player['ranking']
        df_context['point'] = df_player['point']
        df_context['tokopade'] = df_player['tokopade']
        # df_contextをcontext['df_context']として、テンプレートに渡せるようにする
        #context['df_context'] = df_context
       
        df_ranking=pd.DataFrame(columns=["name","point"])
        for i in range(len(df_context)):
        #for i in range(10):
            player_list={}
            player_list[df_context["name"][i].split("・")[0]]=df_context["point"][i]
            player_list[df_context["name"][i].split("・")[1]]=df_context["point"][i]
            df_ranking=pd.concat([df_ranking,pd.DataFrame(list(player_list.items()),columns=["name","point"])],axis=0)
        df_ranking=df_ranking.groupby("name").sum()
        df_ranking=df_ranking.sort_values("point",ascending=False)
        df_ranking = df_ranking.reset_index()
        df_ranking["ranking"] = df_ranking.point.rank(method="min",ascending=False)
        df_ranking["ranking"] = df_ranking["ranking"].astype(int)
        context['df_ranking'] = df_ranking

        return context
    
'''
        qs=models.Player.objects.all()
        df_player=read_frame(qs)

        #テンプレートで表示させるためのデータフレームdf_cocntextを準備
        #大会結果をdf_contextに格納する
        df_context=pd.DataFrame(columns=['name', 'ranking', 'point', 'tokopade'])
        #df_contextへdf_playerのデータを渡す
        df_context['name']=df_player['name']
        df_context['ranking']=df_player['ranking']
        df_context['point']=df_player['point']
        df_context['tokopade']=df_player['tokopade']
        context['df_context'] = df_context

        return context


        #お試し
        #df_contextから選手のランキングデータdf_rankingを作成する
        df_ranking=pd.DataFrame(columns=["name","point"])
        for i in range(len(df_context)):
            player_list={}
            player_list[df_context["name"][i].split("・")[0]]=df_context["point"][i]
            player_list[df_context["name"][i].split("・")[1]]=df_context["point"][i]
            df_ranking=pd.concat([df_ranking,pd.DataFrame(list(player_list.items()),columns=["name","point"])],axis=0)
        df_ranking=df_ranking.groupby("name").sum()
        df_ranking.sort_values("point",ascending=False)

        #context = {
        #    'rankings' : self.df_ranking.to_html(),
        #}
        #return render(request, 'app_folder_HTML/main.html', context)

        # df_contextをcontext['df_context']として、テンプレートに渡せるようにする
'''
