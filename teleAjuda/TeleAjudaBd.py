import pandas as pd
import oracledb as orcl
import json

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
    conexao_BD, str_autentic, inst_SQL = conectar_BD()
    while True:
        print("-" * 50)
        print("👨‍💼 1 - Sou Funcionário")
        print("🧍‍♂️ 2 - Sou Paciente")
        print("🚪 3 - Sair")
        print("-" * 50)
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            while True:
                print("\n👨‍💼 1 - Já tenho cadastro")
                print("📝 2 - Cadastrar")
                print("🔙 3 - Voltar")
                escolha = input("Escolha uma opção: ").strip()

                if escolha == "1":
                    cpf = input("Digite o CPF: ").strip()
                    senha = input("Digite a senha: ").strip()
                    cpfValidado = validar_funcionario(cpf, senha, inst_SQL)
                    if cpfValidado:
                        menu_funcionario(cpfValidado, inst_SQL, str_autentic)
                    else:
                        print("❌ Usuário ou senha incorretos. Tente novamente.")
                elif escolha == "2":
                    cpfFuncionario = cadastrar_funcionario(inst_SQL, str_autentic)
                    if cpfFuncionario:
                        menu_funcionario(cpfFuncionario,inst_SQL, str_autentic)
                    else:
                        print("❌ Falha no cadastro. Tente novamente.")
                elif escolha == "3":
                    break
                else:
                    print("⚠️ Opção inválida. Tente novamente.")
        elif opcao == "2":
            while True:
                print("\n🧍‍♂️ 1 - Já tenho cadastro")
                print("📝 2 - Cadastrar")
                print("🔙 3 - Voltar")
                escolha = input("Escolha uma opção: ").strip()

                if escolha == "1":
                    cpf = input("Digite o CPF: ").strip()
                    senha = input("Digite a senha: ").strip()
                    cpfValidado = validar_paciente(cpf, senha, inst_SQL)
                    if cpfValidado:
                        menu_paciente(cpfValidado, inst_SQL, str_autentic)
                    else:
                        print("❌ Usuário ou senha incorretos. Tente novamente.")
                elif escolha == "2":
                    cpfPaciente = cadastrar_paciente(inst_SQL, str_autentic)
                    if cpfPaciente:
                        menu_paciente(cpfPaciente, inst_SQL, str_autentic)
                    else:
                        print("❌ Falha no cadastro. Tente novamente.")
                elif escolha == "3":
                    break
                else:
                    print("⚠️ Opção inválida. Tente novamente.")
        elif opcao == "3":
            print("\n👋 Encerrando o programa. Até logo!")
            break

        else:
            print("⚠️ Opção inválida. Tente novamente.")



#================================================================================================================
# VALIDAÇÂO DE USUARIOS
def validar_paciente(cpf, senha, inst_SQL):
    sql = """
            SELECT cpf_paciente
              FROM T_TAJ_PACIENTE
             WHERE cpf_paciente = :cpf
               AND senha_paciente = :senha
            """
    inst_SQL.execute(sql, {"cpf": cpf, "senha": senha})
    row = inst_SQL.fetchone()
    if row:
        return row[0]
    return False

def validar_funcionario(cpf, senha, inst_SQL):
    sql = """
        SELECT cpf_funcionario
          FROM T_TAJ_FUNCIONARIO
         WHERE cpf_funcionario = :cpf
           AND senha_funcionario = :senha
        """
    inst_SQL.execute(sql, {"cpf": cpf, "senha": senha})
    row = inst_SQL.fetchone()
    if row:
        return row[0]
    return False

#================================================================================================================
# CADASTROS
def obter_cpf_unico(inst_SQL, tabela, coluna_cpf):
    while True:
        cpf = input("Digite o CPF: ").strip()

        sql = f"SELECT 1 FROM {tabela} WHERE {coluna_cpf} = :cpf"
        inst_SQL.execute(sql, {"cpf": cpf})
        existe = inst_SQL.fetchone()

        if existe:
            print("❌ CPF já cadastrado! Tente outro.")
        else:
            print("✅ CPF disponível!")
            return cpf


def cadastrar_funcionario(inst_SQL, conn):
    try:
        print("\n=== Cadastro de Funcionário ===")
        cpf = obter_cpf_unico(inst_SQL, "T_TAJ_FUNCIONARIO", "cpf_funcionario")
        nome = input("Nome: ")
        email = input("E-mail: ")
        senha = input("Senha: ")

        sql = """
            INSERT INTO T_TAJ_FUNCIONARIO (
                cpf_funcionario, nm_funcionario, mail_funcionario, senha_funcionario
            ) VALUES (
                :cpf, :nome, :email, :senha
            )
            """
        inst_SQL.execute(sql, {
            "cpf": cpf,
            "nome": nome,
            "email": email,
            "senha": senha
        })
        if conn:
            conn.commit()

        print("✅ Funcionário cadastrado com sucesso!")
        return cpf

    except Exception as e:
        print("Erro ao cadastrar funcionário:", e)
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        return False

def cadastrar_paciente(inst_SQL, conn):
    try:
        print("\n=== Cadastro de Paciente ===")
        cpf = obter_cpf_unico(inst_SQL, "T_TAJ_PACIENTE", "cpf_paciente")
        nome = input("Nome: ")
        telefone = input("Telefone: ")
        email = input("E-mail: ")
        rghc = input("RGHC (opcional): ")
        dt_nasc = input("Data de nascimento (YYYY-MM-DD): ")
        senha = input("Senha: ")

        sql = """
            INSERT INTO T_TAJ_PACIENTE (
                cpf_paciente, nm_paciente, tel_paciente, mail_paciente,
                rghc, dt_nasc_paciente, senha_paciente
            ) VALUES (
                :cpf, :nome, :tel, :email, :rghc, :dt_nasc, :senha
            )
            """
        inst_SQL.execute(sql, {
            "cpf": cpf,
            "nome": nome,
            "tel": telefone,
            "email": email,
            "rghc": rghc,
            "dt_nasc": dt_nasc,
            "senha": senha
        })
        if conn:
            conn.commit()

        print("✅ Paciente cadastrado com sucesso!")
        return cpf

    except Exception as e:
        print("Erro ao cadastrar paciente:", e)
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        return False




#================================================================================================================
# MENUS
def menu_funcionario(cpfFuncionario, inst_SQL, conn):
    print("\n" + "=" * 50)
    print(f"🌐 BEM-VINDO(A)".center(50))
    print("=" * 50)
    print("1️⃣  Pesquisa de Satisfação")
    print("2️⃣  Tickets")
    print("3️⃣  Área do Funcionario")
    print("4️⃣  🚪 Sair do Sistema")
    print("-" * 50)
    opcao = input("Escolha uma opção: ")
    match opcao:
        case "1":
            menu_pesquisa_func(cpfFuncionario, inst_SQL, conn)
        case "2":
            menu_ticket_func(cpfFuncionario, inst_SQL, conn)
        case "3":
            area_funcionario(cpfFuncionario, inst_SQL, conn)
        case "4":
            main()

def menu_paciente(cpfPaciente, inst_SQL, conn):
    print("\n" + "=" * 50)
    print(f"🌐 BEM-VINDO(A)".center(50))
    print("=" * 50)
    print("1️⃣  Pesquisa de Satisfação")
    print("2️⃣  Tickets")
    print("3️⃣  Área do Paciente")
    print("4️⃣  🚪 Sair do Sistema")
    print("-" * 50)
    opcao = input("Escolha uma opção: ")
    match opcao:
        case "1":
            menu_pesquisa(cpfPaciente, inst_SQL, conn)
        case "2":
            menu_ticket(cpfPaciente, inst_SQL, conn)
        case "3":
            area_paciente(cpfPaciente, inst_SQL, conn)
        case "4":
            main()

#=========================================================================================
# AREA DO PACIENTE
# === Area do Paciente ===
def area_paciente(cpfPaciente, inst_SQL, conn=None):
    while True:
        inst_SQL.execute("""
            SELECT cpf_paciente,
                   nm_paciente,
                   tel_paciente,
                   mail_paciente,
                   rghc,
                   dt_nasc_paciente
              FROM T_TAJ_PACIENTE
             WHERE cpf_paciente = :cpf
        """, {"cpf": cpfPaciente})
        row = inst_SQL.fetchone()

        print("\n" + "=" * 50)
        print("👤 ÁREA DO PACIENTE".center(50))
        print("=" * 50)

        if not row:
            print("❌ Paciente não encontrado.")
            return

        cols = ["CPF", "Nome", "Telefone", "E-mail", "RGHC", "Data de Nascimento"]
        df = pd.DataFrame([row], columns=cols)
        print(df.to_string(index=False))

        print("=" * 50)
        print("1️⃣  Alterar nome")
        print("2️⃣  Alterar telefone")
        print("3️⃣  Alterar e-mail")
        print("4️⃣  Alterar RGHC")
        print("5️⃣  Alterar data de nascimento")
        print("6️⃣  Alterar senha")
        print("7️⃣  Voltar ao menu principal")
        print("=" * 50)

        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                alterar_nome_paciente(cpfPaciente, inst_SQL, conn)
            case "2":
                alterar_telefone_paciente(cpfPaciente, inst_SQL, conn)
            case "3":
                alterar_email_paciente(cpfPaciente, inst_SQL, conn)
            case "4":
                alterar_rghc_paciente(cpfPaciente, inst_SQL, conn)
            case "5":
                alterar_datanasc_paciente(cpfPaciente, inst_SQL, conn)
            case "6":
                alterar_senha_paciente(cpfPaciente, inst_SQL, conn)
            case "7":
                menu_paciente(cpfPaciente, inst_SQL, conn)
            case _:
                print("⚠️ Opção inválida. Tente novamente.")

# == Alterar nome ==
def alterar_nome_paciente(cpfPaciente, inst_SQL, conn=None):
    print("\n" + "-" * 50)
    novo_nome = input("Digite o novo nome: ").strip()
    print("\nNovo nome será: " + novo_nome)
    print("-" * 50)
    opcao = input("Deseja salvar a alteração? (1 - SIM / 2 - NÃO): ").strip()
    match opcao:
        case "1":
            try:
                sql = """
                    UPDATE T_TAJ_PACIENTE
                       SET nm_paciente = :novo_nome
                     WHERE cpf_paciente = :cpf
                """
                inst_SQL.execute(sql, {"novo_nome": novo_nome, "cpf": cpfPaciente})
                if conn:
                    conn.commit()
                print("\n✅ Nome atualizado com sucesso!")
            except Exception as e:
                print("❌ Erro ao atualizar nome:", e)
                if conn:
                    try:
                        conn.rollback()
                    except Exception:
                        pass
        case "2":
            print("\n↩️ Alteração cancelada.")
            area_paciente(cpfPaciente, inst_SQL, conn)
        case _:
            print("\n⚠️ Opção inválida, nenhuma alteração feita.")

    input("\nPressione Enter para continuar...")
    area_paciente(cpfPaciente, inst_SQL, conn)

# == Alterar telefone ==
def alterar_telefone_paciente(cpfPaciente, inst_SQL, conn=None):
    novo = input("Digite o novo telefone: ").strip()
    print("\nNovo telefone será: " + novo); print("-" * 50)
    op = input("Deseja salvar a alteração? (1 - SIM / 2 - NÃO): ").strip()
    match op:
        case "1":
            try:
                inst_SQL.execute("""
                    UPDATE T_TAJ_PACIENTE
                       SET tel_paciente = :v
                     WHERE cpf_paciente = :cpf
                """, {"v": novo, "cpf": cpfPaciente})
                if conn: conn.commit()
                print("\n✅ Telefone atualizado com sucesso!")
            except Exception as e:
                print("❌ Erro ao atualizar telefone:", e)
                if conn:
                    try: conn.rollback()
                    except Exception: pass
        case "2":
            print("\n↩️ Alteração cancelada.")
            area_paciente(cpfPaciente, inst_SQL, conn)
        case _:   print("\n⚠️ Opção inválida, nenhuma alteração feita.")
    input("\nEnter para continuar...")
    area_paciente(cpfPaciente, inst_SQL, conn)

# == Alterar e-mail ==
def alterar_email_paciente(cpfPaciente, inst_SQL, conn=None):
    print("\n" + "-" * 50)
    novo = input("Digite o novo e-mail: ").strip()
    print("\nNovo e-mail será: " + novo); print("-" * 50)
    op = input("Deseja salvar a alteração? (1 - SIM / 2 - NÃO): ").strip()
    match op:
        case "1":
            try:
                inst_SQL.execute("""
                    UPDATE T_TAJ_PACIENTE
                       SET mail_paciente = :v
                     WHERE cpf_paciente = :cpf
                """, {"v": novo, "cpf": cpfPaciente})
                if conn: conn.commit()
                print("\n✅ E-mail atualizado com sucesso!")
            except Exception as e:
                print("❌ Erro ao atualizar e-mail:", e)
                if conn:
                    try: conn.rollback()
                    except Exception: pass
        case "2":
            print("\n↩️ Alteração cancelada.")
            area_paciente(cpfPaciente, inst_SQL, conn)
        case _:
            print("\n⚠️ Opção inválida, nenhuma alteração feita.")
    input("\nEnter para continuar...")
    area_paciente(cpfPaciente, inst_SQL, conn)

# == Alterar RGHC ==
def alterar_rghc_paciente(cpfPaciente, inst_SQL, conn=None):
    print("\n" + "-" * 50)
    novo = input("Digite o novo RGHC: ").strip()
    print("\nNovo RGHC será: " + novo); print("-" * 50)
    op = input("Deseja salvar a alteração? (1 - SIM / 2 - NÃO): ").strip()
    match op:
        case "1":
            try:
                inst_SQL.execute("""
                    UPDATE T_TAJ_PACIENTE
                       SET rghc = :v
                     WHERE cpf_paciente = :cpf
                """, {"v": novo, "cpf": cpfPaciente})
                if conn: conn.commit()
                print("\n✅ RGHC atualizado com sucesso!")
            except Exception as e:
                print("❌ Erro ao atualizar RGHC:", e)
                if conn:
                    try: conn.rollback()
                    except Exception: pass
        case "2":
            print("\n↩️ Alteração cancelada.")
            area_paciente(cpfPaciente, inst_SQL, conn)
        case _:
            print("\n⚠️ Opção inválida, nenhuma alteração feita.")
    input("\nEnter para continuar...")
    area_paciente(cpfPaciente, inst_SQL, conn)

# == Alterar data de nascimento ==
def alterar_datanasc_paciente(cpfPaciente, inst_SQL, conn=None):
    print("\n" + "-" * 50)
    novo = input("Digite a nova data de nascimento (DD-MM-AAAA): ").strip()
    print("\nNova data será: " + novo); print("-" * 50)
    op = input("Deseja salvar a alteração? (1 - SIM / 2 - NÃO): ").strip()
    match op:
        case "1":
            try:
                inst_SQL.execute("""
                    UPDATE T_TAJ_PACIENTE
                       SET dt_nasc_paciente = :v
                     WHERE cpf_paciente = :cpf
                """, {"v": novo, "cpf": cpfPaciente})
                if conn: conn.commit()
                print("\n✅ Data de nascimento atualizada com sucesso!")
            except Exception as e:
                print("❌ Erro ao atualizar data de nascimento:", e)
                if conn:
                    try: conn.rollback()
                    except Exception: pass
        case "2":
            print("\n↩️ Alteração cancelada.")
            area_paciente(cpfPaciente, inst_SQL, conn)
        case _:
            print("\n⚠️ Opção inválida, nenhuma alteração feita.")
    input("\nEnter para continuar...")
    area_paciente(cpfPaciente, inst_SQL, conn)

# == Alterar senha ==
def alterar_senha_paciente(cpfPaciente, inst_SQL, conn=None):
    print("\n" + "-" * 50)
    nova = input("Digite a nova senha: ").strip()
    op = input("Deseja salvar a alteração? (1 - SIM / 2 - NÃO): ").strip()
    match op:
        case "1":
            try:
                inst_SQL.execute("""
                    UPDATE T_TAJ_PACIENTE
                       SET senha_paciente = :v
                     WHERE cpf_paciente = :cpf
                """, {"v": nova, "cpf": cpfPaciente})
                if conn: conn.commit()
                print("\n✅ Senha atualizada com sucesso!")
            except Exception as e:
                print("❌ Erro ao atualizar senha:", e)
                if conn:
                    try: conn.rollback()
                    except Exception: pass
        case "2":
            print("\n↩️ Alteração cancelada.")
            area_paciente(cpfPaciente, inst_SQL, conn)
        case _:
            print("\n⚠️ Opção inválida, nenhuma alteração feita.")
    input("\nEnter para continuar...")
    area_paciente(cpfPaciente, inst_SQL, conn)

#======================================================================================
#AREA DO FUNCIONARIO
# === Área do Funcionário ===
def area_funcionario(cpfFuncionario, inst_SQL, conn=None):
    while True:
        sql = """
            SELECT cpf_funcionario,
                   nm_funcionario,
                   mail_funcionario
              FROM T_TAJ_FUNCIONARIO
             WHERE cpf_funcionario = :cpf
        """
        inst_SQL.execute(sql, {"cpf": cpfFuncionario})
        row = inst_SQL.fetchone()

        print("\n" + "=" * 50)
        print("🧑‍💼 ÁREA DO FUNCIONÁRIO".center(50))
        print("=" * 50)

        cols = ["CPF", "Nome", "E-mail"]
        df = pd.DataFrame([row], columns=cols)
        print(df.to_string(index=False))

        print("=" * 50)
        print("1️⃣  Alterar nome")
        print("2️⃣  Alterar e-mail")
        print("3️⃣  Alterar senha")
        print("4️⃣  Voltar ao menu principal")
        print("=" * 50)
        opcao = input("Escolha uma opção: ").strip()
        match opcao:
            case "1":
                alterar_nome_funcionario(cpfFuncionario, inst_SQL, conn)
            case "2":
                alterar_email_funcionario(cpfFuncionario, inst_SQL, conn)
            case "3":
                alterar_senha_funcionario(cpfFuncionario, inst_SQL, conn)
            case "4":
                menu_funcionario(cpfFuncionario, inst_SQL, conn)
            case _:
                print("⚠️ Opção inválida. Tente novamente.")


# == Alterar nome ==
def alterar_nome_funcionario(cpfFuncionario, inst_SQL, conn=None):
    print("\n" + "-" * 50)
    novo = input("Digite o novo nome: ").strip()
    print("\nNovo nome será: " + novo); print("-" * 50)

    op = input("Deseja salvar a alteração? (1 - SIM / 2 - NÃO): ").strip()
    match op:
        case "1":
            try:
                inst_SQL.execute("""
                    UPDATE T_TAJ_FUNCIONARIO
                       SET nm_funcionario = :v
                     WHERE cpf_funcionario = :cpf
                """, {"v": novo, "cpf": cpfFuncionario})
                if conn: conn.commit()
                print("\n✅ Nome atualizado com sucesso!")
            except Exception as e:
                print("❌ Erro ao atualizar nome:", e)
                if conn:
                    try: conn.rollback()
                    except Exception: pass
        case "2": print("\n↩️ Alteração cancelada.")
        case _:   print("\n⚠️ Opção inválida, nenhuma alteração feita.")
    input("\nPressione Enter para continuar...")


# == Alterar e-mail ==
def alterar_email_funcionario(cpfFuncionario, inst_SQL, conn=None):
    print("\n" + "-" * 50)
    novo = input("Digite o novo e-mail: ").strip()
    print("\nNovo e-mail será: " + novo); print("-" * 50)

    op = input("Deseja salvar a alteração? (1 - SIM / 2 - NÃO): ").strip()
    match op:
        case "1":
            try:
                inst_SQL.execute("""
                    UPDATE T_TAJ_FUNCIONARIO
                       SET mail_funcionario = :v
                     WHERE cpf_funcionario = :cpf
                """, {"v": novo, "cpf": cpfFuncionario})
                if conn: conn.commit()
                print("\n✅ E-mail atualizado com sucesso!")
            except Exception as e:
                print("❌ Erro ao atualizar e-mail:", e)
                if conn:
                    try: conn.rollback()
                    except Exception: pass
        case "2": print("\n↩️ Alteração cancelada.")
        case _:   print("\n⚠️ Opção inválida, nenhuma alteração feita.")
    input("\nPressione Enter para continuar...")


# == Alterar senha ==
def alterar_senha_funcionario(cpfFuncionario, inst_SQL, conn=None):
    print("\n" + "-" * 50)
    nova = input("Digite a nova senha: ").strip()
    conf = input("Confirme a nova senha: ").strip()
    if nova != conf:
        print("❌ As senhas não conferem.")
        input("\nPressione Enter para continuar...")
        return

    print("\nA nova senha será salva."); print("-" * 50)
    op = input("Deseja salvar a alteração? (1 - SIM / 2 - NÃO): ").strip()
    match op:
        case "1":
            try:
                inst_SQL.execute("""
                    UPDATE T_TAJ_FUNCIONARIO
                       SET senha_funcionario = :v
                     WHERE cpf_funcionario = :cpf
                """, {"v": nova, "cpf": cpfFuncionario})
                if conn: conn.commit()
                print("\n✅ Senha atualizada com sucesso!")
            except Exception as e:
                print("❌ Erro ao atualizar senha:", e)
                if conn:
                    try: conn.rollback()
                    except Exception: pass
        case "2": print("\n↩️ Alteração cancelada.")
        case _:   print("\n⚠️ Opção inválida, nenhuma alteração feita.")
    input("\nPressione Enter para continuar...")

#=====================================================================================
# PESQUISA DE SATISFAÇÃO
## VERSÃO PACIENTE ---------------------------------------------------------
def menu_pesquisa(cpfPaciente, inst_SQL, conn=None):
    while True:
        print("\n" + "=" * 50)
        print("📊 SUAS PESQUISAS DE SATISFAÇÃO".center(50))
        print("=" * 50)

        sql = """
            SELECT id_pesquisa_satis,
                   nt_app, nt_site, nt_suporte,
                   dt_pesquisa
              FROM T_TAJ_PESQUISA_SATIS
             WHERE PACIENTE_cpf_paciente = :cpf
             ORDER BY id_pesquisa_satis DESC
        """
        inst_SQL.execute(sql, {"cpf": cpfPaciente})
        rows = inst_SQL.fetchall()

        cols = ["id", "nt_app", "nt_site", "nt_suporte", "data"]
        df = pd.DataFrame(rows, columns=cols)

        if df.empty:
            print("Nenhuma pesquisa encontrada para este paciente.")
        else:
            print(df.to_string(index=False))

        print("\n1️⃣ 📝 Adicionar nova pesquisa")
        print("2️⃣ ↩️ Voltar")
        acao = input("Escolha uma opção: ").strip()

        if acao == "1":
            criar_pesquisa(cpfPaciente, inst_SQL, conn)
            continue
        elif acao == "2":
            menu_paciente(cpfPaciente, inst_SQL, conn)
        else:
            print("⚠️ Opção inválida. Tente novamente.")


# == Calcular Media Pesquisa ==
def calcular_media(notas):
    n1 = float(notas['App'])
    n2 = float(notas['Site'])
    n3 = float(notas['Suporte'])
    media = (n1 + n2 + n3) / 3
    return media


# == Criar Pesquisa de Satisfação ==
def criar_pesquisa(cpfPaciente, inst_SQL, conn=None):
    print("\n" + "=" * 50)
    print("📝 Pesquisa de Satisfação".center(50))
    print("=" * 50)
    print(f"\n CPF do paciente: {cpfPaciente}")

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
        try:
            sql = """
                        INSERT INTO T_TAJ_PESQUISA_SATIS
                            (nt_app, nt_site, nt_suporte, dt_pesquisa, PACIENTE_cpf_paciente)
                        VALUES
                            (:app, :site, :suporte, SYSDATE, :cpf)
                        """
            inst_SQL.execute(sql, {
                "app": int(round(app)),
                "site": int(round(site)),
                "suporte": int(round(suporte)),
                "cpf": cpfPaciente
            })
            if conn:
                conn.commit()
        except Exception as e:
            print("❌ Erro ao salvar a pesquisa no banco:", e)
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass

        print("\n✅ Obrigado por responder à pesquisa!")
        print("----------------------------------------------")
        print("Essas foram suas notas para pesquisa:")
        for k, v in notas.items():
            print(f"{k}: {v}")
        print(f"A sua nota média foi {calcular_media(notas):.2f}")

    else:
        print("Pesquisa cancelada.")

    input("\nPressione Enter para continuar...")

## VERSÃO FUNCIONARIO
# === VERSÃO FUNCIONÁRIO ===
def menu_pesquisa_func(cpfFuncionario, inst_SQL, conn=None):
    while True:
        print("\n" + "=" * 60)
        print("🧾 PESQUISAS DE SATISFAÇÃO".center(60))
        print("=" * 60)
        sql = """
            SELECT P.id_pesquisa_satis,
                   P.nt_app,
                   P.nt_site,
                   P.nt_suporte,
                   P.dt_pesquisa,
                   C.nm_paciente,
                   C.cpf_paciente
              FROM T_TAJ_PESQUISA_SATIS P
              JOIN T_TAJ_PACIENTE C
                ON P.PACIENTE_cpf_paciente = C.cpf_paciente
             ORDER BY P.id_pesquisa_satis DESC
        """
        inst_SQL.execute(sql)
        rows = inst_SQL.fetchall()
        cols = ["ID", "Nota App", "Nota Site", "Nota Suporte",
            "Data Pesquisa", "Nome Paciente", "CPF Paciente"]
        df = pd.DataFrame(rows, columns=cols)
        print(df.to_string(index=False))
        
        print("\n1️⃣ Exportar todas as pesquisas para JSON")
        print("2️⃣ ↩️ Voltar ao menu principal do funcionário")
        print("=" * 60)
        acao = input("Escolha uma opção: ").strip()

        if acao == "1":
            if df is None or df.empty:
                print("Nao ha pesquisas para exportar.")
                return
            registros = df.to_dict(orient="records")
            with open("pesquisa.json", "w", encoding="utf-8") as arq:
                json.dump(registros, arq, ensure_ascii=False, indent=4)

            print("Arquivo JSON gravado com sucesso!")
            input("\nPressione Enter para continuar...")
            continue
        elif acao == "2":
            menu_funcionario(cpfFuncionario, inst_SQL, conn)
        else:
            print("⚠️ Opção inválida. Tente novamente.")


#============================================================================================
# AREA DE TICKET PACIENTE
def criar_ticket(cpfPaciente, inst_SQL, conn=None):
    print("\n" + "=" * 50)
    print("🎫 CRIAR TICKET".center(50))
    print("=" * 50)
    while True:
        assunto = input("Assunto: ").strip()
        if assunto:
            break
        print("❌ Assunto não pode ser vazio.")

    while True:
        descricao = input("Descrição: ").strip()
        if descricao:
            break
        print("❌ Descrição não pode ser vazia.")

    confirmar = input("\nConfirmar abertura do ticket? (1-SIM / 2-NÃO): ").strip()

    if confirmar != "1":
        print("↩️ Abertura cancelada.")
        input("\nPressione Enter para continuar...")
        menu_ticket(cpfPaciente, inst_SQL, conn)

    try:
        sql = """
            INSERT INTO T_TAJ_TICKET
                (assunto, descricao, dt_abertura, status, PACIENTE_cpf_paciente)
            VALUES
                (:assunto, :descricao, SYSDATE, 'A', :cpf)
        """
        inst_SQL.execute(sql, {
            "assunto": assunto,
            "descricao": descricao,
            "cpf": cpfPaciente
        })
        if conn:
            conn.commit()

        print("\n✅ Ticket criado com sucesso!")
    except Exception as e:
        print("❌ Erro ao criar ticket:", e)
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass

    input("\nPressione Enter para continuar...")
    menu_ticket(cpfPaciente, inst_SQL, conn)

def alterar_descricao_ticket(id_ticket, cpfPaciente, inst_SQL, conn=None):
    print("\n" + "-" * 50)
    while True:
        nova_desc = input("Digite a nova descrição: ").strip()
        if nova_desc:
            break
        print("❌ A descrição não pode ser vazia.")
        input("\nPressione Enter para tentar novamente...")

    confirmar = input("Confirmar alteração? (1-SIM / 2-NÃO): ").strip()
    if confirmar != "1":
        print("↩️ Alteração cancelada.")
        input("\nPressione Enter para continuar...")
        menu_ticket(cpfPaciente, inst_SQL, conn)

    try:
        sql = """
            UPDATE T_TAJ_TICKET
               SET descricao = :p_desc
             WHERE id_ticket = :p_id
               AND PACIENTE_cpf_paciente = :p_cpf
        """
        inst_SQL.execute(sql, {
            "p_desc": nova_desc,
            "p_id": id_ticket,
            "p_cpf": cpfPaciente
        })
        if conn:
            conn.commit()

        if conn:
            conn.commit()
        print("✅ Descrição atualizada com sucesso!")
    except Exception as e:
        print("❌ Erro ao atualizar descrição:", e)
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass

    input("\nPressione Enter para continuar...")
    menu_ticket(cpfPaciente, inst_SQL, conn)



def visualizar_ticket(cpfPaciente, inst_SQL, conn=None):
    print("\n" + "=" * 50)
    print("🔎 VISUALIZAR TICKET".center(50))
    print("=" * 50)

    try:
        id_str = input("Digite o código do ticket: ").strip()
        id_ticket = int(id_str)
    except ValueError:
        print("⚠️ Código inválido.")
        input("\nPressione Enter para continuar...")
        return

    sql = """
            SELECT  t.id_ticket,
                    t.assunto,
                    t.descricao,
                    t.resposta,
                    t.dt_abertura,
                    t.dt_fechamento,
                    t.status,
                    f.nm_funcionario
              FROM  T_TAJ_TICKET t
              LEFT JOIN T_TAJ_FUNCIONARIO f
                ON  t.FUNCIONARIO_cpf_funcionario = f.cpf_funcionario
             WHERE  t.id_ticket = :id
               AND  t.PACIENTE_cpf_paciente = :cpf
        """
    inst_SQL.execute(sql, {"id": id_ticket, "cpf": cpfPaciente})
    row = inst_SQL.fetchone()

    if not row:
        print("❌ Ticket não encontrado para este paciente.")
        input("\nPressione Enter para continuar...")
        return

    print("\n" + "-" * 50)
    print("\n" + "-" * 50)
    print(f"🆔 Código:        {row[0]}")
    print(f"➡️ Assunto:       {row[1]}")
    print(f"➡️ Descrição:     {row[2]}")
    print(f"➡️ Resposta:      {row[3]}")
    print(f"📅 Abertura:      {row[4]}")
    print(f"📅 Fechamento:    {row[5]}")
    print(f"➡️  Status:        {row[6]}")
    print(f"👤 Funcionário responsável: {row[7]}")
    print("-" * 50)
    print("\n1️⃣ Alterar descrição")
    print("2️⃣ ↩️ Voltar")
    acao = input("Escolha uma opção: ").strip()
    match acao:
        case "1":
            alterar_descricao_ticket(id_ticket, cpfPaciente, inst_SQL, conn)
            return visualizar_ticket(cpfPaciente, inst_SQL, conn)
        case "2":
            menu_ticket(cpfPaciente, inst_SQL, conn)
        case _:
            print("⚠️ Opção inválida.")
            input("\nPressione Enter para continuar...")
            return

def menu_ticket(cpfPaciente, inst_SQL, conn=None):
    while True:
        print("\n" + "=" * 50)
        print("🎫 TICKETS".center(50))
        print("=" * 50)
        sql = """
                    SELECT id_ticket,
                           dt_abertura,
                           assunto
                      FROM T_TAJ_TICKET
                     WHERE PACIENTE_cpf_paciente = :cpf
                     ORDER BY id_ticket DESC
                """
        inst_SQL.execute(sql, {"cpf": cpfPaciente})
        rows = inst_SQL.fetchall()
        cols = ["Código", "Data de Abertura", "Assunto"]
        df = pd.DataFrame(rows, columns=cols)
        if df.empty:
            print("Nenhum ticket encontrado.")
        else:
            print(df.to_string(index=False))

        print("\n1️⃣ Criar Ticket")
        print("2️⃣ Visualizar ticket")
        print("3️⃣ Voltar para o menu")
        opcao = input("Escolha uma opção: ").strip()
        match opcao:
            case "1":
                criar_ticket(cpfPaciente, inst_SQL, conn)
            case "2":
                visualizar_ticket(cpfPaciente, inst_SQL, conn)
            case "3":
                menu_paciente(cpfPaciente, inst_SQL, conn)

#AREA TICKET FUNCIONÁRIO =====================================================
def responder_ticket(cpfFuncionario, inst_SQL, conn=None):
    print("\n" + "=" * 60)
    print("✍️ RESPONDER TICKET".center(60))
    print("=" * 60)

    try:
        id_ticket = int(input("Digite o código do ticket: ").strip())
    except ValueError:
        print("⚠️ Código inválido.")
        input("\nPressione Enter para continuar...")
        menu_ticket_func(cpfFuncionario, inst_SQL, conn)

    sql = """
        SELECT  t.id_ticket,
                t.assunto,
                t.descricao,
                t.resposta,
                t.dt_abertura,
                t.dt_fechamento,
                t.status,
                p.cpf_paciente,
                p.nm_paciente
          FROM  T_TAJ_TICKET t
          JOIN  T_TAJ_PACIENTE p
            ON  p.cpf_paciente = t.PACIENTE_cpf_paciente
         WHERE  t.id_ticket = :p_id
    """
    inst_SQL.execute(sql, {"p_id": id_ticket})
    row = inst_SQL.fetchone()

    if not row:
        print("❌ Ticket não encontrado.")
        input("\nPressione Enter para continuar...")
        menu_ticket_func(cpfFuncionario, inst_SQL, conn)

    print("\n" + "-" * 60)
    print(f"🆔 Código:        {row[0]}")
    print(f"➡️ Assunto:       {row[1]}")
    print(f"➡️ Descrição:     {row[2]}")
    print(f"➡️ Resposta:      {row[3]}")
    print(f"📅 Abertura:      {row[4]}")
    print(f"📅 Fechamento:    {row[5]}")
    print(f"➡️  Status:        {row[6]}")
    print(f"👤 CPF Paciente:  {row[7]}")
    print(f"👤 Nome Paciente: {row[8]}")
    print("-" * 60)

    if str(row[6]).upper().strip() != "A":
        print("⚠️ Este ticket não está aberto. Não é possível responder.")
        input("\nPressione Enter para continuar...")
        menu_ticket_func(cpfFuncionario, inst_SQL, conn)

    while True:
        resposta = input("Digite a resposta: ").strip()
        if resposta:
            break
        print("❌ A resposta não pode ser vazia.")

    confirmar = input("Confirmar envio e fechamento do ticket? (1-SIM / 2-NÃO): ").strip()
    if confirmar != "1":
        print("↩️ Operação cancelada.")
        input("\nPressione Enter para continuar...")
        menu_ticket_func(cpfFuncionario, inst_SQL, conn)

    try:
        update_sql = """
            UPDATE T_TAJ_TICKET
               SET resposta = :p_resp,
                   dt_fechamento = SYSDATE,
                   status = 'F',
                   FUNCIONARIO_cpf_funcionario = :p_func
             WHERE id_ticket = :p_id
               AND status = 'A'
        """
        inst_SQL.execute(update_sql, {
            "p_resp": resposta,
            "p_func": cpfFuncionario,
            "p_id": id_ticket
        })
        if conn:
            conn.commit()
        print("\n✅ Ticket respondido e fechado com sucesso!")
    except Exception as e:
        print("❌ Erro ao fechar/responder ticket:", e)
        if conn:
            try: conn.rollback()
            except Exception: pass

    input("\nPressione Enter para continuar...")
    menu_ticket_func(cpfFuncionario, inst_SQL, conn)


def menu_ticket_func(cpfFuncionario, inst_SQL, conn=None):
    while True:
        print("\n" + "=" * 60)
        print("🎫 TICKETS".center(60))
        print("=" * 60)

        sql = """
            SELECT  t.id_ticket,
                    t.dt_abertura,
                    t.assunto,
                    t.PACIENTE_cpf_paciente,
                    p.nm_paciente
              FROM  T_TAJ_TICKET t
              JOIN  T_TAJ_PACIENTE p
                ON  p.cpf_paciente = t.PACIENTE_cpf_paciente
             WHERE  t.status = 'A'
               AND  t.FUNCIONARIO_cpf_funcionario IS NULL
             ORDER BY t.id_ticket DESC
        """
        inst_SQL.execute(sql)
        rows = inst_SQL.fetchall()

        cols = ["Código", "Data de Abertura", "Assunto", "CPF Paciente", "Nome Paciente"]
        df = pd.DataFrame(rows, columns=cols)

        if df.empty:
            print("Nenhum ticket aberto aguardando atendimento.")
        else:
            print(df.to_string(index=False))

        print("\n" + "-" * 60)
        print("1️⃣ Responder ticket")
        print("2️⃣ Meus tickets")
        print("3️⃣ Voltar")
        print("-" * 60)
        acao = input("Escolha uma opção: ").strip()
        match acao:
            case "1":
                responder_ticket(cpfFuncionario, inst_SQL, conn)
                continue
            case "2":
                meus_tickets(cpfFuncionario, inst_SQL, conn)
                continue
            case "3":
                menu_funcionario(cpfFuncionario, inst_SQL, conn)
            case _:
                print("⚠️ Opção inválida. Tente novamente.")



# Iniciar o programa
if __name__ == "__main__":
    main()
