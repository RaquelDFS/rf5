from services.requisito_service import RequisitoService


class RequisitoController:

    def __init__(self):
        self.service = RequisitoService()

    def listar_todos(self):
        return self.service.listar_todos()

    def listar_por_projeto(self, projeto_id):
        return self.service.listar_por_projeto(projeto_id)

    def listar_cliente(self, id_cliente):
        return self.service.listar_cliente(id_cliente)

    def buscar_por_id(self, id_requisito):
        return self.service.buscar_por_id(id_requisito)

    def buscar_registro_por_id(self, id_requisito):
        return self.service.buscar_registro_por_id(id_requisito)

    def criar(self, projeto_id, nome, descricao, tipo, enviar_para_cliente=False):
        if not projeto_id:
            return False, "Selecione um projeto."
        if not nome or not nome.strip():
            return False, "Informe o nome do requisito."
        if not descricao or not descricao.strip():
            return False, "Informe a descrição do requisito."
        if not tipo or not tipo.strip():
            return False, "Selecione o tipo do requisito."

        if enviar_para_cliente:
            status = "aguardando_aprovacao"
            visivel_cliente = 1
        else:
            status = "em_analise"
            visivel_cliente = 0

        id_requisito = self.service.criar(
            projeto_id=projeto_id,
            nome=nome.strip(),
            descricao=descricao.strip(),
            tipo=tipo.strip(),
            status=status,
            visivel_cliente=visivel_cliente
        )

        return True, id_requisito

    def atualizar(self, id_requisito, nome, descricao, tipo, status, visivel_cliente):
        if not id_requisito:
            return False, "Requisito não informado."
        if not nome or not nome.strip():
            return False, "Informe o nome do requisito."
        if not descricao or not descricao.strip():
            return False, "Informe a descrição do requisito."
        if not tipo:
            return False, "Informe o tipo do requisito."
        if not status:
            return False, "Informe o status do requisito."

        self.service.atualizar(
            id_requisito=id_requisito,
            nome=nome.strip(),
            descricao=descricao.strip(),
            tipo=tipo,
            status=status,
            visivel_cliente=visivel_cliente
        )

        return True, "Requisito atualizado com sucesso."

    def atualizar_status(self, id_requisito, status):
        if not id_requisito:
            return False, "Requisito não informado."
        if not status:
            return False, "Status não informado."

        self.service.atualizar_status(id_requisito, status)
        return True, "Status atualizado com sucesso."

    def excluir(self, id_requisito):
        if not id_requisito:
            return False, "Requisito não informado."
        self.service.excluir(id_requisito)
        return True, "Requisito excluído com sucesso."
