# Questionário - Atividades com Instrutores

Um questionário web bonito e intuitivo para coletar informações sobre preferências de atividades com instrutores.

## 🚀 Como executar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o servidor
```bash
python app.py
```

### 3. Acessar o questionário
Abra seu navegador e acesse: `http://localhost:5000`

## 📊 Funcionalidades

- **Interface moderna e responsiva** - Design intuitivo que funciona em desktop e mobile
- **Validação em tempo real** - Feedback imediato para o usuário
- **Múltiplos formatos de dados** - Salva em CSV e JSON
- **Estatísticas automáticas** - Análise básica dos dados coletados
- **Download de dados** - Exportação fácil dos resultados

## 📁 Estrutura dos arquivos

```
questionario-instrutores/
├── app.py              # Servidor Flask (backend)
├── index.html          # Interface do questionário
├── style.css           # Estilos e design
├── script.js           # Funcionalidades JavaScript
├── requirements.txt    # Dependências Python
├── README.md          # Este arquivo
├── respostas.csv      # Dados salvos em CSV (criado automaticamente)
└── respostas.json     # Dados salvos em JSON (criado automaticamente)
```

## 🔗 Endpoints disponíveis

- `GET /` - Página principal do questionário
- `POST /submit` - Envio de respostas
- `GET /responses` - Visualizar todas as respostas (JSON)
- `GET /stats` - Estatísticas dos dados coletados
- `GET /download/csv` - Download do arquivo CSV
- `GET /download/json` - Download do arquivo JSON

## 📋 Perguntas do questionário

1. **Atividade desejada** - Qual atividade você mais gostaria de aprender?
2. **Disposição para pagar** - Pagaria por essa atividade?
3. **Valor justo** - Quanto pagaria por uma aula?
4. **Experiência anterior** - Já teve aula com instrutor?
5. **Como encontrar** - Como procuraria um instrutor?
6. **Comentários** - Sugestões ou observações adicionais

## 💾 Formato dos dados salvos

### CSV
Arquivo simples com colunas separadas por vírgula, ideal para análise em Excel ou Google Sheets.

### JSON
Formato estruturado que preserva arrays e objetos, ideal para análise programática.

## 📈 Visualizar estatísticas

Acesse `http://localhost:5000/stats` para ver um resumo dos dados coletados, incluindo:
- Total de respostas
- Distribuição de respostas por categoria
- Atividades mais procuradas
- Formas preferidas de encontrar instrutores

## 🛠️ Personalização

Para modificar as perguntas ou adicionar novas:

1. **HTML** - Edite `index.html` para alterar a estrutura do formulário
2. **CSS** - Modifique `style.css` para ajustar o design
3. **JavaScript** - Atualize `script.js` para nova lógica de frontend
4. **Backend** - Ajuste `app.py` para processar novos campos

## 🔒 Segurança

- Validação de dados no frontend e backend
- Sanitização de entradas
- CORS configurado para desenvolvimento local
- Logs de erro para debugging

## 📱 Responsividade

O questionário é totalmente responsivo e funciona bem em:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (até 767px)

---

**Desenvolvido com Flask, HTML5, CSS3 e JavaScript vanilla**

