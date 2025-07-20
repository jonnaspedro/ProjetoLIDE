from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'inventario.db'

def init_db():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Inventario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hora TEXT,
                livro TEXT,
                observacoes TEXT,
                clube TEXT,
                data TEXT
            )
        ''')
        con.commit()

@app.route('/adicionar', methods=['POST'])
def adicionar_item():
    data = request.get_json()

    try:
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute('''
                INSERT INTO Inventario (
                    hora, livro, observacoes, clube, data
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                data.get('hora'),
                data.get('livro'),
                data.get('observacoes', ''),
                data.get('clube', ''),
                data.get('data')
            ))
            con.commit()
        return jsonify({"mensagem": "Item adicionado com sucesso"}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@app.route('/listar', methods=['GET'])
def listar():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Inventario")
        rows = cur.fetchall()
        col_names = [description[0] for description in cur.description]
        result = [dict(zip(col_names, row)) for row in rows]
        return jsonify(result)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)