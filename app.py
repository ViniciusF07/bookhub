from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Usuario, Livro
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Configuração do Controle de Acesso (Flask-Login)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.login_message_category = "warning"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
        
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()
        
        # Validações
        erros = []
        
        if not nome:
            erros.append("O nome é obrigatório.")
        elif len(nome) < 3:
            erros.append("O nome deve ter pelo menos 3 caracteres.")
            
        if not email:
            erros.append("O e-mail é obrigatório.")
        elif "@" not in email or "." not in email:
            erros.append("Por favor, insira um e-mail válido.")
            
        if not senha:
            erros.append("A senha é obrigatória.")
        elif len(senha) < 6:
            erros.append("A senha deve ter pelo menos 6 caracteres.")
        
        if erros:
            for erro in erros:
                flash(erro, "danger")
            return render_template("cadastro.html", nome=nome, email=email)
        
        try:
            if Usuario.query.filter_by(email=email).first():
                flash("Este e-mail já está cadastrado.", "danger")
                return render_template("cadastro.html", nome=nome, email=email)

            novo_usuario = Usuario(nome=nome, email=email)
            novo_usuario.set_senha(senha)
            
            db.session.add(novo_usuario)
            db.session.commit()
            
            flash("Cadastro realizado com sucesso! Faça seu login.", "success")
            return redirect(url_for("login"))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar usuário: {str(e)}", "danger")
            return render_template("cadastro.html", nome=nome, email=email)

    return render_template("cadastro.html")

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()
        
        try:
            usuario = Usuario.query.filter_by(email=email).first()
            
            if usuario and usuario.verificar_senha(senha):
                login_user(usuario)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("dashboard"))
            else:
                flash("E-mail ou senha inválidos.", "danger")
        except Exception as e:
            flash(f"Erro ao realizar login: {str(e)}", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sessão.", "info")
    return redirect(url_for("login"))

# --- ROTAS DO SISTEMA (DASHBOARD & CRUD) ---

@app.route("/dashboard")
@login_required
def dashboard():
    try:
        total_livros = Livro.query.count()
        generos_lista = db.session.query(Livro.genero).distinct().all()
        total_generos = len(generos_lista)
        ultimos_livros = Livro.query.order_by(Livro.id.desc()).limit(3).all()

        return render_template(
            "dashboard.html", 
            total_livros=total_livros, 
            total_generos=total_generos,
            ultimos_livros=ultimos_livros
        )
    except Exception as e:
        flash(f"Erro ao carregar dashboard: {str(e)}", "danger")
        return render_template("dashboard.html", total_livros=0, total_generos=0, ultimos_livros=[])

@app.route("/livros")
@login_required
def listar_livros():
    termo_busca = request.args.get("q", "").strip()
    
    try:
        if termo_busca:
            livros = Livro.query.filter(
                (Livro.titulo.ilike(f"%{termo_busca}%")) |
                (Livro.autor.ilike(f"%{termo_busca}%")) |
                (Livro.genero.ilike(f"%{termo_busca}%"))
            ).order_by(Livro.titulo.asc()).all()
        else:
            livros = Livro.query.order_by(Livro.titulo.asc()).all()
            
        total_livros = len(livros)
        
        return render_template("livros.html", 
                             livros=livros, 
                             termo_busca=termo_busca,
                             total_livros=total_livros)
    except Exception as e:
        flash(f"Erro ao listar livros: {str(e)}", "danger")
        return render_template("livros.html", livros=[], termo_busca=termo_busca, total_livros=0)

@app.route("/livros/novo", methods=["GET", "POST"])
@login_required
def novo_livro():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        genero = request.form.get("genero", "").strip()
        ano_publicacao = request.form.get("ano_publicacao", "").strip()
        isbn = request.form.get("isbn", "").strip() or None
        
        # Validações
        erros = []
        
        if not titulo:
            erros.append("O título é obrigatório.")
        
        if not autor:
            erros.append("O autor é obrigatório.")
            
        if not genero:
            erros.append("O gênero é obrigatório.")
            
        if not ano_publicacao:
            erros.append("O ano de publicação é obrigatório.")
        else:
            try:
                ano = int(ano_publicacao)
                ano_atual = datetime.now().year
                if ano < 0 or ano > ano_atual:
                    erros.append(f"O ano deve estar entre 0 e {ano_atual}.")
            except ValueError:
                erros.append("O ano deve ser um número válido.")
        
        if isbn:
            try:
                isbn_existente = Livro.query.filter_by(isbn=isbn).first()
                if isbn_existente:
                    erros.append("Este ISBN já está cadastrado para outro livro.")
            except Exception:
                pass
        
        if erros:
            for erro in erros:
                flash(erro, "danger")
            return render_template("novo_livro.html", 
                                 titulo=titulo, autor=autor, genero=genero, 
                                 ano_publicacao=ano_publicacao, isbn=isbn)
        
        try:
            livro = Livro(
                titulo=titulo,
                autor=autor,
                genero=genero,
                ano_publicacao=int(ano_publicacao),
                isbn=isbn
            )
            db.session.add(livro)
            db.session.commit()
            flash("Livro cadastrado com sucesso!", "success")
            return redirect(url_for("listar_livros"))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar livro: {str(e)}", "danger")
            return render_template("novo_livro.html", 
                                 titulo=titulo, autor=autor, genero=genero, 
                                 ano_publicacao=ano_publicacao, isbn=isbn)

    return render_template("novo_livro.html")

@app.route("/livros/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_livro(id):
    try:
        livro = Livro.query.get_or_404(id)
    except Exception:
        flash("Livro não encontrado.", "danger")
        return redirect(url_for("listar_livros"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        genero = request.form.get("genero", "").strip()
        ano_publicacao = request.form.get("ano_publicacao", "").strip()
        isbn = request.form.get("isbn", "").strip() or None
        
        # Validações
        erros = []
        
        if not titulo:
            erros.append("O título é obrigatório.")
        
        if not autor:
            erros.append("O autor é obrigatório.")
            
        if not genero:
            erros.append("O gênero é obrigatório.")
            
        if not ano_publicacao:
            erros.append("O ano de publicação é obrigatório.")
        else:
            try:
                ano = int(ano_publicacao)
                ano_atual = datetime.now().year
                if ano < 0 or ano > ano_atual:
                    erros.append(f"O ano deve estar entre 0 e {ano_atual}.")
            except ValueError:
                erros.append("O ano deve ser um número válido.")
        
        if isbn:
            try:
                isbn_existente = Livro.query.filter(Livro.id != id, Livro.isbn == isbn).first()
                if isbn_existente:
                    erros.append("Este ISBN já está cadastrado para outro livro.")
            except Exception:
                pass
        
        if erros:
            for erro in erros:
                flash(erro, "danger")
            return render_template("editar_livro.html", livro=livro)
        
        try:
            livro.titulo = titulo
            livro.autor = autor
            livro.genero = genero
            livro.ano_publicacao = int(ano_publicacao)
            livro.isbn = isbn

            db.session.commit()
            flash("Livro atualizado com sucesso!", "success")
            return redirect(url_for("listar_livros"))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar livro: {str(e)}", "danger")
            return render_template("editar_livro.html", livro=livro)

    return render_template("editar_livro.html", livro=livro)

@app.route("/livros/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_livro(id):
    try:
        livro = Livro.query.get_or_404(id)
        db.session.delete(livro)
        db.session.commit()
        flash("Livro excluído com sucesso.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao excluir livro: {str(e)}", "danger")
    
    return redirect(url_for("listar_livros"))

# --- PÁGINAS DE ERRO ---

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def erro_interno(e):
    return render_template("500.html"), 500

# Inicializador facilitado do banco de dados
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)