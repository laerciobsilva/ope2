from .model import db, Produto, Estabelecimento, Categoria
from flask import jsonify

class ControllerProdutos():

    def post_produtos(self, request):
        nome = request.json['nome']
        descricao = request.json['descricao']
        ingredientes = request.json['ingredientes']
        modo_de_preparo = request.json['modo_de_preparo']
        preco = request.json['preco']
        estabelecimento_id = request.json['estabelecimento_id']
        categoria_id = request.json['categoria_id']

        novo_produto = self._criar_produto(nome, descricao, ingredientes, modo_de_preparo, preco, estabelecimento_id, categoria_id)
        return jsonify(
            mensagem='Produto criada com sucesso.',
            id = novo_produto.id
        )

    def delete_produtos(self, id_produto):
        self._deletar_produto(id_produto)
        return jsonify(
            mensagem = 'Produto deletado com sucesso.'
        )

    def get_produtos_id(self, id_produto):
        produto = self._buscar_produto(id_produto)
        return jsonify(
            id = produto.id,
            nome = produto.nome,
            descricao = produto.descricao,
            ingredientes = produto.ingredientes,
            modo_de_preparo = produto.modo_de_preparo,
            preco = produto.preco,
            estabelecimento_id = produto.estabelecimento.id,
            categoria_id = produto.categoria.id
        )

    def get_produtos(self):
        produtos = self._listar_todos_produtos()
        json_response = []
        for produto in produtos:
            json_response.append({
                'id': produto.id,
                'nome': produto.nome,
                'descricao' : produto.descricao,
                'ingredientes' : produto.ingredientes,
                'modo_de_preparo' : produto.modo_de_preparo,
                'preco' : produto.preco,
                'estabelecimento_id' : produto.estabelecimento.id,
                'categoria_id' : produto.categoria.id
            })    
        return jsonify(json_response)

    def put_produtos(self, id_categoria, request):
        nome = request.json['nome']
        descricao = request.json['descricao']
        ingredientes = request.json['ingredientes']
        modo_de_preparo = request.json['modo_de_preparo']
        preco = request.json['preco']
        estabelecimento_id = request.json['estabelecimento_id']
        categoria_id = request.json['categoria_id']

        produto = self._atualizar_produto(id_categoria, nome, descricao, ingredientes, modo_de_preparo, preco, estabelecimento_id, categoria_id)
        return jsonify(
            id = produto.id,
            nome = produto.nome,
            descricao = produto.descricao,
            ingredientes = produto.ingredientes,
            modo_de_preparo = produto.modo_de_preparo,
            preco = produto.preco,
            estabelecimento_id = produto.estabelecimento.id,
            categoria_id = produto.categoria.id
        )

    #
    # métodos internos
    #

    def _criar_produto(self, nome, descricao, ingredientes, modo_de_preparo, preco, estabelecimento_id, categoria_id):
        estabelecimento = Estabelecimento.query.filter_by(id=estabelecimento_id).first()
        categoria = Categoria.query.filter_by(id=categoria_id).first()
        novo_produto = Produto(nome=nome, descricao=descricao, ingredientes=ingredientes, modo_de_preparo=modo_de_preparo, preco=preco, estabelecimento=estabelecimento, categoria=categoria)
        db.session.add(novo_produto)
        db.session.commit()
        return novo_produto

    def _deletar_produto(self, id):
        produto = self._buscar_produto(id)
        db.session.delete(produto)
        db.session.commit()

    def _buscar_produto(self, id):
        return Produto.query.filter_by(id=id).first()

    def _atualizar_produto(self, id, nome, descricao, ingredientes, modo_de_preparo, preco, estabelecimento_id, categoria_id):
        produto = self._buscar_produto(id)
        estabelecimento = Estabelecimento.query.filter_by(id=estabelecimento_id).first()
        categoria = Categoria.query.filter_by(id=categoria_id).first()
        produto.nome = nome
        produto.descricao = descricao
        produto.ingredientes = ingredientes
        produto.modo_de_preparo = modo_de_preparo
        produto.preco = preco
        produto.estabelecimento = estabelecimento
        produto.categoria = categoria

        db.session.add(produto)
        db.session.commit()
        return produto

    def _listar_todos_produtos(self):
        return Produto.query.all()