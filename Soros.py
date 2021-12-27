from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
from colorama import init, Fore, Back
from time import sleep
import sys
import os, stdiomask
import json
import time
from colorama import *
from os import system
import random, ctypes

ctypes.windll.kernel32.SetConsoleTitleW("BOT FLIP COIN SOROS : Tente sua sorte CARA OU COROA????")
system('cls')

print(f'''       	Conecte-se ao Brooker(IQ OPTION)    	\n''')

print(f'''       [-] Digite seu Email   	''')
login= str(input('Email: '))

print(f'''       [-] Digite sua Senha    	''')
senha= stdiomask.getpass()

API = IQ_Option(login, senha)
API.connect()
system('cls')

if API.check_connect():
	print(' Conectado com sucesso!\n')
else:
	print(' Erro ao conectar, EMAIL ou Senha incorretos.')
	sys.exit()

def Payout(par, tipo, timeframe = 1):
    if tipo == 'turbo':
        a = API.get_all_profit()
        return int(100 * a[par]['turbo'])
        
    if tipo == 'digital':
    
        dg = API.get_digital_payout(par)
        return dg

def Ver_Payout():
    par = API.get_all_open_time()
    for paridade in par['digital']:
        if par['digital'][paridade]['open'] == True:
            print('[ DIGITAL ]: '+paridade+' | Payout: '+str( Payout(paridade, 'digital')) + '%' )

while True:
	try:
		API.change_balance = int(input('\n Realizar Operacoes em::\n  1 - Conta Demo\n  2 - Conta REAL\n  :: '))
		
		if API.change_balance > 0 and API.change_balance < 3 : break
	except:
		print('\n Opção invalida')

system('cls')
verHora = API.get_server_timestamp()
print(f'''       	- Analisando Paridades Abertas     \n''')   
Ver_Payout()

banca = int(API.get_balance())
op = []
cifrao = 'R$'
soros_lucro = 0.0
soros_porcentagem = round(100 / 100, 2)
soros_atual = 0
lucro_total = 0
lucro = 0
soros_niveis = 1
entrada_base = 10
pares_bin = str(input('\nDigite a paridade a Operar\n:: ')).upper()
system('cls')

while True:
	top_face = random.randint(0, 1)
	if top_face == 0:
		face = 'Cara'
		dir = 'call'
	else:
		face = 'Coroa'
		dir = 'put'
	
	entrada = float(entrada_base)
	if soros_lucro > 0.0:
		if soros_atual <= soros_niveis:
			entrada = round(entrada_base + (soros_lucro * soros_porcentagem), 2)
		else:
			soros_lucro = 0.0
			soros_atual = 0

	status,id = API.buy_digital_spot(pares_bin, entrada, dir, 1)
	if status:
		print(f'''\n       - Aguardando Resultado...:  {(face, dir.upper())} ''')    
		status = False
		
		while status == False:
			status, valor = API.check_win_digital_v2(id)
		
		if status:
			valor = round(valor, 2)
			    
			print('\n################ Resultado da Operacao: ################\n  ')

			if valor > 0:
				soros_lucro = valor
				soros_atual += 1
				resultado = 'Win'
				op.append(resultado)
				print(f'''       - GAIN		  : [\x1b[32m{cifrao}{round(valor, 2)}\x1b[0m]''')
				
		
			elif valor < 0:
				soros_lucro = 0.0
				soros_atual = 0
				resultado = 'Loss'
				op.append(resultado)
				print(f'''       - LOSS		   : [\x1b[91m{cifrao}{round(valor, 2)}\x1b[0m]''')
				
			else:
				print('Empate')		

			wins = op.count('Win')
			losses = op.count('Loss')
			lucro_total += valor
			assertividade = (wins / (wins + losses)) * 100
			print(f'''       - Saldo Liquido	   : [{cifrao}{round(lucro_total, 2)}]''')
			print(f'''       - Quantidade de WIN : [\x1b[32m{wins}\x1b[0m]''')
			print(f'''       - Quantidade de LOSS: [\x1b[91m{losses}\x1b[0m]''')
			print(f'''       - ASSERTIVIDADE     : [ {int(assertividade)} %]''')
			print(f'''       - SOROS NIVEL   	   : [ {(soros_atual)} ]''')
			print('\n')	
			
			 
							
