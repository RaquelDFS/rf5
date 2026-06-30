from services.usuario_service import UsuarioService


class UsuarioController:
    def __init__(self):
        self.service = UsuarioService()

    def listar(self):
        return self.service.listar()

    def listar_ativos(self):
        return self.service.listar_ativos()

    def listar_responsaveis_projeto(self):
        return self.service.listar_responsaveis_projeto()

    def listar_clientes(self):
        return self.service.listar_clientes()

    def listar_clientes_gestao(self):
        return self.service.listar_clientes_gestao()

    def buscar_cliente_por_id(self, id_cliente):
        return self.service.buscar_cliente_por_id(id_cliente)

    def buscar_por_id(self, id_usuario):
        return self.service.buscar_por_id(id_usuario)

    def cadastrar(self, nome, login, senha, funcao, email, empresa="", tipo_cliente="", documento=""):
        if not nome or not nome.strip():
            return False, "Informe o nome do usuário."

        if not login or not login.strip():
            return False, "Informe o login do usuário."

        if not senha or not senha.strip():
            return False, "Informe a senha do usuário."

        if not funcao or not funcao.strip():
            return False, "Informe a função/perfil do usuário."

        return self.service.cadastrar(
            nome=nome.strip(),
            login=login.strip(),
            senha=senha.strip(),
            funcao=funcao.strip(),
            email=email.strip() if email else "",
            empresa=empresa.strip() if empresa else "",
            tipo_cliente=tipo_cliente.strip() if tipo_cliente else "",
            documento=documento.strip() if documento else ""
        )

    def cadastrar_cliente(self, nome, login, senha, email, empresa="", tipo_cliente="", documento=""):
        if not nome or not nome.strip():
            return False, "Informe o nome do cliente."

        if not login or not login.strip():
            return False, "Informe o login do cliente."

        if not senha or not senha.strip():
            return False, "Informe a senha do cliente."

        return self.service.cadastrar_cliente(
            nome=nome.strip(),
            login=login.strip(),
            senha=senha.strip(),
            email=email.strip() if email else "",
            empresa=empresa.strip() if empresa else "",
            tipo_cliente=tipo_cliente.strip() if tipo_cliente else "",
            documento=documento.strip() if documento else ""
        )

    def atualizar(self, id_usuario, nome, login, funcao, email, ativo, empresa="", tipo_cliente="", documento=""):
        if not id_usuario:
            return False, "Usuário não informado."

        if not nome or not nome.strip():
            return False, "Informe o nome do usuário."

        if not login or not login.strip():
            return False, "Informe o login do usuário."

        if not funcao or not funcao.strip():
            return False, "Informe a função/perfil do usuário."

        return self.service.atualizar(
            id_usuario=id_usuario,
            nome=nome.strip(),
            login=login.strip(),
            funcao=funcao.strip(),
            email=email.strip() if email else "",
            ativo=ativo,
            empresa=empresa.strip() if empresa else "",
            tipo_cliente=tipo_cliente.strip() if tipo_cliente else "",
            documento=documento.strip() if documento else ""
        )

    def atualizar_cliente(self, id_cliente, nome, login, email, ativo, empresa="", tipo_cliente="", documento=""):
        if not id_cliente:
            return False, "Cliente não informado."

        if not nome or not nome.strip():
            return False, "Informe o nome do cliente."

        if not login or not login.strip():
            return False, "Informe o login do cliente."

        return self.service.atualizar_cliente(
            id_cliente=id_cliente,
            nome=nome.strip(),
            login=login.strip(),
            email=email.strip() if email else "",
            ativo=ativo,
            empresa=empresa.strip() if empresa else "",
            tipo_cliente=tipo_cliente.strip() if tipo_cliente else "",
            documento=documento.strip() if documento else ""
        )

    def desativar(self, id_usuario):
        if not id_usuario:
            return False, "Usuário não informado."

        return self.service.desativar(id_usuario)

    def desativar_cliente(self, id_cliente):
        if not id_cliente:
            return False, "Cliente não informado."

        return self.service.desativar_cliente(id_cliente)

    def autenticar(self, login, senha):
        if not login or not senha:
            return None

        return self.service.autenticar(login.strip(), senha.strip())

    def alterar_senha(self, id_usuario, nova_senha):
        if not id_usuario:
            return False, "Usuário não informado."

        if not nova_senha or not nova_senha.strip():
            return False, "Informe a nova senha."

        self.service.alterar_senha(id_usuario, nova_senha.strip())
        return True, "Senha alterada com sucesso."
