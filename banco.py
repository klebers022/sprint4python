import oracledb

def get_conexao():
    return oracledb.connect(user="rm557887", password="210106",
                            dsn="oracle.fiap.com.br/orcl")

def insere_usuario(usuario: dict):
    sql = """
    INSERT INTO tbj_usuarios (nome, cpf, telefone, email, marca, modelo, ano, placa, descricao, logradouro, numero, complemento, bairro, cidade, estado, cep)
    VALUES (:nome, :cpf, :telefone, :email, :marca, :modelo, :ano, :placa, :descricao, :logradouro, :numero, :complemento, :bairro, :cidade, :estado, :cep)
    """
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, usuario)
        con.commit()

def recupera_usuario(id: int):
    sql = "SELECT * FROM tbj_usuarios WHERE id = :id"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"id": id})
            return cur.fetchone()

def recupera_usuarios():
    sql = "SELECT * FROM tbj_usuarios"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

def atualiza_usuario(usuario: dict):
    sql = """
    UPDATE tbj_usuarios
    SET nome = :nome, cpf = :cpf, telefone = :telefone, email = :email,
        marca = :marca, modelo = :modelo, ano = :ano, placa = :placa, descricao = :descricao,
        logradouro = :logradouro, numero = :numero, complemento = :complemento,
        bairro = :bairro, cidade = :cidade, estado = :estado, cep = :cep
    WHERE id = :id
    """
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, usuario)
        con.commit()

def exclui_usuario(id: int):
    sql = "DELETE FROM tbj_usuarios WHERE id = :id"
    with get_conexao() as con:
        with con.cursor() as cur:
            cur.execute(sql, {"id": id})
        con.commit()
