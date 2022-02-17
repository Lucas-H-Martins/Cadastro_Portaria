# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 09:51:07 2022

@author: TI
"""

from tkinter import *
import tkinter as tk
from tkinter import ttk
import datetime as dt
import pandas as pd
from tkinter import messagebox
import numpy as np

root=Tk()
#estou utilizando um banco de dados em excel, posteriormente vou trocar para um banco de dados em SQL, porem para fins de implementação, este me atende no momento.
diretorio='C:\\Users\\TI\Desktop\\progamação\\portaria\\portaria.xlsx'
dados=pd.read_excel(diretorio)#utilizando o pandas para manipular os dados em excel por isso importo o documento onde ele fica, o usuario precisa ter pemissao de gravação nesta pasta.

#aqui as funções que vou utilizar no meu sistema
class funcoes():
    def limpar_tela(self):
        self.placa_get.delete(0,END)
        self.nome_get.delete(0,END)
        # print('Limpar')
    def limpar_frame2(self):
        # self.frame_2.destroy()
        for widget in self.frame_2.winfo_children():
            widget.destroy()
    def registrar_entrada(self):
        placa=self.placa_get.get()
        modelo=self.option_veiculo.get()
        carga=self.option_carga.get()
        motorista=self.nome_get.get()
        transportador=self.transportador_get.get()
        observacao=self.observacao_get.get()
        nf=np.nan
        entrada=dt.datetime.now()    
        entrada=entrada.strftime("%d/%m/%Y %H:%M")
        saida=np.nan
        if placa == "":
           messagebox.showwarning("ERRO", "Placa não pode ser vazio")
           return()
        if len(placa)!=7 :
           messagebox.showwarning("ERRO", "Placa Precisa de ter 7 digitos")
           return()
        if motorista == "":
           messagebox.showwarning("ERRO", "Motorista não pode ser vazio")
           return()
       

        else:        
            #verificando onde temos dados com entrada selecionada sem saida
            df_mask=dados[dados.Placa.isin([placa])&dados.Saida.isin([np.nan])]
            
            #tratando a condição se a identificação estiver sendo usada, ou não.
            if df_mask.empty is True:
                # print('Pode Cadastrar')
                dados.loc[len(dados.index)]=[placa,modelo,entrada,saida,motorista,carga,transportador,nf,observacao]
                
                gravador = pd.ExcelWriter(diretorio,engine='xlsxwriter')
                dados.to_excel(gravador, index=False,sheet_name='Entrada')            
                gravador.save()
                gravador.close()
                messagebox.showinfo("SUCESSO", "Cadastro Entrada Realizado com Sucesso")
                self.limpar_entrada()
                
                
                
            else:
                messagebox.showwarning("ERRO", "PLACA SEM SAIDA")
                return()


    def registrar_saida(self):
        placa=self.placa_get.get()
        
        nf=self.nf_get.get()
        saida=dt.datetime.now()    
        saida=saida.strftime("%d/%m/%Y %H:%M")
        if placa=="":
            messagebox.showwarning("ERRO", "Placa não pode ser vazio")
            return()

        if nf =="":
            messagebox.showwarning("ERRO", "NF não pode ser vazio")
            return()
        if (int(nf)==nf):
            messagebox.showwarning("ERRO", "NF SO PODE TER NUMEROS")
            return()      
        
        else:
            #verificando se a identidade que esta sendo utilizada ja foi  dado saida
            df_mask=dados[dados.Placa.isin([placa])&dados.Saida.isin([np.nan])]
            if df_mask.empty is True:
                messagebox.showwarning("ERRO", "Identificação não está sendo utilizada")
                return()
            else:
                dados.at[df_mask.index.item(),'Saida']=saida
                dados.at[df_mask.index.item(),'NF']=nf           
                gravador = pd.ExcelWriter(diretorio,engine='xlsxwriter')
                dados.to_excel(gravador, index=False,sheet_name='Entrada')
                gravador.save()
                gravador.close()                
                messagebox.showinfo("SUCESSO", "Cadastro Saida Realizado com Sucesso")
                self.limpar_saida()
                
        
    def limpar_entrada(self):
        self.placa_get.delete(0,'end')
        self.nome_get.delete(0,'end')
        self.transportador_get.delete(0,'end')
        self.observacao_get.delete(0,'end')
    def limpar_saida(self):
        self.placa_get.delete(0,'end')
        self.nf_get.delete(0,'end')
    def cancelar_registro(self):
        self.frame_2.destroy()
        
    def listar_dados(self):
        filtro_escolhido=self.option_filtro.get()
        filtro=self.filtro_get.get()
        if filtro_escolhido=="Nenhum":#imprime tudo
            self.listacli.delete(*self.listacli.get_children())
            contacts = []        
            resultado=dados
            for n in range(len(dados)):
                contacts.append((resultado.Placa[n],resultado.Motorista[n],resultado.Entrada[n],resultado.Saida[n],resultado.NF[n]))
                
            for i in range(len(dados)):
                self.listacli.insert("",tk.END,values=contacts[i])
                
        if filtro_escolhido=="Placa":#imprime so as placas iguais
            self.listacli.delete(*self.listacli.get_children())
            contacts = []
            resultado=dados[dados.Placa.isin([filtro])]
            for n in range(len(resultado)):
                contacts.append((resultado.Placa[n],resultado.Motorista[n],resultado.Entrada[n],resultado.Saida[n],resultado.NF[n]))
                
            for i in range(len(resultado)):
                self.listacli.insert("",tk.END,values=contacts[i])
            
            
        if filtro_escolhido=="Nome":#filtra o nome recebido
            self.listacli.delete(*self.listacli.get_children())
            contacts = []
            resultado=dados[dados.Motorista.isin([filtro])]
            for n in range(len(resultado)):
                contacts.append((resultado.Placa[n],resultado.Motorista[n],resultado.Entrada[n],resultado.Saida[n],resultado.NF[n]))
                
            for i in range(len(resultado)):
                self.listacli.insert("",tk.END,values=contacts[i])
            
            
            
        if filtro_escolhido=="NF":#filtra a NF recebida
            self.listacli.delete(*self.listacli.get_children())
            contacts = []
            resultado=dados[dados.NF.isin([filtro])]
            for n in range(len(resultado)):
                contacts.append((resultado.Placa[n],resultado.Motorista[n],resultado.Entrada[n],resultado.Saida[n],resultado.NF[n]))
                
            for i in range(len(resultado)):
                self.listacli.insert("",tk.END,values=contacts[i])
            
                       

        
            
            
            
class Application(funcoes): #lembrar sempre de informar para a classe x que eu vou usar as funcoes da classe y
    def __init__(self):
        #definindo as variaveis globais usadas no sistema
        self.tipos_veiculos=['Motocicleta','Carro','Caminhonete','Muck','Onibus','Caminhão',
                     'Carreta','Van']
        self.tipos_material=['Materia Prima','Funcionários','Terceiro','Pó Balão',
                        'Alimentos','Sucata','Almoxarifado','Gusa']
        self.tipos_filtros=['Nenhum','Placa','Nome','NF']
        
        #iniciando o aplicativo 
        self.root=root
        self.tela()
        self.frame1()
        self.frame2()
        self.Widgets_Frame1()
        root.mainloop()
        
    def tela(self): # configurações da tela principal
        self.root.title('Cadastro')
        self.root.configure(background='#ADD8E6') 
        self.root.geometry('600x500') #tamanho em pixel largura x comprimento
        self.root.resizable(True,True)#permitir ou não aumentar ou diminuir
        self.root.maxsize(width=700,height=600) #atribuir tamanho maximo da tela
        self.root.minsize(width=500,height=400)
    def frame1(self):
        #definindo o frame1
        self.frame_1=tk.Frame(self.root,bd=4,bg='#DCDCDC',
                              highlightbackground='#C0C0C0',highlightthickness=1) #criando o frame 1, onde vou adicionar os dados
        self.frame_1.place(relx=0.02,rely=0.02,relwidth=0.96,relheight=0.1) #o rel aceita de 0 a 1, se usar 0.1 = 10% 
        
    def frame2(self):
        #definindo o frame2
        self.frame_2=tk.Frame(self.root,bd=4,bg='#DCDCDC',
                              highlightbackground='#C0C0C0',highlightthickness=1) #criando o frame 2, onde vou adicionar os dados
        self.frame_2.place(relx=0.02,rely=0.13,relwidth=0.96,relheight=0.85) #o rel aceita de 0 a 1, se usar 0.1 = 10% 
        
            
    def Widgets_Frame1(self):
        #botao entrada
        self.bt_entrada=tk.Button(self.frame_1,text='ENTRADA',command=self.widgets_entrada)
        self.bt_entrada.place(relx=0.05,rely=0.08, relwidth=0.14,relheight=0.90)
        #botao saida
        self.bt_saida=tk.Button(self.frame_1,text='SAIDA',command=self.widgets_saida)
        self.bt_saida.place(relx=0.2,rely=0.08, relwidth=0.14,relheight=0.90)
        #botao Lista
        self.bt_lista=tk.Button(self.frame_1,text='Lista',command=self.lista_entrada)
        self.bt_lista.place(relx=0.35,rely=0.08, relwidth=0.14,relheight=0.90)
        
        
    def widgets_entrada(self):
        #destruindo os widgets
        self.limpar_frame2()        
        #criando lavel placa
        self.lb_placa=tk.Label(self.frame_2,text='PLACA:',bg='#DCDCDC',anchor='w',font=('verdana',12,'bold'))
        self.lb_placa.place(relx=0,rely=0, relwidth=0.15,relheight=0.10)
        #criando o input da Placa
        self.placa_get=tk.Entry(self.frame_2,font=('verdana',12))
        self.placa_get.place(relx=0,rely=0.10, relwidth=0.15,relheight=0.06)
        #criando a label de entrada de nome
        self.lb_nome=tk.Label(self.frame_2,text='NOME:',bg='#DCDCDC',anchor='w',font=('verdana',12,'bold'))
        self.lb_nome.place(relx=0,rely=0.16, relwidth=0.15,relheight=0.10)
        #criando o input da Nome
        self.nome_get=tk.Entry(self.frame_2,font=('verdana',12))
        self.nome_get.place(relx=0,rely=0.26, relwidth=0.5,relheight=0.06)
        #criando a label de entrada de Transportador
        self.lb_transportador=tk.Label(self.frame_2,text='Transportador:',bg='#DCDCDC',anchor='w',font=('verdana',12,'bold')) #lembrete para justificar de um lado usar o comando anchor e = direta w= esquerda
        self.lb_transportador.place(relx=0, rely=0.32, relwidth=0.5,relheight=0.1)
        #criando o input do Transportador
        self.transportador_get=tk.Entry(self.frame_2,font=('verdana',12))
        self.transportador_get.place(relx=0,rely=0.4, relwidth=0.5,relheight=0.06)        
        #criando a label de entrada de Tipo Veiculo
        self.lb_veiculo=tk.Label(self.frame_2,text='MODELO:',bg='#DCDCDC',anchor='w',font=('verdana',12,'bold'))
        self.lb_veiculo.place(relx=0.2,rely=0.0, relwidth=0.15,relheight=0.1)
        #criando o input da Veiculo   
        
        self.option_veiculo=tk.StringVar()
        self.veiculo_get=ttk.OptionMenu(self.frame_2,
                                       self.option_veiculo,self.tipos_veiculos[0],*self.tipos_veiculos,)
        self.veiculo_get.place(relx=0.2,rely=0.1, relwidth=0.2,relheight=0.06)    
        #criando a label de entrada de Tipo Carga
        self.lb_carga=tk.Label(self.frame_2,text='CARGA:',bg='#DCDCDC',anchor='w',font=('verdana',12,'bold'))
        self.lb_carga.place(relx=0.5,rely=0.0, relwidth=0.15,relheight=0.1)
        #criando o input da Carga
        #manipulando o option menu para retornar em uma variavel o valor clicado
        #importante lembrar para retornar a opção de uma widget do tipo OptionMenu
        self.option_carga=tk.StringVar()
        self.carga_get=ttk.OptionMenu(self.frame_2,
                                       self.option_carga,self.tipos_material[0],*self.tipos_material)
        self.carga_get.place(relx=0.5,rely=0.1, relwidth=0.2,relheight=0.06)
        #criando a label de entrada de Observação
        self.lb_observacao=tk.Label(self.frame_2,text='Observacao:',bg='#DCDCDC',anchor='w',font=('verdana',12,'bold')) #lembrete para justificar de um lado usar o comando anchor e = direta w= esquerda
        self.lb_observacao.place(relx=0, rely=0.46, relwidth=0.5,relheight=0.1)
        #criando o input do Observação
        self.observacao_get=tk.Entry(self.frame_2,font=('verdana',12))
        self.observacao_get.place(relx=0, rely=0.56, relwidth=0.5,relheight=0.06)         
        #botao cadastro
        self.bt_cadastrar=tk.Button(self.frame_2,text='CADASTRAR',command=self.registrar_entrada,bg="#58D68D",bd=4,fg='black',font=('verdana',11,'bold'))
        self.bt_cadastrar.place(relx=0,rely=0.65, relwidth=0.2,relheight=0.1)
        #botao limpar
        self.bt_limpar=tk.Button(self.frame_2,text='LIMPAR',command=self.limpar_entrada,bg="#F4D03F",bd=4,fg='black',font=('verdana',11,'bold'))
        self.bt_limpar.place(relx=0.2,rely=0.65, relwidth=0.2,relheight=0.1)
        #botao cancelar
        self.bt_cancelar=tk.Button(self.frame_2,text='CANCELAR',command=self.limpar_frame2,bg="#EC7063",bd=4,fg='black',font=('verdana',11,'bold'))
        self.bt_cancelar.place(relx=0.4,rely=0.65, relwidth=0.2,relheight=0.1)
    def widgets_saida(self):
        #destruindo os widgets
        self.limpar_frame2()  
        #criando label placa
        self.lb_placa=tk.Label(self.frame_2,text='PLACA:',bg='#DCDCDC',anchor='w',font=('verdana',12,'bold'))
        self.lb_placa.place(relx=0,rely=0, relwidth=0.15,relheight=0.10)
        #criando o input da Placa
        self.placa_get=tk.Entry(self.frame_2,font=('verdana',12))
        self.placa_get.place(relx=0,rely=0.10, relwidth=0.15,relheight=0.06)
        #criando label NF
        self.lb_nf=tk.Label(self.frame_2,text='NF:',bg='#DCDCDC',anchor='w',font=('verdana',12,'bold'))
        self.lb_nf.place(relx=0.2,rely=0, relwidth=0.15,relheight=0.10)
        #criando o input da NF
        self.nf_get=tk.Entry(self.frame_2,font=('verdana',12))
        self.nf_get.place(relx=0.2,rely=0.10, relwidth=0.2,relheight=0.06)
        #botao cadastro
        self.bt_cadastrar=tk.Button(self.frame_2,text='CADASTRAR',command=self.registrar_saida,bg="#58D68D",bd=4,fg='black',font=('verdana',11,'bold'))
        self.bt_cadastrar.place(relx=0,rely=0.65, relwidth=0.2,relheight=0.1)
        #botao limpar
        self.bt_limpar=tk.Button(self.frame_2,text='LIMPAR',command=self.limpar_saida,bg="#F4D03F",bd=4,fg='black',font=('verdana',11,'bold'))
        self.bt_limpar.place(relx=0.2,rely=0.65, relwidth=0.2,relheight=0.1)
        #botao cancelar
        self.bt_cancelar=tk.Button(self.frame_2,text='CANCELAR',command=self.limpar_frame2,bg="#EC7063",bd=4,fg='black',font=('verdana',11,'bold'))
        self.bt_cancelar.place(relx=0.4,rely=0.65, relwidth=0.2,relheight=0.1)
        
    

    def lista_entrada(self):
        #destruindo os widgets
        self.limpar_frame2()     
        #setando o tipo de filtro que vou querer aplicar no registro
        #criando a label de filtro
        self.lb_listafiltro=tk.Label(self.frame_2,text='FILTRO:',bg='#DCDCDC',anchor='w',font=('verdana',12,'bold'))
        self.lb_listafiltro.place(relx=0,rely=0.0, relwidth=0.15,relheight=0.1)
        #criando o input da Veiculo        
        self.option_filtro=tk.StringVar()
        self.filtro_menu=ttk.OptionMenu(self.frame_2,
                                       self.option_filtro,self.tipos_filtros[0],*self.tipos_filtros)
        self.filtro_menu.place(relx=0.16,rely=0.02, relwidth=0.2,relheight=0.06)    
        #criando o input do Filtro
        self.filtro_get=tk.Entry(self.frame_2,font=('verdana',12))
        self.filtro_get.place(relx=0.37, rely=0.02, relwidth=0.2,relheight=0.06) 
        # #botao filtrar
        # self.bt_filtrar=tk.Button(self.frame_2,text='FILTRAR',command=self.listar_dados,bg="#58D68D",bd=4,fg='black',font=('verdana',11,'bold'))
        # self.bt_filtrar.place(relx=0.58,rely=0, relwidth=0.15,relheight=0.1)
        #botao listar
        self.bt_listar=tk.Button(self.frame_2,text='Listar',command=self.listar_dados,bg="#58D68D",bd=4,fg='black',font=('verdana',11,'bold'))
        self.bt_listar.place(relx=0.58,rely=0, relwidth=0.15,relheight=0.1)


        
        
        #definindo as variaveis ( colunas que vou apresentar)
        self.listacli=ttk.Treeview(self.frame_2,height=3,column=('Col1','Col2','Col3','Col4','Col5'))
        #definindo o nome das colunas
        self.listacli.heading("#0", text="ID")
        self.listacli.heading("#1", text="Placa")
        self.listacli.heading("#2", text="Nome")
        self.listacli.heading("#3", text="Data Entrada")
        self.listacli.heading("#4", text="Data Saida")
        self.listacli.heading("#5", text="NF")
        #definindo o tamanho das colunas
        self.listacli.column("#0", width=1)
        self.listacli.column("#1", width=50)
        self.listacli.column("#2", width=100)
        self.listacli.column("#3", width=100)
        self.listacli.column("#4", width=100)
        self.listacli.column("#5", width=100)
        #definindo a posição da lista
        self.listacli.place(relx=0.01,rely=0.2,relwidth=0.95,relheigh=0.8)
        #agora criando a barra de rolagem
        self.barra_rolagem=tk.Scrollbar(self.frame_2,orient='vertical')
        #agora configurar a barra de rolagem para o listacli ( a lista que criei)
        self.listacli.configure(yscroll=self.barra_rolagem.set)
        self.barra_rolagem.place(relx=0.965,rely=0.2,relwidth=0.03,relheigh=0.8)
        

Application()




