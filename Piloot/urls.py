
from django.contrib import admin
from django.urls import path, include
from piloot_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.inicio,name="inicio"),
    path("home/<int:empresaSelec>/",views.home, name="home"),
    path("select-empresa/",views.SelectEmpresa,name="SelectEmpresa"),
    path("lancar/",views.lancar,name="lancar"),
    path("register-empresa/",views.registerEmpresa,name="registerEmpresa"),
    path("<int:empresaSelec>/<str:tipo>/<int:ano>/",views.Anual,name="Anual"),
    path("<int:empresaSelec>/periodo/",views.Periodo,name="periodo"),
    path("config/",views.Config,name="config"),
    path("secreto/supersecreto/cadastrar/user/",views.cadastrarUser,name="registrarUser"),
    path("cadastrar/opcao/",views.cadastrarOp,name="registrarOp"),
    path("<int:empresaSelec>/<str:opGlob>-detalhada/<int:mes>/<int:ano>/",views.Detalhamento,name="Detalhamento"),
    path('accounts/',include("django.contrib.auth.urls"))
   

]
