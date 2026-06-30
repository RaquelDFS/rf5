from services.projeto_service import ProjetoService


class ProjetoController:

    def __init__(self):
        self.service = ProjetoService()

    def listar(self):
        return self.service.listar()

    def listar_por_usuario(self, id_usuario):
        return self.service.listar_por_usuario(id_usuario)

    def buscar_por_id(self, id_projeto):
        return self.service.buscar_por_id(id_projeto)

    def buscar_registro_por_id(self, id_projeto):
        return self.service.buscar_registro_por_id(id_projeto)

    def criar(self, nome, descricao, data_inicio, data_fim_prevista, id_responsavel, id_cliente):
        if not nome or not nome.strip():
            return False, "Informe o nome do projeto."
        if not descricao or not descricao.strip():
            return False, "Informe a descrição do projeto."
        if not data_inicio:
            return False, "Informe a data de início."
        if not data_fim_prevista:
            return False, "Informe a data fim prevista."
        if not id_responsavel:
            return False, "Selecione o responsável pelo projeto."
        if not id_cliente:
            return False, "Selecione o cliente do projeto."

        id_projeto = self.service.criar(
            nome=nome.strip(),
            descricao=descricao.strip(),
            data_inicio=str(data_inicio),
            data_fim_prevista=str(data_fim_prevista),
            id_responsavel=id_responsavel,
            id_cliente=id_cliente
        )

        return True, id_projeto

    def atualizar(self, id_projeto, nome, descricao, status, data_inicio, data_fim_prevista, id_responsavel, id_cliente=None):
        if not id_projeto:
            return False, "Projeto não informado."
        if not nome or not nome.strip():
            return False, "Informe o nome do projeto."
        if not descricao or not descricao.strip():
            return False, "Informe a descrição do projeto."
        if not status:
            return False, "Informe o status do projeto."
        if not id_responsavel:
            return False, "Selecione o responsável pelo projeto."

        self.service.atualizar(
            id_projeto=id_projeto,
            nome=nome.strip(),
            descricao=descricao.strip(),
            status=status,
            data_inicio=str(data_inicio),
            data_fim_prevista=str(data_fim_prevista),
            id_responsavel=id_responsavel,
            id_cliente=id_cliente
        )

        return True, "Projeto atualizado com sucesso."

    def registrar_formalizacao(self, id_projeto, data_formalizacao):
        if not id_projeto:
            return False, "Projeto não informado."
        self.service.registrar_formalizacao(id_projeto, data_formalizacao)
        return True, "Formalização registrada com sucesso."

    def excluir(self, id_projeto):
        if not id_projeto:
            return False, "Projeto não informado."
        self.service.excluir(id_projeto)
        return True, "Projeto excluído com sucesso."

    def listar_requisitos_completos(self, id_projeto):
        return self.service.listar_requisitos_completos(id_projeto)

    def listar_comentarios(self, id_projeto):
        return self.service.listar_comentarios(id_projeto)

    def listar_historico_completo(self, id_projeto):
        return self.service.listar_historico_completo(id_projeto)

    def listar_aprovacoes_reprovacoes(self, id_projeto):
        return self.service.listar_aprovacoes_reprovacoes(id_projeto)
