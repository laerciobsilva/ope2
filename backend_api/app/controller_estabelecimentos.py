from .model import db, Estabelecimento
from flask import jsonify

class ControllerEstabelecimentos():

    def post_estabelecimentos(self, request):
        nome = request.json['nome']
        cnpj = request.json['cnpj']
        novo_estabelecimento = self._criar_estabelecimento(nome, cnpj)
        return jsonify(
            mensagem='Estabelecimento criado com sucesso.',
            id = novo_estabelecimento.id
        )

    def delete_estabelecimentos(self, id_estabelecimento):
        self._deletar_estabelecimento(id_estabelecimento)
        return jsonify(
            mensagem = 'Estabelecimento deletado com sucesso.'
        )

    def get_estabelecimentos_id(self, id_estabelecimento):
        estabelecimento = self._buscar_estabelecimento(id_estabelecimento)
        return jsonify (
            id = estabelecimento.id,
            nome = estabelecimento.nome,
            cnpj = estabelecimento.cnpj
        )

    def get_estabelecimentos(self):
        estabelecimentos = self._listar_todos_estabelecimentos()
        json_response = []
        for estabelecimento in estabelecimentos:
            json_response.append({
                'id': estabelecimento.id,
                'nome': estabelecimento.nome,
                'cnpj': estabelecimento.cnpj
            })    
        return jsonify (json_response)

    def put_estabelecimentos(self, id_estabelecimento, request):
        nome = request.json['nome']
        cnpj = request.json['cnpj']
        self._atualizar_estabelecimento(id_estabelecimento, nome, cnpj)
        estabelecimento = self._buscar_estabelecimento(id_estabelecimento)
        return jsonify (
            id = estabelecimento.id,
            nome = estabelecimento.nome,
            cnpj = estabelecimento.cnpj
        )

    #
    # métodos internos
    #

    def _criar_estabelecimento(self, nome, cnpj):
        novo_estabelecimento = Estabelecimento(nome=nome, cnpj=cnpj)
        db.session.add(novo_estabelecimento)
        db.session.commit()
        return novo_estabelecimento

    def _deletar_estabelecimento(self, id):
        estabelecimento = Estabelecimento.query.filter_by(id=id).first()
        db.session.delete(estabelecimento)
        db.session.commit()

    def _buscar_estabelecimento(self, id):
        return Estabelecimento.query.filter_by(id=id).first()

    def _atualizar_estabelecimento(self, id, nome, cnpj):
        estabelecimento = Estabelecimento.query.filter_by(id=id).first()
        estabelecimento.nome = nome
        estabelecimento.cnpj = cnpj
        db.session.add(estabelecimento)
        db.session.commit()

    def _listar_todos_estabelecimentos(self):
        return Estabelecimento.query.all()
