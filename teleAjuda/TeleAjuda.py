
# AREA DO USUARIO
# == Validação do Usuario ==
def validar_usuario(lista_pacientes, usuario, senha):
    for i in range(len(lista_pacientes)):
        if (lista_pacientes[i]['Usuario'] == usuario and lista_pacientes[i]['Senha'] == senha):
            print("Conectando...")
            paciente = lista_pacientes[i]
            return paciente
    return False

# == Localizar indice do usuario ==
def localizar_usuario(lista_pacientes, usuario):
    indice = -1
    for i in range(len(lista_pacientes)):
        if (lista_pacientes[i]['Usuario'] == usuario):
            indice = i
    return(indice)

# == Cadastrar Usuario ==
def cadastrar_usuario(lista_pacientes):
    try:
        usuario = input("Digite o usuario: ")
        indice = localizar_usuario(lista_pacientes,usuario)
        while (indice != -1): # quer dizer que o codigo ja existe
            usuario = input("Esse usuario ja existe! Digite outro usuario: ")
            indice = localizar_usuario(lista_pacientes, usuario)
        # inputs dos outros dados
        senha = input("Digite sua senha: ")
        nome = input("Digite seu nome: ")
        datanasc = input("Digite sua data de nascimento: ")
    except ValueError:
        print("Houve um erro nos seus dados, tente novamente")
    else:
        paciente = {
            'Usuario':usuario,
            'Senha':senha,
            'Nome':nome,
            'Data de Nascimento':datanasc
        }
        lista_pacientes.append(paciente)
        print("Paciente cadastrado com sucesso!")
        mostrar_menu_principal(paciente)

#===================================================================================
# MENU PRINCIPAL
def mostrar_menu_principal(paciente):
    print("\n" + "=" * 50)
    print(f"🌐 BEM-VINDO(A) {paciente['Nome']}".center(50))
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
            alterar_usuario(paciente)
        case "2":
            alterar_nome(paciente)
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

def visualizar_tickets(paciente):
    return False;



#==============================================================================================
# INICIO DO PROGRAMA
def main():
    print("\n" + "=" * 50)
    print("🌐 SISTEMA DE ATENDIMENTO AO USUÁRIO".center(50))
    print("=" * 50)
    print("1️⃣  Já tenho cadastro")
    print("2️⃣  Fazer cadastro")
    opcao = input("Escolha uma oção: ")
    if opcao == "1":
        usuario = input("\nUsuario: ")
        senha = input("\nSenha: ")
        paciente = validar_usuario(lista_pacientes, usuario, senha)
        if paciente:
            mostrar_menu_principal(paciente)
        else:
            print("Usuario ou senha incorretos. Tente novamente")
            main()

    else:
        cadastrar_usuario(lista_pacientes)

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
