class Requisito:
    def __init__(
        self,
        id=None,
        projeto_id=None,
        nome="",
        descricao="",
        tipo="",
        status="em_analise",
        visivel_cliente=0
    ):
        self.id = id
        self.projeto_id = projeto_id
        self.nome = nome
        self.descricao = descricao
        self.tipo = tipo
        self.status = status
        self.visivel_cliente = visivel_cliente

    def eh_funcional(self):
        return self.tipo == "funcional"

    def eh_nao_funcional(self):
        return self.tipo == "nao_funcional"

    def esta_em_analise(self):
        return self.status == "em_analise"

    def esta_aguardando_aprovacao(self):
        return self.status == "aguardando_aprovacao"

    def esta_aprovado(self):
        return self.status == "aprovado"

    def esta_reprovado(self):
        return self.status == "reprovado"

    def esta_concluido(self):
        return self.status == "concluido"

    def esta_visivel_para_cliente(self):
        return self.visivel_cliente == 1

    def pode_ser_avaliado_pelo_cliente(self):
        return self.esta_aguardando_aprovacao() and self.esta_visivel_para_cliente()

    def to_dict(self):
        return {
            "id": self.id,
            "projeto_id": self.projeto_id,
            "nome": self.nome,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "status": self.status,
            "visivel_cliente": self.visivel_cliente
        }

    def __str__(self):
        return f"{self.nome} - {self.status}"
