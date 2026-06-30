from database import db
from models.usuario import Usuario


class UsuarioService:
    def listar(self):
        return db.listar_usuarios()

    def listar_ativos(self):
        return db.listar_usuarios_ativos()

    def listar_responsaveis_projeto(self):
        return db.listar_responsaveis_projeto()

    def listar_clientes(self):
        return db.listar_clientes()

    def listar_clientes_gestao(self):
        return db.listar_clientes_gestao()

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
            empresa=registro[5],
            tipo_cliente=registro[6],
            documento=registro[7],
            ativo=registro[8]
        )

    def cadastrar(self, nome, login, senha, funcao, email, empresa="", tipo_cliente="", documento=""):
        return db.cadastrar_usuario(
            nome,
            login,
            senha,
            funcao,
            email,
            empresa,
            tipo_cliente,
            documento
        )

    def cadastrar_cliente(self, nome, login, senha, email, empresa="", tipo_cliente="", documento=""):
        return db.cadastrar_cliente(
            nome,
            login,
            senha,
            email,
            empresa,
            tipo_cliente,
            documento
        )

    def atualizar(self, id_usuario, nome, login, funcao, email, ativo, empresa="", tipo_cliente="", documento=""):
        return db.atualizar_usuario(
            id_usuario,
            nome,
            login,
            funcao,
            email,
            ativo,
            empresa,
            tipo_cliente,
            documento
        )

    def atualizar_cliente(self, id_cliente, nome, login, email, ativo, empresa="", tipo_cliente="", documento=""):
        return db.atualizar_cliente(
            id_cliente,
            nome,
            login,
            email,
            ativo,
            empresa,
            tipo_cliente,
            documento
        )

    def desativar(self, id_usuario):
        return db.desativar_usuario(id_usuario)

    def desativar_cliente(self, id_cliente):
        return db.desativar_cliente(id_cliente)

    def autenticar(self, login, senha):
        return db.autenticar_usuario(login, senha)

    def alterar_senha(self, id_usuario, nova_senha):
        return db.alterar_senha(id_usuario, nova_senha)