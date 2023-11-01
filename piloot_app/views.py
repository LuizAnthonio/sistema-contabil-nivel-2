from django.shortcuts import render, redirect
from .models import Empresa, EmpresaDFV, Opcoes, cadastrarNaTab, tema, cadastrarTema
from datetime import date as dt
from datetime import timedelta 
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Avg, Count, Sum
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import locale



varUniverse = "Benehime"
# Create your views here.
def moeda(valor):
        
        novo_valor = f"{valor:_.2f}"
        novo_valor = novo_valor.replace(".",",").replace("_",".")

        return novo_valor
        """
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        valor = locale.currency(valor, grouping=True, symbol=None)

        return valor
        """
        

def totalT(d1,d2,banco,tab):
     valor = 0;

     for i in banco.objects.filter(data__gte=d1,data__lte=d2,tipo_id__in=str(tab)):
          valor += i.valor

     return valor

def totalSum(tab,empresa):
     valor = 0;

     for i in EmpresaDFV.objects.filter(tipo_id__in=str(tab),empresa_id=empresa):
          valor += i.valor

     return valor

          
def realTot(s,data1,data2,margem):
    valorReceita = totalT(data1,data2,EmpresaDFV,3)
    valorSaque = totalT(data1,data2,EmpresaDFV,s)

    margemTotal = valorReceita * (margem/100);
    saldo = margemTotal - valorSaque
    
    #transformar prints em objetos para usar quando retornar
    print(f"total da Margem = {round(margemTotal,2)}")
    print(f"Saque = {round(valorSaque,2)}")
    print(f"Saldo = {round(saldo,2)}")
    return {"margem":round(margemTotal,2), "saque":round(valorSaque,2),"saldo":round(saldo,2)}
    

def converte1(data):
    return {"ano":int(data[0:4]),"mes":int(data[5:7]),"dia":int(data[8:10])}


def cadParcelados(dados):
    
     #print("teste = ",dados)
     cadastrarNaTab(dados)
     n = int(dados["qtd"])

     for i in range(1,n):
        
        aData = converte1(dados["data"])
        ano = aData["ano"]
        mes = aData["mes"]
        dia = aData["dia"]
        
        finalData = f"{dt(ano,mes,dia) + relativedelta(months=1)}"
        dados["data"] = finalData

        cadastrarNaTab(dados)


def olha(obj,n):
    val = 0
    for i in range(0,n):
      val += obj[i].valor
                 
    return val
            

def olhaCompra(obj,n):
    val = 0
    for i in range(0,n):
        val += (obj[i].valor)/2.25
        print(val)
                 
    return val
            


     
        #print("teste2 = ",dados["data"])
        #print(i," - teste3 = ",dados)

@login_required
def SelectEmpresa(request):
     tema1 = tema.objects.get(user_id=request.user.id)
     
     print(tema1)

     
     
     opcoes = {
          "empresas":Empresa.objects.all(),
          "tema":tema1,

     } 
     
     return render(request,"selectEmpresa.html",opcoes)



@login_required
def home(request,empresaSelec):


    
    despesaTotal = totalSum(1,empresaSelec)
    franquiaTotal = totalSum(2,empresaSelec)
    receitaTotal = totalSum(3,empresaSelec)

    saldoTot = receitaTotal - despesaTotal - franquiaTotal

    compraT = receitaTotal/2.5

    lucroT = saldoTot - compraT


    print(moeda(despesaTotal))
    print("despesa: ",despesaTotal)

    uma_data_qualquer = '2023-01-01'

    
    empresa_selecionada = Empresa.objects.get(id_E=empresaSelec)

    ano = dt.today().year
    mes = int(dt.today().month)

   # print(f"{dt.today() + relativedelta(months=2)}")
    
    #cadParcelados({"tes":1,"data":"2023-01-01"})
    tema1 = tema.objects.get(user_id=request.user.id)

    dados = {
         "despesaReal":moeda(despesaTotal),
         "franquiaReal":moeda(franquiaTotal),
         "receitaReal":moeda(receitaTotal),
         "saldoReal":moeda(saldoTot),
         "compraT":moeda(compraT),
         "lucroT":moeda(lucroT),
         "direct":{"despesa":f"despesa/{ano}","franquia":f"franquia/{ano}","receita":f"receita/{ano}","compra":f"compra/{ano}","saldo":f"saldo/{ano}"},
         "direct2":{"despesa":f"despesa-detalhada/{mes}/{ano}","franquia":f"franquia-detalhada/{mes}/{ano}","receita":f"receita-detalhada/{mes}/{ano}","compra":f"compra-detalhada/{mes}/{ano}","saldo":f"saldo-detalhada/{mes}/{ano}"},
         "emp":empresaSelec,
         "tema":tema1,
         "nome":empresa_selecionada,

    }


    return render(request,'home.html',dados)

@login_required
def Anual(request,ano,tipo,empresaSelec):
    tips = tipo
    if(tips == "compra"):
         paginaReal = f'{tips.title()}, insumo e outras'
    else:
        paginaReal = f"{tipo.title()}"
    print(paginaReal)

    tipoOP = []

    for n in Opcoes.objects.all():
         tipoOP.append((n.nome_op).lower())


    if(tipo == "compra" or tipo == "saldo"):
         tipo = "receita"
    
    achador = str(tipoOP.index(tipo) + 1)

    

    meses = ["jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    anual = []
    anosT = []


    for i in range(1,13):
            some = 0
            dataFor = f"{ano}-{i}-1"
            if i > 11 :
                dataFor2 = f"{ano+1}-1-1"
                #print(dataFor, " - ", dataFor2)
                  

            else:
                dataFor2 = f"{ano}-{i+1}-1"
                #print(dataFor, " - ", dataFor2)
                #print(respo)  
                   
            respo1= []
            respo2=[]

            if tips == "saldo":
                 respo1 = EmpresaDFV.objects.filter(data__gte=dataFor,data__lt=dataFor2,tipo_id__in="1",empresa_id=empresaSelec)
                 respo2 = EmpresaDFV.objects.filter(data__gte=dataFor,data__lt=dataFor2,tipo_id__in="2",empresa_id=empresaSelec)

                 
            respo = EmpresaDFV.objects.filter(data__gte=dataFor,data__lt=dataFor2,tipo__in=achador,empresa_id=empresaSelec)
            #print(len(respo))
            #print(olha(respo,len(respo)))
            print(tips)
            if tips == "compra":
                anual.append(olhaCompra(respo,len(respo)))

            elif(tips == "saldo"):
                saldinho = olha(respo,len(respo)) - olha(respo1,len(respo1)) - olha(respo2,len(respo2))

                anual.append((saldinho))
                 
            else: 
                anual.append(olha(respo,len(respo)))
            

                     

               

    print(anual)


         
    dados1 = []

    if tips == "saldo":
        
        
        for i in range(1,4):
             
             for j in EmpresaDFV.objects.filter(tipo_id__in=str(i),empresa_id=empresaSelec):
                dados1.append(j)           
    else:

        dados1 = EmpresaDFV.objects.filter(tipo__in=achador,empresa_id=empresaSelec)

    

    totalGeral = 0
    for a in dados1:
        
         totalGeral += a.valor
         if (((a.data).year not in anosT)):
            anosT.append((a.data).year)
         
    empresa_selecionada = Empresa.objects.get(id_E=empresaSelec)
         

    print(dados1)
    print("anos todos = ",anosT)
    totalAno = sum(anual)
    novoAnual = list(map(moeda,anual))
    print(novoAnual)
    tema1 = tema.objects.get(user_id=request.user.id)
   
    infos = {
            "tema":tema1,
            "pagina":paginaReal,
            "pagDir":tips,
            "meses":meses,
            "anual":novoAnual,
            "total":moeda(totalAno),
            "totalGeral":moeda(totalGeral),
            "ano":ano,
            "anos":anosT,
         "nome":empresa_selecionada,
            "emp":empresaSelec
            
            }

    return render(request,'relatorioAnual.html',infos)

@login_required
def Detalhamento(request,mes,ano,opGlob,empresaSelec):
    print(opGlob)

    vejamos = opGlob.split("-")

    if len(vejamos) > 1:
         opGlob = f"{vejamos[0]} {vejamos[1]}"
    
    
    print(len("uma-coisa".split('-')))
    opcoesGeral = []
    margens = [56.38,3.62,40]

    for u in Opcoes.objects.all():
         opcoesGeral.append((u.nome_op).lower())
         

    achador = str(opcoesGeral.index(opGlob) + 1)

    print(opcoesGeral)
    print(achador)

    meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    meses2 = [{"mes":"Jan","num":1},{"mes":"Fev","num":2},{"mes":"Mar","num":3},{"mes":"Abr","num":4},{"mes":"Mai","num":5},{"mes":"Jun","num":6},{"mes":"Jul","num":7},{"mes":"Ago","num":8},{"mes":"Set","num":9},{"mes":"Out","num":10},{"mes":"Nov","num":11},{"mes":"Dez","num":12}]
    
    
    
    mesSelec = []
    anosT = []
    totalMes = 0

    data = f'{ano}-1-1'
    data2 = f'{ano+1}-1-1'

    
         

    dados1 = EmpresaDFV.objects.filter(tipo__in=achador,empresa_id=empresaSelec)
    dados2 = EmpresaDFV.objects.filter(data__gte=data,data__lt=data2,tipo__in=achador,empresa_id=empresaSelec)

    anualTotal = 0;

    for o in dados2:
         anualTotal += o.valor


    totalGeral = 0
    for a in dados1:
         totalGeral += a.valor
         if (((a.data).year not in anosT)):
            anosT.append((a.data).year)

    print(mes,ano)
    segData = f"{ano}-{mes}-1"
    if mes > 11:
         
        segData2 = f"{ano+1}-1-1"
    else:
        segData2 = f"{ano}-{mes+1}-1"



    indice_Margem = int(achador)-1;
    tabela = int(achador) + 3
    resultadoFinal = realTot(tabela,segData,segData2,margens[indice_Margem])



    empresa_selecionada = Empresa.objects.get(id_E=empresaSelec)

    for i in EmpresaDFV.objects.filter(data__gte=segData,data__lt=segData2,tipo__in=achador,empresa_id=empresaSelec):
        
        #if(( dt(ano,(mes + 1),1) > dt(i.data.year,i.data.month,i.data.day) >= dt(ano,mes,1) )):
            totalMes += i.valor
            i.valor = moeda(i.valor)
            mesSelec.append(i)
            
        
    
    #print(dt(2023,1,1))
    print("valor total ",totalMes)
    paginaReal = f"{opGlob.title()} Detalhada"
    print(paginaReal)
    atual_mes = meses[mes-1]
   
    print(resultadoFinal['margem'])
    tema1 = tema.objects.get(user_id=request.user.id)
    infos = {
            "pagina":paginaReal,
         "nome":empresa_selecionada,
            "paginaG":opGlob,
            "dados":mesSelec,
            "totalMes":moeda(totalMes),
            "mes":atual_mes,
            "anoIni":ano,
            "meses2":meses2,
            "anosT":anosT,
            "anualTotal":moeda(anualTotal),
            "margem":moeda(resultadoFinal["margem"]),
            "saldo":moeda(resultadoFinal["saldo"]),
            "saque":moeda(resultadoFinal["saque"]),
            "percent":moeda(margens[indice_Margem]),
            "emp":empresaSelec,
            "tema":tema1,
            
            }

    return render(request,'relatorioDetalhado.html',infos)

@login_required
def Periodo(request,empresaSelec):
    mesSelec = []
    totalMes = 0
    geral = False
    if request.method == "GET":

        busca = request.GET.get("busca")
        data_inicio = request.GET.get("inicio")
        data_fim = request.GET.get("fim")
        tipo = str(request.GET.get("tipo"))

        

        print("busca",busca)
        print("inicio",data_inicio)
        print(data_fim == "")
        print("fim",data_fim)
        #print("tipo",tipo)

        
             








        if(data_fim == None and data_inicio == None and busca == None):
            po = 0
            for i in EmpresaDFV.objects.filter(empresa_id=empresaSelec):
                    po += 1
                    i.posi = po
                    totalMes += i.valor
                    i.valor = moeda(i.valor)
                    mesSelec.append(i)

        elif(data_fim == "" and data_inicio == "" and busca != None):

            po = 0
            for i in EmpresaDFV.objects.filter(titulo__icontains=busca,empresa_id=empresaSelec):
                
                    po += 1
                    i.posi = po
                    totalMes += i.valor
                    i.valor = moeda(i.valor)
                    mesSelec.append(i)
                    geral = False
        
        else:
            
            po = 0
            for i in EmpresaDFV.objects.filter(data__gte=data_inicio,data__lte=data_fim,titulo__icontains=busca,empresa_id=empresaSelec):
        
                    po += 1
                    i.posi = po
                    totalMes += i.valor
                    i.valor = moeda(i.valor)
                    mesSelec.append(i)
                    geral = True


    empresa_selecionada = Empresa.objects.get(id_E=empresaSelec)
    
                
            
    
    #print(dt(2023,1,1))
    tema1 = tema.objects.get(user_id=request.user.id)
    infos = {
         
            "pagina":"Periodo",
             "dados":mesSelec,
             "geral":geral,
             "totalMes":moeda(totalMes),
             "inicio":data_inicio,
             "fim":data_fim,
             "emp":empresaSelec,
             "tema":tema1,
             "nome":empresa_selecionada,
             
             }

    print("valor total ",totalMes)
    return render(request,'periodo.html',infos)

@login_required
def registerEmpresa(request):

    empresa = Empresa()

    tema1 = tema.objects.get(user_id=request.user.id)

    infos = {
    "tema":tema1,
         
    }
    if request.method == "POST":
        print(request.POST.get("empresa"))
        empresa.nome_empresa = request.POST.get("empresa")
        empresa.save()

        return redirect('SelectEmpresa')

    else:
        return render(request,'registerEmpresa.html',infos)

@login_required
def lancar(request):

    tema1 = tema.objects.get(user_id=request.user.id)

    
    print(Empresa.objects.all())

    opcoes = {
              "empresas": Empresa.objects.all(), 
              "opcoes":Opcoes.objects.all(),
              "tema":tema1,

              }




    if request.method == "POST":
        
        print('titulo ',request.POST.get("titulo"))
        print('opcao ',request.POST.get("opcao-ipunt"))
        print('data ',request.POST.get("data"))
        print('valor ',request.POST.get("valor"))
        print('empresas ',request.POST.get("empresas"))
        print('radiop ',request.POST.get("radiop"))
        #print('qtd ',request.POST.get("qtd"))

       
        if(request.POST.get("radiop") == "True"):
            #print("qtd = 1")
            
            dados = {"titulo":request.POST.get("titulo"),
                     "tipo":request.POST.get("opcao-ipunt"),
                     "qtd":1,
                     "data":request.POST.get("data"),
                     "valor":request.POST.get("valor"), 
                     "empresa": request.POST.get("empresas")}    
            
            cadastrarNaTab(dados)
          

        else:
            dados = {"titulo":request.POST.get("titulo"),
                     "tipo":request.POST.get("opcao-ipunt"),
                     "qtd":int(request.POST.get("qtd")),
                     "data":request.POST.get("data"),
                     "valor":request.POST.get("valor"), 
                     "empresa": request.POST.get("empresas")}    
            #cadastrarNaTab(dados)
            cadParcelados(dados)
            #print("qtd = ",request.POST.get("qtd"))

        
       
       # cadastrarNaTab()
        

        return render(request,'registrar.html',opcoes)

    else:
        #opcoes = {"empresas": empresas.objects.all()}
        return render(request,'registrar.html',opcoes)
    

def cadastrarUser(request):

    

    if(request.method == "POST"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        tema = request.POST.get("tema")
         

        user = User.objects.filter(username=username)

        if user:
             return render(request,"cadastrar.html",{"msg":"Já existe uma pessoa com esse nome"})


        user = User.objects.create_user(username=username,password=password)
        user.save()

        print("criou\n")

        idUser = User.objects.get(username=username)
        print(idUser)
        print(idUser.id)
        dadosTema = {"user":idUser,"temaEsc":tema}
        cadastrarTema(dadosTema)
        print("tema cadastrado!\n")

        


        return redirect("login")


     


    return render(request,"cadastrar.html")


def Config(request):
     
     tema1 = tema.objects.get(user_id=request.user.id)

     if request.method == "POST":
        user = request.user.id
        otema = tema.objects.get(user_id=user)
        otema.tema_escolhido = request.POST.get("tema")
        otema.save()
        return redirect("config")

      
     else:
        return render(request,'config.html',{"tema":tema1})
          
def inicio(request):
     return redirect("SelectEmpresa")
    



     


         