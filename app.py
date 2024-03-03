from flask import Flask, request, jsonify, render_template_string
import mysql.connector
from mysql.connector import errorcode
import traceback
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def create_tables():
    conn = None
    try:
        conn = mysql.connector.connect(user='4NT', password='<h-<E[NdBe{j3[;e', host='4NT.mysql.pythonanywhere-services.com', database='muie')
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                pessoa VARCHAR(255),
                opcao VARCHAR(255),
                whatsapp VARCHAR(255),
                submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                error_message TEXT
            )
        """)
        conn.commit()
    except mysql.connector.Error as err:
        print("Error while connecting to MySQL", err)
    finally:
        if conn is not None:
            conn.close()

def log_error(error_message):
    conn = mysql.connector.connect(user='4NT', password='<h-<E[NdBe{j3[;e', host='4NT.mysql.pythonanywhere-services.com', database='muie')
    cursor = conn.cursor()
    query = "INSERT INTO error_logs (error_message) VALUES (%s)"
    cursor.execute(query, (error_message,))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/api/whatsapp', methods=['POST'])
def receber_whatsapp():
    try:
        data = request.get_json()
        pessoa = data['pessoa']
        opcao = data['opcao']
        whatsapp = data.get('whatsapp', '')
        conn = mysql.connector.connect(user='4NT', password='<h-<E[NdBe{j3[;e', host='4NT.mysql.pythonanywhere-services.com', database='muie')
        cursor = conn.cursor()
        
        query = "INSERT INTO submissions (pessoa, opcao, whatsapp) VALUES (%s, %s, %s)"
        cursor.execute(query, (pessoa, opcao, whatsapp))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"status": "success", "message": "Dados submetidos com sucesso!"})
    except Exception as e:
        error_message = traceback.format_exc()
        log_error(error_message)
        return jsonify({"status": "error", "message": "Houve um erro ao processar sua solicitação."})

@app.route('/ver-erros')
def view_errors():
    conn = mysql.connector.connect(user='4NT', password='<h-<E[NdBe{j3[;e', host='4NT.mysql.pythonanywhere-services.com', database='muie')
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM error_logs")
    error_logs = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    html = '''
    <h1>Logs de Erro</h1>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Mensagem de Erro</th>
        </tr>
        {% for error_log in error_logs %}
        <tr>
            <td>{{ error_log['id'] }}</td>
            <td>{{ error_log['error_message'] }}</td>
        </tr>
        {% endfor %}
    </table>
    '''
    
    return render_template_string(html, error_logs=error_logs)

@app.route('/ver-submissoes')
def view_submissions():
    conn = mysql.connector.connect(user='4NT', password='<h-<E[NdBe{j3[;e', host='4NT.mysql.pythonanywhere-services.com', database='muie')
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM submissions")
    submissions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    html = '''
    <h1>Submissões</h1>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Pessoa</th>
            <th>Opção</th>
            <th>WhatsApp</th>
            <th>Submetido em</th>
        </tr>
        {% for submission in submissions %}
        <tr>
            <td>{{ submission['id'] }}</td>
            <td>{{ submission['pessoa'] }}</td>
            <td>{{ submission['opcao'] }}</td>
            <td>{{ submission['whatsapp'] }}</td>
            <td>{{ submission['submitted_at'] }}</td>
        </tr>
        {% endfor %}
    </table>
    '''
    
    return render_template_string(html, submissions=submissions)

if __name__ == '__main__':
    with app.app_context():
        create_tables()
app.run(debug=True, host='0.0.0.0')
