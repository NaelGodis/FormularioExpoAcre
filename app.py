from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import csv
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

# Configurações
CSV_FILE = 'respostas.csv'
JSON_FILE = 'respostas.json'

# Cabeçalhos do CSV
CSV_HEADERS = [
    'timestamp',
    'atividade_desejada',
    'pagaria',
    'valor_justo',
    'ja_teve_aula',
    'como_encontrar',
    'comentarios'
]

def init_csv_file():
    """Inicializa o arquivo CSV com cabeçalhos se não existir"""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADERS)

def init_json_file():
    """Inicializa o arquivo JSON se não existir"""
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'w', encoding='utf-8') as file:
            json.dump([], file, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """Serve a página principal"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve arquivos estáticos (CSS, JS, etc.)"""
    return send_from_directory('.', filename)

@app.route('/submit', methods=['POST'])
def submit_response():
    """Recebe e salva as respostas do questionário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Valida campos obrigatórios
        required_fields = ['atividade_desejada', 'pagaria', 'valor_justo', 'ja_teve_aula']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Campo obrigatório ausente: {field}'}), 400
        
        # Prepara os dados para salvar
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Converte lista de checkboxes para string
        como_encontrar = data.get('como_encontrar', [])
        if isinstance(como_encontrar, list):
            como_encontrar_str = '; '.join(como_encontrar)
        else:
            como_encontrar_str = como_encontrar
        
        # Dados para CSV
        csv_row = [
            timestamp,
            data.get('atividade_desejada', ''),
            data.get('pagaria', ''),
            data.get('valor_justo', ''),
            data.get('ja_teve_aula', ''),
            como_encontrar_str,
            data.get('comentarios', '')
        ]
        
        # Salva no CSV
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(csv_row)
        
        # Salva no JSON (formato mais estruturado)
        json_data = {
            'timestamp': timestamp,
            'atividade_desejada': data.get('atividade_desejada', ''),
            'pagaria': data.get('pagaria', ''),
            'valor_justo': data.get('valor_justo', ''),
            'ja_teve_aula': data.get('ja_teve_aula', ''),
            'como_encontrar': como_encontrar,
            'comentarios': data.get('comentarios', '')
        }
        
        # Lê o arquivo JSON existente
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []
        
        # Adiciona nova resposta
        existing_data.append(json_data)
        
        # Salva de volta no JSON
        with open(JSON_FILE, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=2)
        
        print(f"Nova resposta salva: {json_data}")
        
        return jsonify({
            'success': True,
            'message': 'Resposta salva com sucesso',
            'total_responses': len(existing_data)
        })
        
    except Exception as e:
        print(f"Erro ao salvar resposta: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/responses')
def get_responses():
    """Endpoint para visualizar todas as respostas (opcional)"""
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify({
            'total': len(data),
            'responses': data
        })
    except FileNotFoundError:
        return jsonify({
            'total': 0,
            'responses': []
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/csv')
def download_csv():
    """Endpoint para download do arquivo CSV"""
    try:
        return send_from_directory('.', CSV_FILE, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo CSV não encontrado'}), 404

@app.route('/download/json')
def download_json():
    """Endpoint para download do arquivo JSON"""
    try:
        return send_from_directory('.', JSON_FILE, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'Arquivo JSON não encontrado'}), 404

@app.route('/stats')
def get_stats():
    """Endpoint para estatísticas básicas"""
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        total = len(data)
        if total == 0:
            return jsonify({'total': 0, 'stats': {}})
        
        # Estatísticas básicas
        stats = {
            'total_respostas': total,
            'pagaria': {},
            'ja_teve_aula': {},
            'valor_justo': {},
            'atividades_mais_procuradas': {},
            'formas_de_encontrar': {}
        }
        
        for response in data:
            # Contagem de "pagaria"
            pagaria = response.get('pagaria', '')
            stats['pagaria'][pagaria] = stats['pagaria'].get(pagaria, 0) + 1
            
            # Contagem de "já teve aula"
            ja_teve = response.get('ja_teve_aula', '')
            stats['ja_teve_aula'][ja_teve] = stats['ja_teve_aula'].get(ja_teve, 0) + 1
            
            # Contagem de valor justo
            valor = response.get('valor_justo', '')
            stats['valor_justo'][valor] = stats['valor_justo'].get(valor, 0) + 1
            
            # Atividades mais procuradas
            atividade = response.get('atividade_desejada', '').lower()
            if atividade:
                stats['atividades_mais_procuradas'][atividade] = stats['atividades_mais_procuradas'].get(atividade, 0) + 1
            
            # Formas de encontrar instrutor
            formas = response.get('como_encontrar', [])
            if isinstance(formas, list):
                for forma in formas:
                    stats['formas_de_encontrar'][forma] = stats['formas_de_encontrar'].get(forma, 0) + 1
        
        return jsonify(stats)
        
    except FileNotFoundError:
        return jsonify({'total': 0, 'stats': {}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Inicializa os arquivos de dados
    init_csv_file()
    init_json_file()
    
    print("🚀 Servidor iniciado!")
    print("📊 Questionário disponível em: http://localhost:5000")
    print("📈 Estatísticas em: http://localhost:5000/stats")
    print("📥 Download CSV: http://localhost:5000/download/csv")
    print("📥 Download JSON: http://localhost:5000/download/json")
    print("=" * 50)
    
    # Executa o servidor
    app.run(host='0.0.0.0', port=5000, debug=True)

