# 📚 BookHub - Gerenciador de Biblioteca

Sistema acadêmico simples e elegante para gerenciamento de biblioteca, desenvolvido em Flask como projeto para disciplina de Banco de Dados.

## 📋 Visão Geral

BookHub é uma aplicação web que permite gerenciar um acervo de livros com funcionalidades completas de CRUD (Criar, Ler, Atualizar, Excluir) e sistema de autenticação de usuários. Desenvolvido com foco em simplicidade, organização e boas práticas de desenvolvimento.

### 🎯 Funcionalidades

#### 🔐 Autenticação
- Cadastro de novos usuários com validação
- Login seguro com senha hash
- Sessão gerenciada pelo Flask-Login
- Logout com encerramento de sessão

#### 📊 Dashboard
- Métricas gerais do acervo (total de livros, gêneros únicos)
- Últimos livros adicionados
- Links rápidos para ações principais

#### 📚 Gerenciamento de Livros
- **Listagem**: Visualização completa do acervo com ordenação alfabética
- **Pesquisa**: Busca por título, autor ou gênero (case-insensitive)
- **Cadastro**: Formulário com validações robustas
- **Edição**: Atualização de dados existentes
- **Exclusão**: Remoção segura com confirmação via modal

#### ✅ Validações Implementadas
- Campos obrigatórios (título, autor, gênero, ano)
- Formato de e-mail válido no cadastro
- Senha com mínimo de 6 caracteres
- Ano de publicação numérico (0 até ano atual)
- ISBN único (quando informado)

#### 🛡 Tratamento de Erros
- Operações de banco protegidas com try/except/rollback
- Páginas personalizadas 404 e 500
- Mensagens Flash amigáveis e informativas
- Recuperação automática de erros

## 🛠 Tecnologias Utilizadas

### Backend
- **Flask 3.1.3**: Framework web principal
- **SQLAlchemy 2.0.50**: ORM para manipulação do banco de dados
- **Flask-Login 0.6.3**: Gerenciamento de sessão e autenticação
- **Werkzeug 3.1.8**: Utilitários para segurança e hash de senhas

### Banco de Dados
- **PostgreSQL (Neon)**: Banco de dados recomendado (produção)
- **SQLite**: Banco para desenvolvimento local (opcional)
- **psycopg2-binary 2.9.12**: Driver PostgreSQL

### Frontend
- **Bootstrap 5.3.2**: Layout responsivo e componentes
- **Font Awesome 6.4.0**: Ícones e elementos visuais
- **Jinja2 3.1.6**: Sistema de templates

## 📁 Estrutura do Projeto

```
bookhub/
│
├── app.py                  # Aplicação principal (rotas, lógica de negócio)
├── config.py               # Configurações da aplicação
├── models.py               # Modelos SQLAlchemy (Usuário, Livro)
├── requirements.txt        # Dependências do projeto
├── .env                    # Variáveis de ambiente (não versionado)
├── .gitignore              # Arquivos ignorados pelo Git
│
├── README.md               # Documentação do projeto
│
└── templates/              # Templates Jinja2
    ├── base.html           # Layout base (navbar, footer)
    ├── login.html          # Página de login
    ├── cadastro.html       # Página de cadastro
    ├── dashboard.html      # Dashboard com métricas
    ├── livros.html         # Listagem com pesquisa
    ├── novo_livro.html     # Cadastro de livro
    ├── editar_livro.html   # Edição de livro
    ├── 404.html            # Página não encontrada
    └── 500.html            # Erro interno do servidor
```

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- PostgreSQL (Neon) ou SQLite

### Passo a Passo

#### 1. Clone o repositório
```bash
git clone https://github.com/viniciusF07/bookhub.git
cd bookhub
```

#### 2. Crie e ative um ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

#### 4. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

**Para produção (Neon):**
```env
# Banco de Dados PostgreSQL (Neon)
DATABASE_URL=postgresql://usuario:senha@ep-sua-instancia.region.aws.neon.tech/database

# Chave secreta (gere uma aleatória)
SECRET_KEY=sua_chave_secreta_aleatoria_aqui
```

**Para desenvolvimento (SQLite):**
```env
# Banco de Dados SQLite (local)
DATABASE_URL=sqlite:///bookhub.db

# Chave secreta (gere uma aleatória)
SECRET_KEY=sua_chave_secreta_aleatoria_aqui
```

> ⚠️ **Importante**: A `SECRET_KEY` deve ser uma string aleatória e única. Nunca compartilhe ou versionie o arquivo `.env`.

#### 5. Execute a aplicação
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

## 🗄 Modelos de Dados

### Usuário (`usuario`)
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | Integer | Identificador único | PRIMARY KEY |
| nome | String(100) | Nome completo | NOT NULL |
| email | String(150) | E-mail | UNIQUE, NOT NULL |
| senha_hash | String(256) | Senha em hash | NOT NULL |

### Livro (`livro`)
| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| id | Integer | Identificador único | PRIMARY KEY |
| titulo | String(200) | Título do livro | NOT NULL |
| autor | String(100) | Nome do autor | NOT NULL |
| genero | String(50) | Gênero literário | NOT NULL |
| ano_publicacao | Integer | Ano de publicação | NOT NULL |
| isbn | String(20) | Código ISBN | UNIQUE, NULL |

## 🔒 Autenticação e Segurança

### Funcionalidades
- **Cadastro**: Usuários criam conta com senha hasheada
- **Login**: Autenticação via e-mail e senha
- **Sessão**: Gerenciada com cookies seguros
- **Proteção**: Rotas protegidas com `@login_required`
- **Logout**: Encerramento seguro da sessão

### Medidas de Segurança
- Senhas armazenadas em hash (Werkzeug)
- Validação de entrada em todos os formulários
- Proteção contra SQL Injection (SQLAlchemy)
- Prevenção de XSS (escape automático do Jinja2)
- Exclusão segura via POST com confirmação

## 🔍 Pesquisa de Livros

A barra de pesquisa oferece busca inteligente:
- **Busca**: Título, autor ou gênero (case-insensitive)
- **Ordenação**: Resultados ordenados alfabeticamente por título
- **Feedback**: Contador de resultados e estado vazio informativo
- **Persistência**: Termo pesquisado é mantido após a busca
- **Limpeza**: Botão rápido para limpar a pesquisa

## 💡 Funcionalidades de UX

### Feedback ao Usuário
- ✅ Mensagens Flash com ícones (sucesso, erro, aviso, info)
- 🔄 Animações sutis nos cards (hover)
- 📊 Contadores visíveis em todas as listagens
- 🎯 Estados vazios com ações sugeridas

### Organização Visual
- 📱 Layout totalmente responsivo
- 🎨 Cores consistentes com feedback visual
- 🔘 Botões com ícones descritivos
- 📋 Tabelas limpas e organizadas

### Segurança nas Ações
- 🗑️ Exclusão com modal de confirmação
- ✏️ Campos validados com feedback imediato
- 🔒 Rotas protegidas contra acesso não autorizado

## 🐛 Tratamento de Erros

### Páginas Personalizadas
- **404**: Página não encontrada com links para navegação
- **500**: Erro interno com opção de recarregar

### Operações de Banco
- Try/except em todas as operações críticas
- Rollback automático em caso de erro
- Mensagens amigáveis para o usuário
- Logging de erros (via console)

### Validações
- Client-side: HTML5 (required, type, etc)
- Server-side: Validação completa no backend
- Mensagens de erro específicas por campo

## 📝 Exemplo de Uso

### 1. Cadastro de Usuário
```bash
# Acesse /cadastro
# Preencha: Nome, E-mail, Senha (mínimo 6 caracteres)
# Receba confirmação de cadastro
```

### 2. Login
```bash
# Acesse /login ou /
# Informe: E-mail e Senha cadastrados
# Redirecionado para Dashboard
```

### 3. Gerenciar Livros
```bash
# Dashboard: Veja métricas e últimos livros
# Acervo: Liste, pesquise, adicione, edite ou exclua livros
# Cada ação tem feedback visual imediato
```

## 🔧 Manutenção

### Recriar o Banco de Dados
```python
# No Python interativo ou em um script:
from app import app, db
with app.app_context():
    db.drop_all()
    db.create_all()
```

### Adicionar Dados de Teste
```python
# No Python interativo:
from app import app, db
from models import Livro

with app.app_context():
    livro = Livro(
        titulo="O Senhor dos Anéis",
        autor="J.R.R. Tolkien",
        genero="Fantasia",
        ano_publicacao=1954,
        isbn="978-0-618-57495-3"
    )
    db.session.add(livro)
    db.session.commit()
```

## 🤝 Contribuições

Este projeto é acadêmico e está aberto para contribuições que mantenham sua simplicidade e propósito educacional.

### Como Contribuir
1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature/melhoria`)
3. Commit suas alterações (`git commit -m 'Adiciona melhoria'`)
4. Push para a branch (`git push origin feature/melhoria`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é de uso acadêmico e está disponível para fins educacionais. Sinta-se livre para usá-lo como base para seus estudos.

## 🎯 Objetivos do Projeto

1. ✅ Demonstrar conceitos de CRUD com Flask
2. ✅ Implementar autenticação de usuários
3. ✅ Integrar com banco de dados PostgreSQL
4. ✅ Aplicar validações e tratamentos de erro
5. ✅ Manter código organizado e documentado
6. ✅ Prover UX agradável com Bootstrap
7. ✅ Servir como base para estudos de Banco de Dados

## 📚 Referências

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/)
- [Neon Database](https://neon.tech/docs)

---

**Desenvolvido para disciplina de Banco de Dados**
