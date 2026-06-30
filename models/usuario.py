class Usuario:
    def __init__(self, id=None, nome="", login="", senha="", funcao="", email="", empresa="", tipo_cliente="", documento="", ativo=1):
        self.id = id
        self.nome = nome
        self.login = login
        self.senha = senha
        self.funcao = funcao
        self.email = email
        self.empresa = empresa
        self.tipo_cliente = tipo_cliente
        self.documento = documento
        self.ativo = ativo

    def esta_ativo(self):
        return self.ativo == 1

    def eh_gerente(self):
        return self.funcao == "gerente"

    def eh_analista(self):
        return self.funcao == "analista"

    def eh_desenvolvedor(self):
        return self.funcao == "desenvolvedor"

    def eh_testador(self):
        return self.funcao == "testador"

    def eh_cliente(self):
        return self.funcao == "cliente"

    def pode_gerenciar_usuarios(self):
        return self.eh_gerente()

    def pode_cadastrar_projeto(self):
        return self.funcao in ["gerente", "analista"]

    def pode_cadastrar_requisito(self):
        return self.funcao in ["gerente", "analista"]

    def pode_comentar_requisito(self):
        return self.funcao in ["gerente", "analista", "desenvolvedor", "testador", "cliente"]

    def pode_aprovar_requisito(self):
        return self.eh_cliente()

    def nome_exibicao_cliente(self):
        if self.empresa:
            return self.empresa
        return self.nome

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "login": self.login,
            "senha": self.senha,
            "funcao": self.funcao,
            "email": self.email,
            "empresa": self.empresa,
            "tipo_cliente": self.tipo_cliente,
            "documento": self.documento,
            "ativo": self.ativo
        }

    def __str__(self):
        return f"{self.nome} ({self.funcao})"
