from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as gemini

app = Flask(__name__)
CORS(app)
gemini.configure(api_key="chave vai aqui")
model = gemini.GenerativeModel('gemini-1.5-flash')

@app.route('/filmes', methods=['POST'])
def make_():
    try:
        dados = request.json
        recomendacao = dados.get('recomendacao')
        prompt = f"""
        Baseado no sentimento {recomendacao}, recomende um filme, uma série e um conteúdo infantil que mais se encaixem.
        Para cada recomendação não importa a plataforma que esteja como por exemplo netflix, prime ou etc, forneça as seguintes informações:
        - Nome do conteúdo
        - Duração 
        - Indicação de idade
        - Tema principal
        - Motivo da escolha do filme (relação com o sentimento)
        - Plataforma onde o conteúdo pode ser assistido

        Apresente a recomendação no formato HTML com codificação UTF-8, sem o header,
        com o título em h1, subtítulos em h2 para cada categoria (Filme, Série, Infantil),
        e as informações detalhadas em parágrafos. Mantenha o formato especificado para os ícones de relógio e pratos, 
        como indicado no código original, mesmo que não sejam aplicáveis neste contexto.
        O nome do filme deve ser um link (link amarelo) de uma pesquisa do google que mostre o filme ou serie(nesse link você precisa colocar o nome do conteudo e após o que ele é filme ou série)
        """
        resposta = model.generate_content(prompt)
        print(resposta)
        recomendacao = resposta.text.strip().split('\n')
        return (recomendacao), 200
    except Exception as e:
        return jsonify({"Erro": str(e)}), 300

if __name__ == '__main__':
    app.run(debug=True)