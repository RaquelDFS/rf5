class Projeto:
    def __init__(
        self,
        id=None,
        nome="",
        descricao="",
        status="iniciado",
        data_inicio=None,
        data_fim_prevista=None,
        data_formalizacao=None,
        id_responsavel=None,
        id_cliente=None
    ):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.status = status
        self.data_inicio = data_inicio
        self.data_fim_prevista = data_fim_prevista
        self.data_formalizacao = data_formalizacao
        self.id_responsavel = id_responsavel
        self.id_cliente = id_cliente

    def esta_iniciado(self):
        return self.status == "iniciado"

    def esta_em_aprovacao(self):
        return self.status == "em_aprovacao"

    def esta_aprovado(self):
        return self.status == "aprovado"

    def esta_concluido(self):
        return self.status == "concluido"

    def possui_cliente(self):
        return self.id_cliente is not None

    def possui_responsavel(self):
        return self.id_responsavel is not None

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "status": self.status,
            "data_inicio": self.data_inicio,
            "data_fim_prevista": self.data_fim_prevista,
            "data_formalizacao": self.data_formalizacao,
            "id_responsavel": self.id_responsavel,
            "id_cliente": self.id_cliente
        }

    def __str__(self):
        return f"{self.nome} - {self.status}"
