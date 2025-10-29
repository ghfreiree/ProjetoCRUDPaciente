import oracledb

def get_conexao():
    try:
        conn = oracledb.connect(
            user= input('Digite seu usuário: '),
            password= input('Digite sua senha: '),
            host="oracle.fiap.com.br",
            port="1521",
            service_name="orcl"
        )
        print('Conexão com Oracle DB realizada!')
        return conn
    except Exception as e:
        print(f'Erro ao obter a conexão: {e}')
        return None


def criar_tabela(conn):
    try:
        cursor = conn.cursor()
        sql = """
            CREATE TABLE pacientes(
                id number GENERATED ALWAYS AS IDENTITY,
                nome VARCHAR2(100) NOT NULL,
                idade NUMBER(3),
                descricao VARCHAR2(200),
                status VARCHAR2(30),
                CONSTRAINT pk_pacientes PRIMARY KEY (id)
            )
        """
        cursor.execute(sql)
        print(f'Tabela Pacientes criada com sucesso!')
    except oracledb.Error as e:
        # O erro -955 significa que a tabela já existe, o que não é um problema.
        if e.args[0].code == 955:
            print("Tabela 'pacientes' já existe.")
        else:
            print(f'Erro ao criar tabela: {e}')
    finally:
        if cursor:
            cursor.close()


def inserir_paciente(conn, nome, idade, descricao, status):
    print('*** Inserindo um novo paciente na tabela Pacientes ***')
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO pacientes (nome, idade, descricao, status) VALUES (:1, :2, :3, :4)"
        cursor.execute(sql, [nome, idade, descricao, status])
        conn.commit()
        print(f'Paciente {nome} adicionado com sucesso!')
    except oracledb.Error as e:
        print(f'\nErro ao inserir paciente: {e}')
        conn.rollback()
    finally:
        if cursor:
            cursor.close()


def inserir_multiplos_pacientes(conn):
    """Coleta dados de vários pacientes em uma matriz e os insere no banco de uma só vez."""
    print('*** Inserindo múltiplos pacientes ***')
    matriz_de_novos_pacientes = []

    while True:
        nome = input('Nome do paciente: ')
        try:
            idade = int(input('Idade: '))
            descricao = input('Descrição: ')
            status = input('Status: ')
            nova_linha = [nome, idade, descricao, status]
            matriz_de_novos_pacientes.append(nova_linha)
            print(f'Paciente {nome} adicionado à lista para inserção.:')
        except ValueError:
            print("Idade inválida. Por favor, insira um número inteiro.")
        while True:
            continuar = input('Deseja adicionar mais um paciente? [s/n] ').lower()
            if continuar == 'n':
                break
            elif continuar == 's':
                break
            else:
                print('Resposta inválida, responda "s" ou "n".')
        if continuar == 'n':
            break

    if not matriz_de_novos_pacientes:
        print("Nenhum paciente foi adicionado.")
        return

    print(f"\nInserindo {len(matriz_de_novos_pacientes)} pacientes no banco de dados...")
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO pacientes (nome, idade, descricao, status) VALUES (:1, :2, :3, :4)"
        cursor.executemany(sql, matriz_de_novos_pacientes)
        conn.commit()
        print("Todos os pacientes foram adicionados com sucesso!")
    except oracledb.Error as e:
        print(f'\nErro ao inserir múltiplos pacientes: {e}')
        conn.rollback()
    finally:
        if cursor:
            cursor.close()


def listar_pacientes(conn):
    try:
        cursor = conn.cursor()
        sql = "SELECT id, nome, idade, descricao, status FROM pacientes ORDER BY id"
        cursor.execute(sql)
        print("\n --- Lista de Pacientes ---")
        rows = cursor.fetchall()
        if not rows:
            print("Nenhum paciente cadastrado.")
        for row in rows:
            print(f'ID: {row[0]}, Nome: {row[1]}, Idade: {row[2]}, Descrição: {row[3]}, Status: {row[4]}')
        print('----------------------------------')
    except oracledb.Error as e:
        print(f'\nErro ao ler pacientes: {e}')
    finally:
        if cursor:
            cursor.close()


def atualizar_status_paciente(conn, id_paciente, novo_status):
    print(f'*** Atualizando o status de um paciente com base no ID ***')
    try:
        cursor = conn.cursor()
        sql = "UPDATE pacientes SET status = :novo_status WHERE id = :id_paciente"
        cursor.execute(sql, {'novo_status': novo_status, 'id_paciente': id_paciente})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'Status do paciente com ID {id_paciente} foi atualizado!')
        else:
            print(f'Nenhum paciente com ID {id_paciente} foi encontrado!')
    except oracledb.Error as e:
        print(f'\nErro ao atualizar o status: {e}')
        conn.rollback()
    finally:
        if cursor:
            cursor.close()


def deletar_paciente(conn, id_paciente):
    print(f'*** Excluindo o paciente de id: {id_paciente} ***')
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM pacientes WHERE id = :id_paciente"
        cursor.execute(sql, {'id_paciente': id_paciente})
        conn.commit()
        if cursor.rowcount > 0:
            print(f'Paciente com ID {id_paciente} foi excluído com sucesso!')
        else:
            print(f'Nenhum paciente com ID {id_paciente} foi encontrado para exclusão.')
    except oracledb.Error as e:
        print(f'Erro ao excluir paciente: {e}')
        conn.rollback()
    finally:
        if cursor:
            cursor.close()


def main():
    conn = get_conexao()
    if not conn:
        print("Falha na conexão. O programa será encerrado.")
        return

    criar_tabela(conn)

    while True:
        print(f'\n{"-" * 10} Menu de Pacientes {"-" * 10}')
        print('1 - Inserir um novo paciente')
        print('2 - Listar todos os pacientes')
        print('3 - Atualizar o status de um paciente')
        print('4 - Deletar um paciente')
        print('5 - Inserir múltiplos pacientes')
        print('6 - Sair')
        print("-" * 39)

        try:
            opcao = int(input('Escolha uma opção: '))

            if opcao == 1:
                nome = input('Nome do paciente: ')
                idade = int(input('Idade: '))
                descricao = input('Descrição: ')
                status = input('Status: ')
                inserir_paciente(conn, nome, idade, descricao, status)
            elif opcao == 2:
                listar_pacientes(conn)
            elif opcao == 3:
                listar_pacientes(conn)
                id_paciente = int(input('Digite o ID do paciente para atualizar: '))
                novo_status = input('Digite o novo status: ')
                atualizar_status_paciente(conn, id_paciente, novo_status)
            elif opcao == 4:
                listar_pacientes(conn)
                id_paciente = int(input('Digite o ID para remover: '))
                deletar_paciente(conn, id_paciente)
            elif opcao == 5:
                inserir_multiplos_pacientes(conn)
            elif opcao == 6:
                print('Saindo do programa...')
                break
            else:
                print('Opção inválida!')
        except ValueError:
            print(f'\nErro: Escolha uma das opções numéricas ou digite um número válido.')
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    if conn:
        conn.close()
        print('Conexão fechada.')


if __name__ == "__main__":
    main()