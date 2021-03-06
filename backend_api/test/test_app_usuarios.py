import unittest, os, sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from app import app


class TestAppUsuarios(unittest.TestCase):
    #
    # setUp e tearDown
    #

    @classmethod
    def setUpClass(self):
        self.client = app.app.test_client()
        self.id_estabelecimento = self.client.post('/estabelecimentos/', json={
            'nome': 'nome teste',
            'cnpj': '12345678901234'
        }).json['id']

    @classmethod
    def tearDownClass(self):
        self.client.delete('/estabelecimentos/' + str(self.id_estabelecimento))

    def setUp(self):
        self.ids_usuarios_criados = []

    def tearDown(self):
        for id_usuario in self.ids_usuarios_criados:
            self.client.delete('/usuarios/' + str(id_usuario))
        self.ids_usuarios_criados = []

    #
    # testes
    #

    def test_cria_usuario(self):
        # arrange
        json_data = self._test_data()

        #act
        response = self._cria_usuario(json_data)

        # assert
        assert response.json['mensagem'] == u'Usuário criado com sucesso.'

    def test_busca_usuario(self):
        # arrange
        json_data = self._test_data()
        id_usuario = self._cria_usuario(json_data).json['id']

        # act
        response = self.client.get('/usuarios/' + str(id_usuario))

        # assert
        assert response.json['id'] == id_usuario
        assert response.json['login'] == json_data['login']
        assert response.json['id_estabelecimento'] == json_data['id_estabelecimento']

    def test_listar_usuarios(self):
        # arrange
        json_data_1 = self._test_data()
        id_usuario_1  = self._cria_usuario(json_data_1).json['id']

        json_data_2 = {
            'login': 'login teste_',
            'senha': 'senha teste_',
            'id_estabelecimento': self.id_estabelecimento
        }
        id_usuario_2 = self._cria_usuario(json_data_2).json['id']

        # act
        response = self.client.get('/usuarios/')

        # assert
        for response_item in response.json:
            if response_item['id'] == id_usuario_1:
                usuario_1 = response_item
            if response_item['id'] == id_usuario_2:
                usuario_2 = response_item

        assert usuario_1['login'] == json_data_1['login']
        assert usuario_1['id_estabelecimento'] == json_data_1['id_estabelecimento']
        assert usuario_2['login'] == json_data_2['login']
        assert usuario_2['id_estabelecimento'] == json_data_2['id_estabelecimento']

    def test_atualizar_usuario(self):
        # arrange
        id_usuario = self._cria_usuario(self._test_data()).json['id']
        novo_json_data = {
            'login': 'login teste_',
            'senha': 'senha teste_',
            'id_estabelecimento': self.id_estabelecimento
        }

        # act
        response = self.client.put('/usuarios/' + str(id_usuario), json=novo_json_data)

        # assert
        assert response.json['id'] == id_usuario
        assert response.json['login'] == novo_json_data['login']
        assert response.json['id_estabelecimento'] == self.id_estabelecimento

    def test_login(self):
        # arrange
        json_data_usuario = self._test_data()
        id_usuario = self._cria_usuario(json_data_usuario).json['id']

        json_data_login = {
            'login': json_data_usuario['login'],
            'senha': json_data_usuario['senha']
        }

        # act
        response = self.client.post('/usuarios/login', json=json_data_login)

        # assert
        assert response.status_code == 200

    def test_login_invalido(self):
        # arrange
        json_data_usuario = self._test_data()
        id_usuario = self._cria_usuario(json_data_usuario).json['id']

        json_data_login = {
            'login': json_data_usuario['login'],
            'senha': 'outra senha'
        }

        # act
        response = self.client.post('/usuarios/login', json=json_data_login)

        # assert
        assert response.status_code == 400

    #
    # metodos de suporte
    #

    def _cria_usuario(self, json_data):
        response = self.client.post('/usuarios/', json=json_data)
        self.ids_usuarios_criados.append(response.json['id'])
        return response

    def _test_data(self):
        return {
            'login': 'login teste',
            'senha': 'senha teste',
            'id_estabelecimento': self.id_estabelecimento
        }
