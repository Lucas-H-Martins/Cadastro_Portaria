# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 09:08:14 2022

@author: TI
"""

import tkinter as tk
from tkinter import ttk
import datetime as dt
import pandas as pd
from tkinter import messagebox
import numpy as np

lista_tipos=['Motocicleta','Carro','Caminhonete','Muck','Onibus','Caminhão',
             'Carreta','Van']
lista_material=['Materia Prima','Funcionários','Terceiro','Pó Balão',
                'Alimentos','Sucata','Almoxarifado','Gusa']

diretorio='T:\PORTARIA\Controle Veiculos\portaria.xlsx'
dados=pd.read_excel(diretorio)

dados.columns=['Placa','Modelo','Entrada','Saida','Motorista','Carga','Transportador','NF','Observacao']
dados.Saida=dados.Saida.astype(object)
# gravador = pd.ExcelWriter('portaria.xlsx',engine='xlsxwriter')
# dados.to_excel(gravador, index=False,sheet_name='Entrada')

# gravador.save()
# gravador.close()




def inserir_entrada():
    
    # ident=ident_get.get()    
    placa=placa_get.get()    
    modelo=combobox_modelo.get()    
    motorista=motorista_get.get()    
    carga=combobox_carga.get()    
    transportador=transportador_get.get()    
    nf=np.nan 
    observacao=observacao_get.get()    
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
            placa_get.delete(0,'end')
            motorista_get.delete(0,'end')
            transportador_get.delete(0,'end')
            observacao_get.delete(0,'end')
            gravador = pd.ExcelWriter(diretorio,engine='xlsxwriter')
            dados.to_excel(gravador, index=False,sheet_name='Entrada')            
            gravador.save()
            gravador.close()


            messagebox.showinfo("SUCESSO", "Cadastro Entrada Realizado")
            
            
            
        else:
            messagebox.showwarning("ERRO", "Identificação sendo usada")
            return()
        


def registrar_saida():
    placa=placa_saida_get.get()
    nf=nf_get.get()
    saida=dt.datetime.now()    
    saida=saida.strftime("%d/%m/%Y %H:%M")
    
    if placa=="":
        messagebox.showwarning("ERRO", "Placa não pode ser vazio")
        return()

    if nf =="":
        messagebox.showwarning("ERRO", "NF não pode ser vazio")
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
            placa_saida_get.delete(0,'end')
            nf_get.delete(0,'end')
            messagebox.showinfo("SUCESSO", "Cadastro Saida Realizado")
            
            
        
           
janela=tk.Tk()

# janela.iconbitmap("logo.ico")

janela.geometry("500x320")
janela.resizable(False, False)
   
    
    
janela.title('Entrada Veiculos Ferguminas')

#cabecalhos

label_entrada=tk.Label(text="ENTRADA VEICULOS")
label_entrada.grid(row=0,column=2,padx=10, sticky='nswe',columnspan=2)

label_entrada=tk.Label(text="SAIDA VEICULOS")
label_entrada.grid(row=0,column=6,padx=10, sticky='nswe',columnspan=2)

#PLACA
label_placa=tk.Label(text="Placa:")
label_placa.grid(row=1,column=0,padx=10, sticky='nswe',columnspan=2)
placa_get =  tk.Entry()
placa_get.grid(row=1, column=2,padx = 10, pady=10, sticky='nswe', columnspan =2 )

#modelo
label_modelo = tk.Label(text="Modelo de Veiculo:")
label_modelo.grid(row=2, column=0,padx = 10, pady=10, sticky='nswe', columnspan =2 )
combobox_modelo = ttk.Combobox(values=lista_tipos)
combobox_modelo.grid(row=2, column=2, padx = 10, pady=10, sticky='nswe', columnspan = 2)
combobox_modelo.set(lista_tipos[0])

#motorista
label_motorista=tk.Label(text="Motorista:")
label_motorista.grid(row=3,column=0,padx=10, sticky='nswe',columnspan=2)
motorista_get =  tk.Entry()
motorista_get.grid(row=3, column=2,padx = 10, pady=10, sticky='nswe', columnspan =2 )

#carga
label_carga = tk.Label(text="Tipo de Carga:")
label_carga.grid(row=4, column=0,padx = 10, pady=10, sticky='nswe', columnspan =2 )
combobox_carga = ttk.Combobox(values=lista_material)
combobox_carga.grid(row=4, column=2, padx = 10, pady=10, sticky='nswe', columnspan = 2)
combobox_carga.set(lista_material[0])

#Transportador
label_transportador=tk.Label(text="Transportador:")
label_transportador.grid(row=5,column=0,padx=10, sticky='nswe',columnspan=2)
transportador_get =  tk.Entry()
transportador_get.grid(row=5, column=2,padx = 10, pady=10, sticky='nswe', columnspan =2 )

#Observacao
label_observacao=tk.Label(text="Observacao:")
label_observacao.grid(row=6,column=0,padx=10, sticky='nswe',columnspan=2)
observacao_get =  tk.Entry()
observacao_get.grid(row=6, column=2,padx = 10, pady=10, sticky='nswe', columnspan =2 )

#ID saida
label_placa_saida=tk.Label(text="Placa:")
label_placa_saida.grid(row=1,column=4,padx=10, sticky='nswe',columnspan=2)
placa_saida_get =  tk.Entry()
placa_saida_get.grid(row=1, column=6,padx = 10, pady=10, sticky='nswe', columnspan =2 )

#NF saida
label_nf=tk.Label(text="NF:")
label_nf.grid(row=2,column=4,padx=10, sticky='nswe',columnspan=2)
nf_get =  tk.Entry()
nf_get.grid(row=2, column=6,padx = 10, pady=10, sticky='nswe', columnspan =2 )


#comandos de ação
botao_criar_codigo = tk.Button(text="Cadastrar Entrada", command=inserir_entrada)
botao_criar_codigo.grid(row=9,column=0,padx = 10, pady=10,sticky='nswe', columnspan =4)

botao_saida_codigo = tk.Button(text="Cadastrar Saida", command=registrar_saida)
botao_saida_codigo.grid(row=3,column=4,padx = 10, pady=10,sticky='nswe', columnspan =4)

janela.mainloop()


