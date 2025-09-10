from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inscricoes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'segredo_LIDE'

class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    primeiro_nome = db.Column(db.String(30), nullable = False)
    ultimo_nome = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    cidade = db.Column(db.String(100), nullable = False)
    estado = db.Column(db.String(2), nullable = False)

@app.route("/")
def materiais():
    return render_template("materiais.html")

@app.route("/inscrever", methods=["post"])
def inscrever():
    primeiro_nome = request.form["primeiro_nome"]
    ultimo_nome = request.form["ultimo_nome"]
    email = request.form["email"]
    cidade = request.form["cidade"]
    estado = request.form["estado"]
    acao = request.form["acao"]
    nome_completo = f"{primeiro_nome} {ultimo_nome}"

    if acao == "inscrever":
        #BANCO DE DADOS AQUI
        nova_inscricao = Inscricao (
            primeiro_nome = primeiro_nome,
            ultimo_nome = ultimo_nome,
            email = email,
            cidade = cidade,
            estado = estado)
        db.session.add(nova_inscricao)
        db.session.commit()

        enviar_email_pdf(email, primeiro_nome)
        flash("Inscrição realizada com sucesso! Verifique sua caixa de entrada.")
    
    elif acao == "cancelar":
        #BANCO DE DADOS AQUI
        inscricao = Inscricao.query.filter_by(email=email).first()
        if inscricao:
                db.session.delete(inscricao)
                db.session.commit()
        flash("Sua inscrição foi cancelada. Você não receberá mais e-mails.")
    
    return redirect(url_for("materiais"))

def enviar_email_pdf(dest, nome):
    #BANCO DE DADOS AQUI
    remetente = "lss52@discente.ifpe.edu.br"
    senha = "xluf wwwu isxg ehkg"

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = dest
    msg["Subject"] = "Bem-vindo(a) ao Projeto LIDE!"

    body = f"""
    Olá, {nome}!
    
    Obrigado por se inscrever no Projeto LIDE.
    Em breve, você receberá mais materiais exclusivos!

    Atenciosamente,
    Equipe LIDE.
    """

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remetente, senha)
            servidor.send_message(msg)
        print("E-mail enviado com sucesso.")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)



#funçoes de listar

@app.route("/listar")
def listar_todoMundo():
    chave_acesso = request.args.get("chave_acesso")
    if chave_acesso != "segredo_LIDE":
        return "Acesso negado!", 403
    
    inscritos = Inscricao.query.all()
    return render_template("listar.html", inscritos = inscritos)


@app.route("/inscrito")
def buscar_email():
    email = request.args.get("email")
    inscrito = Inscricao.query.filter_by(email = email).first()

    if not inscrito:
        return f"Nenhuma pessoa cadastrada com eo email: {email}"
    return render_template("inscrito.html", inscrito = inscrito)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() #cria o banco e a tabela, pfvr nn mexer
    app.run(host="0.0.0.0", port=5502, debug=True)