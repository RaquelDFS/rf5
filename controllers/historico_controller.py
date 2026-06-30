from services.historico_service import HistoricoService


class HistoricoController:

    def __init__(self):
        self.service = HistoricoService()

    def registrar(self, tipo_entidade, id_entidade, id_usuario, acao, descricao):
        if not tipo_entidade:
            return False, "Tipo da entidade não informado."
        if not id_entidade:
            return False, "Entidade não informada."
        if not acao:
            return False, "Ação não informada."
        if not descricao:
            return False, "Descrição não informada."

        self.service.registrar(tipo_entidade, id_entidade, id_usuario, acao, descricao)
        return True, "Histórico registrado com sucesso."

    def listar_requisito(self, id_requisito):
        return self.service.listar_requisito(id_requisito)

    def listar_projeto(self, id_projeto):
        return self.service.listar_projeto(id_projeto)

    def listar_projeto_e_requisitos(self, id_projeto):
        return self.service.listar_projeto_e_requisitos(id_projeto)
