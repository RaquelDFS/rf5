class Historico:
    def __init__(
        self,
        id=None,
        tipo_entidade="",
        id_entidade=None,
        id_usuario=None,
        acao="",
        descricao="",
        data_historico=None
    ):
        self.id = id
        self.tipo_entidade = tipo_entidade
        self.id_entidade = id_entidade
        self.id_usuario = id_usuario
        self.acao = acao
        self.descricao = descricao
        self.data_historico = data_historico

    def eh_historico_de_requisito(self):
        return self.tipo_entidade == "requisito"

    def eh_historico_de_projeto(self):
        return self.tipo_entidade == "projeto"

    def eh_historico_de_usuario(self):
        return self.tipo_entidade == "usuario"

    def to_dict(self):
        return {
            "id": self.id,
            "tipo_entidade": self.tipo_entidade,
            "id_entidade": self.id_entidade,
            "id_usuario": self.id_usuario,
            "acao": self.acao,
            "descricao": self.descricao,
            "data_historico": self.data_historico
        }

    def __str__(self):
        return f"{self.acao}: {self.descricao}"
