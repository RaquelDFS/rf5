from database import db
from models.usuario import Usuario


class UsuarioService:
    """Camada de serviço responsável pelas operações de usuários.

    Ela mantém o banco SQLite concentrado no database/db.py e transforma
    os registros retornados pelo banco em objetos Usuario quando necessário.
    """

    def listar(self):
        return db.listar_usuarios()

    def listar_ativos(self):
        return db.listar_usuarios_ativos()

    def listar_responsaveis_projeto(self):
        return db.listar_responsaveis_projeto()

    def listar_clientes(self):
        return db.listar_clientes()


    def buscar_cliente_por_id(self, id_cliente):
        return db.buscar_cliente_por_id(id_cliente)

    def buscar_por_id(self, id_usuario):
        registro = db.buscar_usuario_por_id(id_usuario)
        if not registro:
            return None

        return Usuario(
            id=registro[0],
            nome=registro[1],
            login=registro[2],
            funcao=registro[3],
            email=registro[4],
            ativo=registro[5]
        )

    def cadastrar(self, nome, login, senha, funcao, email):
        return db.cadastrar_usuario(nome, login, senha, funcao, email)

    def atualizar(self, id_usuario, nome, login, funcao, email, ativo):
        return db.atualizar_usuario(id_usuario, nome, login, funcao, email, ativo)

    def desativar(self, id_usuario):
        return db.desativar_usuario(id_usuario)

    def autenticar(self, login, senha):
        return db.autenticar_usuario(login, senha)

    def alterar_senha(self, id_usuario, nova_senha):
        return db.alterar_senha(id_usuario, nova_senha)
