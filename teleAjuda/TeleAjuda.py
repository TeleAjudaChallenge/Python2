def validar_usuario(lista_pacientes, usuario, senha):
    for i in range(len(lista_pacientes)):
        if (lista_pacientes[i]['Usuario'] == usuario and lista_pacientes[i]['Senha'] == senha):
            print("Conectando...")
            mostrar_menu_principal(lista_pacientes[i])

def localizar_usuario(lista_pacientes, usuario):
    indice = -1
    for i in range(len(lista_pacientes)):
        if (lista_pacientes[i]['Usuario'] == usuario):
            indice = i
    return(indice)

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



# === Menu Principal ===
def mostrar_menu_principal(paciente):
    print("\n" + "=" * 50)
    print(f"🌐 BEM-VINDO(A) {paciente['Nome']}".center(50))
    print("=" * 50)
    print("1️⃣  Pesquisa de Satisfação")
    print("2️⃣  Tickets")
    print("3️⃣  Chatbot")
    print("4️⃣  Lembretes")
    print("5️⃣  Área do Paciente")
    print("6️⃣  🚪 Sair do Sistema")
    print("-" * 50)
    opcao = input("Escolha uma opção: ")
    match opcao:
        case "1":
            pesquisa_satisfacao(paciente)
        case "2":
            print("Tickets")
        case "3":
            print("Chatbot")
        case "4":
            print("Lembretes")
        case "5":
            print("Area do Paciente")
        case "6":
            main()

def calcular_media(notas):
    n1 = float(notas['App'])
    n2 = float(notas['Site'])
    n3 = float(notas['Suporte'])
    media = (n1 + n2 + n3) / 3
    return media


def pesquisa_satisfacao(nome):
    print("\n" + "=" * 50)
    print("📝 Pesquisa de Satisfação".center(50))
    print("=" * 50)
    print(f"\n Nome: {nome}")
    iniciar = input("\nAperte 1 para começar a pesquisa: ")
    if iniciar == "1":
        while True:
            site = float(input("\nDe 0 a 10, qual nota você dá para nosso site? "))
            if (site >= 0 and site <= 10):
                break
            else:
                print("❌Digite uma nota valida!")

        while True:
            app = float(input("\nDe 0 a 10, qual nota você dá para nosso aplicativo? "))
            if (app >= 0 and app <= 10):
                break
            else:
                print("❌Digite uma nota valida!")

        while True:
            suporte = input("\nDe 0 a 10, qual nota você dá para nosso suporte? ")
            if (suporte >= 0 and suporte <= 10):
                break
            else:
                print("❌Digite uma nota valida!")
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
        print(f"A sua nota média foi {calcular_media(notas)}")
    else:
        print("Pesquisa cancelada.")
    input("\nPressione Enter para continuar...")




# === Main ===
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
        validar_usuario(lista_pacientes, usuario, senha)
    else:
        cadastrar_usuario(lista_pacientes)


# === Inicio do Programa ===
lista_pacientes = []
pacienteteste = {
            'Usuario':"pacienteteste",
            'Senha':"1234",
            'Nome':"João Pedro",
            'Data de Nascimento':"17/20/2001"
        }
lista_pacientes.append(pacienteteste)

# Iniciar o programa
main()
