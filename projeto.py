#Biblioteca de data e hora
from datetime import datetime

#Arquivos para leitura
arquivo_clientes =  open("Clientes.txt" ,"r")
arquivo_extrato =  open("Extrato.txt" ,"r")
      
#Função para criar novos clientes.
def novo_cliente():
    
    #Abre arquivo para leitura 
    with open('Clientes.txt', 'r') as arquivo:
        #Separa a string em cada linha no caractere ","
        clientes = [line.strip().split(',') for line in arquivo]

    print('Criar novo cliente: ')
    print()

    lista_clientes = []
    cpf = str(input("CPF: "))

    #Valida o cpf quando for fazer a criação
    if len(cpf) != 14 or cpf[3] != '.' or cpf[7] != '.' or cpf[11] != '-':
        print()
        print('CPF invalido!')
        return

    #Verificar se o cliente ja é existente
    for x in range(len(clientes)):
        if cpf in clientes[x]:
            print()
            print("Cliente ja existente!")
            return
                    
    #Cria as informações do cliente
    nome = str(input("Nome: ")) 
    tipo_de_conta =  str(input("Tipo de conta (1-Comum , 2-Plus): "))
    #Verifica o tipo de conta
    if tipo_de_conta == '1':
        tipo_de_conta = "Comum"
    elif tipo_de_conta == "2":
        tipo_de_conta = "Plus"
    else:
        print()
        print('Tipo de conta invalido')
        return
    valor_inicial = str(input("Valor inicial: "))
    senha = str(input("Digite a senha: "))
    
    #Verifica se a senha é valida de 4 digitos e somente numeros
    for i in senha:
        valor_ascii = ord(i)
        if valor_ascii < 48 or valor_ascii > 57 or len(senha) != 4:
            print()
            print("Senha invalida")
            return
    
    #Salva as informações em uma lista        
    lista_clientes.append(cpf)
    lista_clientes.append(nome)
    lista_clientes.append(tipo_de_conta)
    lista_clientes.append(valor_inicial)
    lista_clientes.append(senha)
    
    #Abre o arquivo para adicionar informações
    arquivo_clientes = open("Clientes.txt" , 'a')
     #Adiciona o cliente no arquivo
    arquivo_clientes.write(','.join(lista_clientes) + '\n')

    print()
    print("Cliente criado!")
    print()
    
    
    

    
#Função para excluir clientes.
def excluirCliente():
    
    #Abre arquivo para leitura
    with open('Clientes.txt', 'r') as arquivo:
        #Separa a string em cada linha no caractere ","
        clientes = [line.strip().split(',') for line in arquivo]
    
    print("Excluir Cliente!")

    cpf = str(input("Digite o CPF: "))
    
    #Verifica se a digitação do cpf esta correta
    if len(cpf) != 14 or cpf[3] != '.' or cpf[7] != '.' or cpf[11] != '-':
        print()
        print('CPF invalido!')
        return
    
    #Verifica se o cliente existe
    for x in range(len(clientes)):
        if cpf in clientes[x]:
            #Remove o cliente
            clientes.remove(clientes[x])
            print()
            print("Cliente removido!")
            print()
            
            #Faz alteração do arquivo reescrevendo a lista de clientes sem o cliente removido    
            with open('Clientes.txt', 'w') as arquivo:
                for c in clientes:
                    arquivo.write(','.join(str(item) for item in c) + '\n')
            return
    print()
    print("Inexistente")

    
#Função para listar os clientes.
def listar_cliente():
    
    #Abre arquivo para leitura
    with open('Clientes.txt', 'r') as arquivo:
        clientes = arquivo.readlines()

    print('Lista de Clientes:')
    print()

    # Lista todos os clientes existentes
    for x in clientes:
        campos = x.split(',')
        tipos = ['CPF: ', 'Nome: ', 'Tipo: ', 'Saldo: ', 'Senha: ']
        for tipo, campo in zip(tipos, campos):
            print(tipo, campo.strip())
        print("\n")
    print()     

#Função para debitos.
def debito():
    
    #Abre arquivo para leitura
    with open('Clientes.txt', 'r') as arquivo:
        #Separa a string em cada linha no caractere ","
        clientes = [line.strip().split(',') for line in arquivo]
    
    lista_extrato = []
    
    #Variaveis de data e hora
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
    
    print("Debitos!")
    
    cpf = input("Digite o CPF: ")
    senha = input("Digite a senha: ")

    #Verifica se o cliente existe
    for x in range(len(clientes)):
        if cpf in clientes[x] and senha in clientes[x]:
            valor = float(input("Valor para Débito: "))
            
            #Verifica se a conta é Comum e tem saldo
            if clientes[x][2] == 'Comum' and float(clientes[x][3]) - valor < -1000:
                print()
                print('Saldo insuficiente')
                return

            #verifica se a conta é Plus e tem saldo
            elif clientes[x][2] == 'Plus' and float(clientes[x][3]) - valor < -5000:
                print()
                print('Saldo insuficiente')
                return

            else:
                #Debito para conta comum
                if clientes[x][2] == 'Comum':
                    #Tarifa de 5%
                    tarifa = valor * 0.05
                    #Debita na conta do cliente
                    clientes[x][3] = float(clientes[x][3]) - valor - tarifa 
                    #Cria o extrato
                    lista_extrato.append("Data: %s       - %.2f    Tarifa: %.2f   Saldo = %.2f _ %s" % (data_e_hora_em_texto,valor,tarifa,clientes[x][int(3)],cpf))
                    
                    #Faz alteração do arquivo reescrevendo a lista de clientes com o saldo alterado
                    with open('Clientes.txt', 'w') as arquivo:
                        for c in clientes:
                            arquivo.write(','.join(str(item) for item in c) + '\n')
                    
                    #Adiciona o extrato no arquivo
                    with open('Extrato.txt', 'a') as arquivo_extrato:
                        arquivo_extrato.write(','.join(lista_extrato) + '\n')
                        
                
                #Debito para conta Plus
                else:
                    #Tarifa de 3%
                    tarifa = valor * 0.03
                    #Debita na conta do cliente
                    clientes[x][3] = float(clientes[x][3]) - valor - tarifa
                    #Cria o extrato
                    lista_extrato.append("Data: %s       - %.2f    Tarifa: %.2f   Saldo = %.2f _ %s" % (data_e_hora_em_texto,valor,tarifa,clientes[x][int(3)],cpf))
                    
                    #Faz alteração do arquivo reescrevendo a lista de clientes com o saldo alterado
                    with open('Clientes.txt', 'w') as arquivo:
                        for c in clientes:
                            arquivo.write(','.join(str(item) for item in c) + '\n')

                    #Adiciona o extrato no arquivo
                    with open('Extrato.txt', 'a') as arquivo_extrato:
                        arquivo_extrato.write(','.join(lista_extrato) + '\n')

            
            print()
            print('Valor debitado!')
            print()
            return

    print()
    print("CPF ou senha invalida!")
    print()


#Função para depositos.
def deposito():
    #Abre o arquivo para leitura
    with open('Clientes.txt', 'r') as arquivo:
        #Separa a string em cada linha no caractere ","
        clientes = [line.strip().split(',') for line in arquivo]
    
    lista_extrato = []
    
    #Data e hora atual
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')

    print("Deposito!")
    
    cpf = str(input("Digite o CPF: "))
    
    #Verifica se o cliente existe
    for x in range(len(clientes)):
        if cpf in clientes[x]:
            valor = float(input("Valor para Deposito: "))
            
            #Deposita na conta do cliente
            clientes[x][3] = float(clientes[x][3]) + valor
            #Cria o extrato
            lista_extrato.append("Data: %s       + %.2f    Tarifa: 0.00   Saldo = %.2f _ %s" % (data_e_hora_em_texto,valor,clientes[x][int(3)],cpf))

            #Faz alteração do arquivo reescrevendo a lista de clientes com o saldo alterado
            with open('Clientes.txt', 'w') as arquivo:
                for c in clientes:
                    arquivo.write(','.join(str(item) for item in c) + '\n')
            
            #Adiciona o extrato no arquivo       
            with open('Extrato.txt', 'a') as arquivo_extrato:
                arquivo_extrato.write(','.join(lista_extrato) + '\n')

            print()
            print('Valor depositado!')
            print()
            return
    print()   
    print("CPF invalido!")
    print()
    



#Função para extratos.   
def extratos():
    
    #Abre arquivo de clientes para leitura
    with open('Clientes.txt', 'r') as arquivo:
        #Separa a string em cada linha no caractere ","
        clientes = [line.strip().split(',') for line in arquivo]
    
    #Abre arquivo de extratos para leitura    
    with open('Extrato.txt' , 'r') as arquivo_extrato:
        extrato = [line.strip().split('_') for line in arquivo_extrato]
    
    cpf = input('Digite o CPF: ')
    senha = input('Digite a senha: ')

    #Verifica se o cliente existe
    for x in range(len(clientes)):
        if cpf in clientes[x] and senha in clientes[x]:
            #Printa informações do cliente
            print()
            print('Extratos: ')
            print()
            print("Nome: " , clientes[x][1])
            print("CPF: ",clientes[x][0])
            print("Tipo: " ,clientes[x][2])
            print()
            #Verifica o cpf do cliente na lista extratos e tras extratos do cpf digitado
            for a in extrato:
                if cpf in a[1]:
                    print(a[0])
                        
            return

            
    print()
    print("CPF ou senha invalida!")
    print()

                
				
#Função para transferencias.
def transferencia():
    
    #Abre o arquivo para leitura
    with open('Clientes.txt', 'r') as arquivo:
        #Separa a string em cada linha no caractere ","
        clientes = [line.strip().split(',') for line in arquivo]
    
    lista_extrato = []
    #Variaveis de data e hora atual
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y %H:%M')
    
    print("Área de tranferencia!")
    print()

    cpf_origem = str(input("Digite o CPF de origem: "))
    senha_origem = str(input("Digite a senha: "))
    
    #Verifica se o cliente de origem existe
    for x in range(len(clientes)):
        if cpf_origem in clientes[x] and senha_origem in clientes[x]:
            valor =  float(input("Digite o valor: "))
            
            #Verifica se a conta é Comum e tem saldo
            if clientes[x][2] == 'Comum' and float(clientes[x][3]) - valor < -1000:
                print()
                print('Saldo insuficiente')
                return

            #verifica se a conta é Plus e tem saldo
            elif clientes[x][2] == 'Plus' and float(clientes[x][3]) - valor < -5000:
                print()
                print('Saldo insuficiente')
                return

            else:
                cpf_destino =  str(input("Digite o CPF de destino: "))
                #Verifica se o cpf de destino existe
                for x in range(len(clientes)):
                    if cpf_destino in clientes[x]:
                        
                        for x in range(len(clientes)):
                            if cpf_origem in clientes[x] and senha_origem in clientes[x]:
                                #Retira da conta origem
                                clientes[x][3] = float(clientes[x][3]) - valor
                                #Cria extrato
                                lista_extrato.append("Data: %s       - %.2f    Tarifa: 0.00   Saldo = %.2f _ %s" % (data_e_hora_em_texto,valor,clientes[x][int(3)],cpf_origem))
                                
                                #Faz alteração do arquivo reescrevendo a lista de clientes com o saldo alterado
                                with open('Clientes.txt', 'w') as arquivo:
                                    for c in clientes:
                                        arquivo.write(','.join(str(item) for item in c) + '\n')
                                        
                        for x in range(len(clientes)):
                            if cpf_destino in clientes[x]:
                                #Adiciona o valor ao cliente destino
                                clientes[x][3] = float(clientes[x][3]) + valor
                                #Cria extrato
                                lista_extrato.append("Data: %s       + %.2f    Tarifa: 0.00   Saldo = %.2f _ %s" % (data_e_hora_em_texto,valor,clientes[x][int(3)],cpf_destino))
                                
                                #Faz alteração do arquivo reescrevendo a lista de clientes com o saldo alterado
                                with open('Clientes.txt', 'w') as arquivo:
                                    for c in clientes:
                                        arquivo.write(','.join(str(item) for item in c) + '\n')
                                
                                #Adiciona o extrato no arquivo        
                                with open('Extrato.txt', 'a') as arquivo_extrato:
                                    arquivo_extrato.write('\n'.join(lista_extrato) + '\n')

                                print()
                                print('Transferencia concluida!')
                                print()
                                return
                
                print()
                print('CPF de destino invalido!')
                return
    
    print()
    print("CPF ou senha de origem invalida!")
    print()


#Função para debitos automaticos.
def recarga():

    #abre o arquivo para leitura
    with open('Clientes.txt', 'r') as arquivo:
        #Separa a string em cada linha no caractere ","
        clientes = [line.strip().split(',') for line in arquivo]
    
    lista_extrato = []
    #Variaveis de data e hora atual
    data_atual = datetime.now()
    data_atual = data_atual.strftime('%d/%m/%Y %H:%M')
    
    print('Recarga')
    print()
    
    cpf = str(input("Digite o CPF: "))
    senha = str(input("Digite a senha: "))
    
    #Verifica se o cliente existe
    for x in range(len(clientes)):
        if cpf in clientes[x] and senha in clientes[x]:
            print()
            numero = input("Digite o numero: ")
            
            #Verifica a operadora
            operadora = input("OPERADORA - 1-VIVO , 2-TIM , 3-CLARO: ")
            if operadora == '1':
                operadora = "VIVO"   
            elif operadora == 'TIM':
                operadora = "2"  
            elif operadora == '3':
                operadora = "CLARO"
            else:
                print()
                print('Operadora Invalida!')
                return
            
            
            valor = float(input("Digite o Valor da recarga: "))
            
             #Verifica se a conta é Comum e tem saldo
            if clientes[x][2] == 'Comum' and float(clientes[x][3]) - valor < -1000:
                print()
                print('Saldo insuficiente')
                return

            #verifica se a conta é Plus e tem saldo
            elif clientes[x][2] == 'Plus' and float(clientes[x][3]) - valor < -5000:
                print()
                print('Saldo insuficiente')
                return

            else:
                
                print()
                #Mostra a operação
                print("Data: %s  - %s - %s - %.2f" % (data_atual,numero,operadora,valor))

                print()
                print("Recarga Realizada!")
                print()

                #Debita o valor da conta do cliente
                clientes[x][3] = float(clientes[x][3]) - valor

                #Cria extrato
                lista_extrato.append("Data: %s       - %.2f    Tarifa: 0.00   Saldo = %.2f _ %s" % (data_atual,valor,clientes[x][int(3)],cpf))
                    
                #Faz alteração do arquivo reescrevendo a lista de clientes com o saldo alterado
                with open('Clientes.txt', 'w') as arquivo:
                    for c in clientes:
                        arquivo.write(','.join(str(item) for item in c) + '\n')
                    
                #Adiciona o extrato no arquivo    
                with open('Extrato.txt', 'a') as arquivo_extrato:
                    arquivo_extrato.write(','.join(lista_extrato) + '\n')
                
                return       
                

    print()
    print("CPF ou senha invalida!")
    print()

#Laço de repetição infinito.
while True:

    print()
    print("1. Novo cliente")
    print("2. Apaga cliente")
    print("3. Listar clientes")
    print("4. Débito")
    print("5. Depósito")
    print("6. Extrato")
    print("7. Transferência entre contas")
    print("8. Recargas")
    print("9. Sair")
    print()

    opcao =(input("Digite a operação: "))
    print()

    #Condição para sair .
    if opcao == "9":
        print("Encerrado!")
        print()
        break
    
    #Condição para criar cliente
    elif opcao == "1":
        novo_cliente()

    #Condição para excluir cliente
    elif opcao == "2":
        excluirCliente()
    
    #Condição para listar clientes
    elif opcao == "3":
        listar_cliente()
    
    #Condição para debitos
    elif opcao == "4":
        debito()
    
    #Condição para depositos
    elif opcao == "5":
        deposito()

    #Condição para extratos
    elif opcao == '6':
        extratos()
    
    #Condição para transferencias
    elif opcao == '7':
        transferencia()
    
    #Condição para recargas
    elif opcao == '8':
       recarga()
    
    #Condição para operação invalida 
    else:
        print("Opção invalida!")


#Fecha os arquivos
arquivo_clientes.close()
arquivo_extrato.close()
