import json
import requests
from banco import insere_usuario, recupera_usuarios, atualiza_usuario, exclui_usuario

# Lista para armazenar os dados do usuário
usuarios = []

# Função para carregar usuários de um arquivo JSON 
def carregar_usuarios():
    global usuarios
    try:
        with open("usuarios.json", "r") as file:
            usuarios = json.load(file)
            print("Dados carregados com sucesso!")
    except (FileNotFoundError, json.JSONDecodeError):
        print("Nenhum dado existente encontrado. Iniciando com lista vazia.")

# Função para salvar usuários em um arquivo JSON
def salvar_usuarios():
    try:
        with open("usuarios.json", "w") as file:
            json.dump(usuarios, file, indent=4)
            print("Dados salvos com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar dados: {e}")

# Função para exportar usuários para um arquivo JSON
def exportar_usuarios_para_json():
    global usuarios
    if not usuarios:
        print("Nenhum usuário disponível para exportar.")
        return
    try:
        with open("usuarios_exportados.json", "w") as file:
            json.dump(usuarios, file, indent=4)
            print("Usuários exportados para 'usuarios_exportados.json' com sucesso!")
    except IOError as e:
        print(f"Erro ao exportar dados: {e}")

# Função para obter endereço com base no CEP usando a API ViaCEP
def obter_endereco(cep):
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        data = response.json()
        if "erro" not in data:
            return {
                "logradouro": data["logradouro"],
                "numero": input("Digite o número da residência: "),
                "complemento": input("Digite o complemento (opcional): "),
                "bairro": data["bairro"],
                "cidade": data["localidade"],
                "estado": data["uf"],
                "cep": data["cep"]
            }
        else:
            print("CEP não encontrado.")
            return None
    except requests.RequestException as e:
        print("Erro de conexão:", e)
        return None

# Função para cadastrar usuário
def cadastrar_usuario():
    try:
        nome = input("Digite seu nome: ")
        cpf = input("Digite seu CPF: ")
        telefone = input("Digite seu telefone: ")
        email = input("Digite seu email: ")
        marca = input("Digite a marca do veículo: ")
        modelo = input("Digite o modelo do veículo: ")
        ano = input("Digite o ano do veículo: ")
        placa = input("Digite a placa do veículo: ")
        descricao = input("Digite uma descrição do seu problema: ")

        while True:
            cep = input("Digite seu CEP: ")
            endereco = obter_endereco(cep)
            if endereco is not None:
                break  
            else:
                print("Por favor, tente novamente ou digite 'sair' para cancelar.")
                opcao = input("Deseja tentar novamente? (sim/sair): ").lower()
                if opcao == 'sair':
                    print("Operação cancelada.")
                    return 

        usuario = {
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone,
            "email": email,
            "marca": marca,
            "modelo": modelo,
            "ano": ano,
            "placa": placa,
            "descricao": descricao,
            **endereco
        }
        insere_usuario(usuario)
        usuarios.append(usuario)  
        print("Cadastro realizado com sucesso!")
    except ValueError as e:
        print(f"Erro no cadastro: {e}")

# Função para listar usuários
def listar_usuarios():
    global usuarios
    usuarios.clear()  
    usuarios.extend(recupera_usuarios())  
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        for idx, usuario in enumerate(usuarios, start=1):
            print(f"{idx}. Nome: {usuario[1]}, CPF: {usuario[2]}, Telefone: {usuario[3]}, Email: {usuario[4]}, Placa: {usuario[8]}, Cidade: {usuario[13]}, Estado: {usuario[14]}")

# Função para atualizar usuário
def atualizar_usuario_menu():
    listar_usuarios()
    try:
        idx = int(input("Selecione o número do usuário que deseja atualizar: ")) - 1
        if 0 <= idx < len(usuarios):
            id_usuario = usuarios[idx][0] 
            novo_nome = input(f"Novo nome ({usuarios[idx][1]}): ") or usuarios[idx][1]
            novo_cpf = input(f"Novo CPF ({usuarios[idx][2]}): ") or usuarios[idx][2]
            novo_telefone = input(f"Novo telefone ({usuarios[idx][3]}): ") or usuarios[idx][3]
            novo_email = input(f"Novo email ({usuarios[idx][4]}): ") or usuarios[idx][4]
            novo_marca = input(f"Nova marca ({usuarios[idx][5]}): ") or usuarios[idx][5]
            novo_modelo = input(f"Novo modelo ({usuarios[idx][6]}): ") or usuarios[idx][6]
            novo_ano = input(f"Novo ano ({usuarios[idx][7]}): ") or usuarios[idx][7]
            novo_placa = input(f"Nova placa ({usuarios[idx][8]}): ") or usuarios[idx][8]
            nova_descricao = input(f"Nova descrição ({usuarios[idx][9]}): ") or usuarios[idx][9]
            
            usuario_atualizado = {
                "id": id_usuario,
                "nome": novo_nome,
                "cpf": novo_cpf,
                "telefone": novo_telefone,
                "email": novo_email,
                "marca": novo_marca,
                "modelo": novo_modelo,
                "ano": novo_ano,
                "placa": novo_placa,
                "descricao": nova_descricao,
                "logradouro": usuarios[idx][10],
                "numero": usuarios[idx][11],
                "complemento": usuarios[idx][12],
                "bairro": usuarios[idx][13],
                "cidade": usuarios[idx][14],
                "estado": usuarios[idx][15],
                "cep": usuarios[idx][16]
            }
            atualiza_usuario(usuario_atualizado)
            print("Usuário atualizado com sucesso!")
        else:
            print("Usuário não encontrado.")
    except (ValueError, IndexError):
        print("Entrada inválida.")

# Função para excluir usuário
def excluir_usuario():
    listar_usuarios()
    try:
        idx = int(input("Selecione o número do usuário que deseja excluir: ")) - 1
        if 0 <= idx < len(usuarios):
            id_usuario = usuarios[idx][0]
            exclui_usuario(id_usuario)
            print("Usuário excluído com sucesso!")
        else:
            print("Usuário não encontrado.")
    except (ValueError, IndexError):
        print("Entrada inválida.")

# Função de cadastro de usuário
def cadastro_usuario():
    while True:
        print("\n--- CADASTRO DO USUÁRIO ---")
        print("1. Cadastrar Usuário")
        print("2. Listar Usuários")
        print("3. Atualizar Usuário")
        print("4. Excluir Usuário")
        print("5. Exportar Usuários para JSON")
        print("6. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            listar_usuarios()
        elif opcao == '3':
            atualizar_usuario_menu()
        elif opcao == '4':
            excluir_usuario()
        elif opcao == '5':
            exportar_usuarios_para_json()
        elif opcao == '6':
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    carregar_usuarios()
    cadastro_usuario()
