import sqlite3


DATABASE_NAME = "sistema.db"


def conectar():
    return sqlite3.connect(DATABASE_NAME)



def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            login  TEXT    NOT NULL UNIQUE,
            senha  TEXT    NOT NULL,
            funcao TEXT    NOT NULL
        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projeto (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            nome              TEXT    NOT NULL,
            descricao         TEXT    NOT NULL,
            status            TEXT    NOT NULL DEFAULT 'iniciado' CHECK (
                                  status IN (
                                      'iniciado',
                                      'em_aprovacao',
                                      'aprovado',
                                      'em_construcao',
                                      'em_atraso',
                                      'em_revisao',
                                      'concluido',
                                      'suspenso',
                                      'cancelado'
                                  )
                              ),
            data_inicio       TEXT    NOT NULL,
            data_fim_prevista TEXT    NOT NULL,
            data_formalizacao TEXT,
            id_responsavel    INTEGER NOT NULL,
            id_cliente        INTEGER NOT NULL,

            FOREIGN KEY (id_responsavel)
                REFERENCES usuarios(id)
                ON DELETE RESTRICT,

            FOREIGN KEY (id_cliente)
                REFERENCES usuarios(id)
                ON DELETE RESTRICT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requisitos (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id          INTEGER NOT NULL,
            nome                TEXT    NOT NULL,
            descricao           TEXT    NOT NULL,
            tipo                TEXT    NOT NULL CHECK (
                                    tipo IN ('funcional', 'nao_funcional')
                                ),
            status              TEXT    NOT NULL DEFAULT 'em_analise' CHECK (
                                    status IN (
                                        'em_analise',
                                        'aguardando_aprovacao',
                                        'aprovado',
                                        'reprovado'
                                    )
                                ),
            visivel_cliente     INTEGER NOT NULL DEFAULT 1,

            FOREIGN KEY (projeto_id)
                REFERENCES projeto(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def criar_usuarios_padrao():
    conn = conectar()
    cursor = conn.cursor()

    usuarios = [
        ("raquel",  "123",    "analista"),
        ("Wallace", "123456", "cliente"),
        ("Caio",    "123456", "cliente")
    ]

    for usuario in usuarios:
        cursor.execute("""
            INSERT OR IGNORE INTO usuarios (login, senha, funcao)
            VALUES (?, ?, ?)
        """, usuario)

    conn.commit()
    conn.close()


def autenticar_usuario(login, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, login, funcao
        FROM usuarios
        WHERE login = ? AND senha = ?
    """, (login, senha))

    usuario = cursor.fetchone()

    conn.close()

    return usuario


def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, login
        FROM usuarios
        WHERE funcao = 'cliente'
        ORDER BY login
    """)

    clientes = cursor.fetchall()

    conn.close()

    return clientes


def buscar_cliente_por_id(id_cliente):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, login, funcao
        FROM usuarios
        WHERE id = ?
    """, (id_cliente,))

    cliente = cursor.fetchone()

    conn.close()

    return cliente


def alterar_senha(id_usuario, nova_senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET senha = ?
        WHERE id = ?
    """, (nova_senha, id_usuario))

    conn.commit()
    conn.close()


def criar_projeto(
    nome,
    descricao,
    data_inicio,
    data_fim_prevista,
    id_responsavel,
    id_cliente
):
    """
    Cria um novo projeto vinculando um responsável (analista/gerente)
    e um cliente. O status inicial é sempre 'iniciado'.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO projeto (
            nome,
            descricao,
            status,
            data_inicio,
            data_fim_prevista,
            id_responsavel,
            id_cliente
        )
        VALUES (?, ?, 'iniciado', ?, ?, ?, ?)
    """, (
        nome,
        descricao,
        data_inicio,
        data_fim_prevista,
        id_responsavel,
        id_cliente
    ))

    conn.commit()
    conn.close()


def listar_projetos():
    """
    Retorna todos os projetos. Uso exclusivo do Gerente.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.nome,
            p.descricao,
            p.status,
            p.data_inicio,
            p.data_fim_prevista,
            p.data_formalizacao,
            resp.login AS responsavel,
            cli.login  AS cliente
        FROM projeto p
        INNER JOIN usuarios resp ON resp.id = p.id_responsavel
        INNER JOIN usuarios cli  ON cli.id  = p.id_cliente
        ORDER BY p.id DESC
    """)

    projetos = cursor.fetchall()

    conn.close()

    return projetos


def listar_projetos_por_usuario(id_usuario):
    """
    Retorna os projetos em que o usuário é responsável ou cliente.
    Cobre o analista (id_responsavel) e o cliente (id_cliente).
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.nome,
            p.descricao,
            p.status,
            p.data_inicio,
            p.data_fim_prevista
        FROM projeto p
        WHERE p.id_responsavel = ?
           OR p.id_cliente = ?
        ORDER BY p.id DESC
    """, (id_usuario, id_usuario))

    projetos = cursor.fetchall()

    conn.close()

    return projetos


def buscar_projeto_por_id(id_projeto):
    """
    Retorna todos os dados de um projeto, incluindo
    login do responsável e do cliente vinculado.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.nome,
            p.descricao,
            p.status,
            p.data_inicio,
            p.data_fim_prevista,
            p.data_formalizacao,
            p.id_responsavel,
            p.id_cliente,
            resp.login AS responsavel,
            cli.login  AS cliente
        FROM projeto p
        INNER JOIN usuarios resp ON resp.id = p.id_responsavel
        INNER JOIN usuarios cli  ON cli.id  = p.id_cliente
        WHERE p.id = ?
    """, (id_projeto,))

    projeto = cursor.fetchone()

    conn.close()

    return projeto


def atualizar_projeto(
    id_projeto,
    nome,
    descricao,
    status,
    data_inicio,
    data_fim_prevista
):
    """
    Atualiza os campos editáveis do projeto.
    id_responsavel, id_cliente e data_formalizacao
    não são alterados por esta função.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE projeto
        SET
            nome              = ?,
            descricao         = ?,
            status            = ?,
            data_inicio       = ?,
            data_fim_prevista = ?
        WHERE id = ?
    """, (
        nome,
        descricao,
        status,
        data_inicio,
        data_fim_prevista,
        id_projeto
    ))

    conn.commit()
    conn.close()


def registrar_formalizacao(id_projeto, data_formalizacao):
    """
    Preenchida automaticamente pelo sistema quando o PDF
    de formalização é gerado. Também fecha o status em 'aprovado'.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE projeto
        SET
            data_formalizacao = ?,
            status            = 'aprovado'
        WHERE id = ?
    """, (data_formalizacao, id_projeto))

    conn.commit()
    conn.close()


def excluir_projeto(id_projeto):
    """
    Exclui um projeto. Permitido apenas para o Gerente.
    O controle de permissão deve ser feito na camada de interface.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM projeto
        WHERE id = ?
    """, (id_projeto,))

    conn.commit()
    conn.close()


def _buscar_id_cliente_do_projeto(cursor, projeto_id):
    """
    Função interna. Busca o id_cliente vinculado ao projeto.
    Usada por criar_requisito para herdar o cliente automaticamente.
    """
    cursor.execute("""
        SELECT id_cliente
        FROM projeto
        WHERE id = ?
    """, (projeto_id,))

    resultado = cursor.fetchone()

    if resultado is None:
        raise ValueError(f"Projeto com id {projeto_id} não encontrado.")

    return resultado[0]


def criar_requisito(
    projeto_id,
    nome,
    descricao,
    tipo,
    visivel_cliente=1
):
    """
    Cria um requisito vinculado ao projeto.
    O cliente é herdado automaticamente do projeto —
    o analista não precisa informá-lo.
    """
    conn = conectar()
    cursor = conn.cursor()

    # Valida se o projeto existe antes de inserir
    _buscar_id_cliente_do_projeto(cursor, projeto_id)

    cursor.execute("""
        INSERT INTO requisitos (
            projeto_id,
            nome,
            descricao,
            tipo,
            visivel_cliente
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        projeto_id,
        nome,
        descricao,
        tipo,
        visivel_cliente
    ))

    conn.commit()
    conn.close()


def listar_todos_requisitos():
    """
    Retorna todos os requisitos com o cliente herdado do projeto.
    Uso do Gerente e Analista.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.nome,
            r.descricao,
            r.tipo,
            r.status,
            r.visivel_cliente,
            p.nome    AS projeto,
            cli.login AS cliente
        FROM requisitos r
        INNER JOIN projeto  p   ON p.id   = r.projeto_id
        INNER JOIN usuarios cli ON cli.id = p.id_cliente
        ORDER BY r.id DESC
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados


def listar_requisitos_por_projeto(projeto_id):
    """
    Retorna todos os requisitos de um projeto específico.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.nome,
            r.descricao,
            r.tipo,
            r.status,
            r.visivel_cliente
        FROM requisitos r
        WHERE r.projeto_id = ?
        ORDER BY r.id DESC
    """, (projeto_id,))

    requisitos = cursor.fetchall()

    conn.close()

    return requisitos


def listar_requisitos_cliente(id_cliente):
    """
    Retorna os requisitos visíveis para um cliente específico,
    buscando via projeto ao qual ele está vinculado.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.nome,
            r.descricao,
            r.tipo,
            r.status
        FROM requisitos r
        INNER JOIN projeto p ON p.id = r.projeto_id
        WHERE p.id_cliente = ?
        AND r.visivel_cliente = 1
        ORDER BY r.id DESC
    """, (id_cliente,))

    requisitos = cursor.fetchall()

    conn.close()

    return requisitos


def buscar_requisito_por_id(id_requisito):
    """
    Retorna os dados de um requisito com o cliente herdado do projeto.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.id,
            r.nome,
            r.descricao,
            r.tipo,
            r.status,
            r.visivel_cliente,
            r.projeto_id,
            p.id_cliente,
            cli.login AS cliente
        FROM requisitos r
        INNER JOIN projeto  p   ON p.id   = r.projeto_id
        INNER JOIN usuarios cli ON cli.id = p.id_cliente
        WHERE r.id = ?
    """, (id_requisito,))

    requisito = cursor.fetchone()

    conn.close()

    return requisito


def atualizar_requisito(
    id_requisito,
    nome,
    descricao,
    tipo,
    status,
    visivel_cliente
):
    """
    Atualiza os campos editáveis de um requisito.
    O projeto_id não pode ser alterado após a criação.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE requisitos
        SET
            nome            = ?,
            descricao       = ?,
            tipo            = ?,
            status          = ?,
            visivel_cliente = ?
        WHERE id = ?
    """, (
        nome,
        descricao,
        tipo,
        status,
        visivel_cliente,
        id_requisito
    ))

    conn.commit()
    conn.close()


def excluir_requisito(id_requisito):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM requisitos
        WHERE id = ?
    """, (id_requisito,))

    conn.commit()
    conn.close()


# def inserir_requisitos_teste():
    """
    Insere requisitos de teste apenas se o banco estiver vazio
    e se existir ao menos um projeto cadastrado.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM requisitos")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    cursor.execute("SELECT id FROM projeto LIMIT 1")
    projeto = cursor.fetchone()

    if projeto is None:
        conn.close()
        return

    projeto_id = projeto[0]

    requisitos = [
        ("Tela de Login",          "Permitir autenticação utilizando usuário e senha.",              "funcional",    "aprovado",             projeto_id, 1),
        ("Recuperação de Senha",   "Permitir redefinição de senha através de e-mail.",               "funcional",    "aguardando_aprovacao",  projeto_id, 1),
        ("Dashboard Financeiro",   "Exibir indicadores financeiros e gráficos de desempenho.",       "funcional",    "em_analise",            projeto_id, 0),
        ("Tempo de Resposta",      "As páginas devem carregar em até 2 segundos.",                   "nao_funcional","aprovado",              projeto_id, 1),
        ("Exportação para PDF",    "Permitir exportação dos relatórios em formato PDF.",             "funcional",    "reprovado",             projeto_id, 1),
        ("Controle de Permissões", "Permitir acesso às funcionalidades conforme perfil do usuário.", "funcional",    "em_analise",            projeto_id, 0),
    ]

    cursor.executemany("""
        INSERT INTO requisitos (
            nome,
            descricao,
            tipo,
            status,
            projeto_id,
            visivel_cliente
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, requisitos)

    conn.commit()
    conn.close()



def inicializar_banco():
    criar_tabelas()
    criar_usuarios_padrao()