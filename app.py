from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication  # pra quando for usar o PDF

app = Flask(__name__)
app.secret_key = 'segredo_LIDE'

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
        print(f"Inserir no banco: {nome_completo} - {email} - {cidade}/{estado}")
        enviar_email_pdf(email, primeiro_nome)
        flash("Inscrição realizada com sucesso! Verifique sua caixa de entrada.")
    
    elif acao == "cancelar":
        #BANCO DE DADOS AQUI
        print(f"Remover do banco: {email}")
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5502, debug=True)