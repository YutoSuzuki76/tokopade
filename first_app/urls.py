from django.urls import path
from . import views

#アプリ名を定義
app_name="App"

urlpatterns=[
    path('', views.Login,name='Login'),
    path("logout", views.Logout,name='Logout'),
    path('register', views.AccountRegistration.as_view(),name='register'),
    path('home', views.home,name='home'),
    path('formpage', views.FormView.as_view(),name="formpage"),
    path("index",views.Index.as_view(),name="Index"),
    path("list", views.CompanyList.as_view(),name="list"),
    path("tokopade_home", views.TokopadeHome.as_view(),name="tokopade_home"),
    path("tokopade_result2", views.TokopadeList.as_view(),name="tokopade_result"),
    path("detail/<int:pk>/", views.TokopadeDetail.as_view(),name="detail"),
    path('detail2/<int:pk>/',views.CompanyDetail.as_view(),name='detail2'),
    path('player', views.TokopadePlayer.as_view(), name='tokopade_player'),
    path('tokopade_top', views.TokopadeIndex.as_view(),name="tokopade_top"),
    path('tokopade_about', views.TokopadeResult.as_view(),name="tokopade_about"),
    path('ranking', views.TokopadeRanking.as_view(),name="tokopade_ranking"),
]
