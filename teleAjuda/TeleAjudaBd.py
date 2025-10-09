import pandas as pd
import oracledb as orcl

def conectar_BD():
    try:
        # string de conexao para configurar os dados do servidor Oracle
        str_conexao = orcl.makedsn("oracle.fiap.com.br", "1521", "ORCL")
        str_autentic = orcl.connect(user="RM564870", password="170201", dsn=str_conexao)

        inst_SQL = str_autentic.cursor()

    except Exception as erro:
        print(f"Erro: {erro}")
        conexao_BD = False
    else:
        conexao_BD = True

    return conexao_BD, str_autentic, inst_SQL

#==============================================================================================
# INICIO DO PROGRAMA
def main():
    usuario = []
    paciente = []
    conexao_BD, str_autentic, inst_SQL = conectar_BD()
    print("\n" + "=" * 50)
    print("🌐 SISTEMA DE ATENDIMENTO AO USUÁRIO".center(50))
    print("=" * 50)
    print("1️⃣  Já tenho cadastro")
    print("2️⃣  Fazer cadastro")
    opcao = input("Escolha uma oção: ")
    if opcao == "1":
        usuario_localizar = input("\nUsuario: ")
        senha = input("\nSenha: ")
        usuario_localizado = validar_usuario(usuario_localizar, senha, inst_SQL)
        if usuario_localizado:
            usuario.append(usuario_localizado)
            codigo = usuario[0][0]
            paciente_localizado = localizar_paciente(codigo, inst_SQL)
            if paciente_localizado:
                paciente.append(paciente_localizado)
                mostrar_menu_principal(paciente)
            else:
                print("Usuario ou senha incorretos. Tente novamente")
                main()
        else:
            print("Usuario ou senha incorretos. Tente novamente")
            main()

    else:
        cadastrar_usuario(inst_SQL, str_autentic)

#================================================================================================================
# AREA DO USUARIO
# == Validação do Usuario ==
def validar_usuario(usuario, senha, inst_SQL):
    lista_dados = []
    str_consulta = f"SELECT * FROM T_TAJ_LOGIN WHERE USER_LOGIN = '{usuario}' AND SENHA_LOGIN = '{senha}'"
    inst_SQL.execute(str_consulta)
    dados = inst_SQL.fetchall()
    for dado in dados:
        lista_dados.append(dado)
    if len(lista_dados) == 0:
        return False
    else:
        usuario = lista_dados[0]
        return usuario

# == Localizar paciente ==
def localizar_paciente(codigo, inst_SQL):
    lista_dados = []
    str_consulta = f"SELECT * FROM T_TAJ_PACIENTE WHERE T_TAJ_LOGIN_ID_LOGIN = '{codigo}'"
    inst_SQL.execute(str_consulta)
    dados = inst_SQL.fetchall()
    for dado in dados:
        lista_dados.append(dado)
    if len(lista_dados) == 0:
        return False
    else:
        paciente = lista_dados[0]
        return paciente


# == Cadastrar Usuario ==
def cadastrar_usuario(inst_SQL, str_autentic):
    try:
        lista_dados = []
        novo_usuario = input("Digite o usuario: ")

        #== verificando se usuario já existe ==
        str_usuario = f"SELECT * FROM T_TAJ_LOGIN WHERE USER_LOGIN = '{novo_usuario}'"
        inst_SQL.execute(str_usuario)
        dados = inst_SQL.fetchall()
        for dado in dados:
            lista_dados.append(dado)
        while len(lista_dados) != 0:
            lista_dados.remove(lista_dados[0])
            novo_usuario = input("Esse usuario ja existe! Digite outro usuario: ")
            str_usuario = f"SELECT * FROM T_TAJ_LOGIN WHERE USER_LOGIN = '{novo_usuario}'"
            inst_SQL.execute(str_usuario)
            dados = inst_SQL.fetchall()
            for dado in dados:
                lista_dados.append(dado)

        # == inputs dos outros dados ==
        senha = input("Digite sua senha: ")
        cpf = input("Digite seu CPF: ")
        nome = input("Digite seu nome: ")
        tel = input("Digite seu telefone: ")
        mail = input("Digite seu email: ")
        rghc = input("Digite seu RGHC: ")
        datanasc = input("Digite sua data de nascimento: ")
        str_novo_user = f"""INSERT INTO T_TAJ_LOGIN (USER_LOGIN, SENHA_LOGIN, TP_LOGIN) VALUES ('{novo_usuario}', '{senha}', 'P')"""
        inst_SQL.execute(str_novo_user)
        str_autentic.commit()

        #== resgatando id do usuario para criação do paciente ==
        usuario_localizado = validar_usuario(novo_usuario, senha, inst_SQL)
        codigo_user = usuario_localizado[0]

        str_novo_paciente = f"""INSERT INTO T_TAJ_PACIENTE (CPF_PACIENTE, NM_PACIENTE, TEL_PACIENTE, MAIL_PACIENTE, RGHC, T_TAJ_LOGIN_ID_LOGIN) VALUES ('{cpf}', '{nome}', '{tel}', '{mail}', '{rghc}', '{codigo_user}')"""
        inst_SQL.execute(str_novo_paciente)
        str_autentic.commit()
    except Exception as erro:
        print(f"Erro: {erro}")
    else:
        print("Usuario cadastrado com sucesso!")
        print("\n")
        paciente = localizar_paciente(codigo_user, inst_SQL)
        mostrar_menu_principal(paciente)

#===================================================================================
# MENU PRINCIPAL
def mostrar_menu_principal(paciente):
    print("\n" + "=" * 50)
    print(f"🌐 BEM-VINDO(A) {paciente[0][0]}".center(50))
    print("=" * 50)
    print("1️⃣  Pesquisa de Satisfação")
    print("2️⃣  Tickets")
    print("3️⃣  Área do Paciente")
    print("4️⃣  🚪 Sair do Sistema")
    print("-" * 50)
    opcao = input("Escolha uma opção: ")
    match opcao:
        case "1":
            pesquisa_satisfacao(paciente)
        case "2":
            menu_ticket(paciente)
        case "3":
            area_paciente(paciente)
        case "4":
            main()

#=========================================================================================
# AREA DO PACIENTE
# === Area do Paciente ===
def area_paciente(paciente):
    print("\n" + "=" * 50)
    print("👤 AREA DO PACIENTE".center(50))
    print("=" * 50)
    print(f"\n Usuario: {paciente['Usuario']}")
    print(f" Nome: {paciente['Nome']}")
    print(f" Data de Nascimento: {paciente['Data de Nascimento']}")
    print("=" * 50)
    print("1️⃣  Alterar usuario")
    print("2️⃣  Alterar nome")
    print("3️⃣  Alterar senha")
    print("4️⃣  Alterar data de nascimento")
    print("5️⃣  Deletar conta")
    print("6️⃣  Voltar para o menu")
    print("-" * 50)
    opcao = input("Escolha uma opção: ")
    match opcao:
        case "1":
            alterar_usuario(paciente)
        case "2":
            alterar_nome(paciente)
        case "3":
            alterar_senha(paciente)
        case "4":
            alterar_datanasc(paciente)
        case "5":
            print("Deletar conta")
        case "6":
            mostrar_menu_principal(paciente)

# == Alterar usuario ==
def alterar_usuario(paciente):
    print("\n" + "-" * 50)
    print("Usuario atual: " + paciente['Usuario'])
    novo_usuario = input("Digite o novo usuario: ")
    print("\n Novo usuario sera: " + novo_usuario)
    print("-" * 50)
    opcao = input("Deseja salvar a alteração (1-SIM/2-NAO): ")
    match opcao:
        case "1":
            indice = localizar_usuario(lista_pacientes, paciente['Usuario'])
            lista_pacientes[indice]['Usuario'] = novo_usuario
            paciente = lista_pacientes[indice]
            area_paciente(paciente)
        case "2":
            area_paciente(paciente)

# == Alterar nome ==
def alterar_nome(paciente):
    print("\n" + "-" * 50)
    print("Nome atual: " + paciente['Nome'])
    novo_nome = input("Digite o novo nome: ")
    print("\n Novo nome sera: " + novo_nome)
    print("-" * 50)
    opcao = input("Deseja salvar a alteração (1-SIM/2-NAO): ")
    match opcao:
        case "1":
            indice = localizar_usuario(lista_pacientes, paciente['Usuario'])
            lista_pacientes[indice]['Nome'] = novo_nome
            paciente = lista_pacientes[indice]
            area_paciente(paciente)
        case "2":
            area_paciente(paciente)

# == Alterar Senha ==
def alterar_senha(paciente):
    print("\n" + "-" * 50)
    print("Senha atual: " + paciente['Senha'])
    nova_senha = input("Digite a nova senha: ")
    print("\n Novo senha sera: " + nova_senha)
    print("-" * 50)
    opcao = input("Deseja salvar a alteração (1-SIM/2-NAO): ")
    match opcao:
        case "1":
            indice = localizar_usuario(lista_pacientes, paciente['Usuario'])
            lista_pacientes[indice]['Senha'] = nova_senha
            paciente = lista_pacientes[indice]
            area_paciente(paciente)
        case "2":
            area_paciente(paciente)
# == Alterar Data de Nascimento ==
def alterar_datanasc(paciente):
    print("\n" + "-" * 50)
    print("Data de nascimento atual: " + paciente['Data de Nascimento'])
    nova_datanasc = input("Digite a nova data de nascimento: ")
    print("\n Nova data de nascimento sera: " + nova_datanasc)
    print("-" * 50)
    opcao = input("Deseja salvar a alteração (1-SIM/2-NAO): ")
    match opcao:
        case "1":
            indice = localizar_usuario(lista_pacientes, paciente['Usuario'])
            lista_pacientes[indice]['Data de Nascimento'] = nova_datanasc
            paciente = lista_pacientes[indice]
            area_paciente(paciente)
        case "2":
            area_paciente(paciente)

#=====================================================================================
# PESQUISA DE SATISFAÇÃO
# == Calcular Media Pesquisa ==
def calcular_media(notas):
    n1 = float(notas['App'])
    n2 = float(notas['Site'])
    n3 = float(notas['Suporte'])
    media = (n1 + n2 + n3) / 3
    return media

# == Pesquisa de Satisfação ==
def pesquisa_satisfacao(paciente):
    print("\n" + "=" * 50)
    print("📝 Pesquisa de Satisfação".center(50))
    print("=" * 50)
    print(f"\n Nome: {paciente['Nome']}")

    iniciar = input("\nAperte 1 para começar a pesquisa: ")

    if iniciar == "1":
        while True:
            try:
                site = float(input("\nDe 0 a 10, qual nota você dá para nosso site? "))
                if 0 <= site <= 10:
                    break
                else:
                    print("❌ Digite uma nota válida entre 0 e 10!")
            except ValueError:
                print("⚠️ Por favor, digite apenas números.")

        while True:
            try:
                app = float(input("\nDe 0 a 10, qual nota você dá para nosso aplicativo? "))
                if 0 <= app <= 10:
                    break
                else:
                    print("❌ Digite uma nota válida entre 0 e 10!")
            except ValueError:
                print("⚠️ Por favor, digite apenas números.")

        while True:
            try:
                suporte = float(input("\nDe 0 a 10, qual nota você dá para nosso suporte? "))
                if 0 <= suporte <= 10:
                    break
                else:
                    print("❌ Digite uma nota válida entre 0 e 10!")
            except ValueError:
                print("⚠️ Por favor, digite apenas números.")

        notas = {
            'App': app,
            'Site': site,
            'Suporte': suporte,
        }

        print("\n✅ Obrigado por responder à pesquisa!")
        print("----------------------------------------------")
        print("Essas foram suas notas para pesquisa:")
        for k, v in notas.items():
            print(f"{k}: {v}")
        print(f"A sua nota média foi {calcular_media(notas):.2f}")  # média com 2 casas decimais

    else:
        print("Pesquisa cancelada.")

    input("\nPressione Enter para continuar...")
    mostrar_menu_principal(paciente)

#============================================================================================
# AREA DE TICKET
def menu_ticket(paciente):
    print("\n" + "=" * 50)
    print("📝 TICKETS".center(50))
    print("=" * 50)
    print(f" Nome do Paciente: {paciente['Nome']}")
    print("=" * 50)
    print("1️⃣  Criar Ticket")
    print("2️⃣  Ver Tickets")
    print("3️⃣  Voltar para o menu")
    print("-" * 50)
    opcao = input("Escolha uma opção: ")
    match opcao:
        case "1":
            criar_ticket(paciente)
        case "2":
            visualizar_tickets(paciente)
        case "3":
            mostrar_menu_principal(paciente)

def criar_ticket(paciente):
    print("\n" + "=" * 50)
    print("📝 NOVO TICKET".center(50))
    assunto = input("\n Digite o assunto do seu ticket: ")
    problema = input("\n Agora nos explique sobre seu problema: ")
    novoticket = {
        'Id': len(lista_tickets) +2,
        'Usuario': paciente["Usuario"],
        'Assunto': assunto,
        'Problema': problema,
        'Resposta': "Sem resposta",
        'Status': True,
    }
    lista_tickets.append(novoticket)
    menu_ticket(paciente)

def visualizar_tickets(paciente):
    print("\n" + "=" * 50)
    print("📝 TODOS OS TICKETS".center(50))
    for ticket in lista_tickets:
        if ticket["Usuario"] == paciente["Usuario"]:
            for chave, valor in ticket.items():
                print(f"{chave}: {valor}")
            print("------------------------------------")
    
    input("\nPressione Enter para continuar...")
    menu_ticket(paciente)


lista_pacientes = []
pacienteteste = {
            'Usuario':"pacienteteste",
            'Senha':"1234",
            'Nome':"João Pedro",
            'Data de Nascimento':"17/20/2001"
        }
lista_pacientes.append(pacienteteste)

lista_tickets = []
ticketteste = {
    'Id':1,
    'Usuario':"pacienteteste",
    'Assunto':"Erro ao fazer login",
    'Problema':"Tentei fazer login pelo minha conta do governo mas está dando erro",
    'Resposta':"Sem resposta",
    'Status': True,
}

# Iniciar o programa
main()
