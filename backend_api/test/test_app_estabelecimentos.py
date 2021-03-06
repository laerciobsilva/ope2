import unittest, os, sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from app import app


class TestApp(unittest.TestCase):
    #
    # setUp e tearDown
    #

    def setUp(self):
        self.ids_estabelecimentos_criados = []
        self.client = app.app.test_client()

    def tearDown(self):
        for estabelecimento in self.ids_estabelecimentos_criados:
            self.client.delete('/estabelecimentos/' + str(estabelecimento))
        self.ids_estabelecimentos_criados = []


    #
    # testes
    #

    def test_cria_estabelecimento(self):
        # arrange
        json_data = self._test_data()
        
        # act
        response = self._cria_estabelecimento(json_data)
        
        # assert
        assert response.json['mensagem'] == 'Estabelecimento criado com sucesso.'

    def test_busca_estabelecimento(self):
        # arrange
        json_data = self._test_data()
        id_estabelecimento = self._cria_estabelecimento(json_data).json['id']

        # act
        response = self.client.get('/estabelecimentos/' + str(id_estabelecimento))

        # assert
        assert response.json['id'] == id_estabelecimento
        assert response.json['nome'] == json_data['nome']
        assert response.json['cnpj'] == json_data['cnpj']

    def test_listar_estabelecimentos(self):
        # arrange
        json_data_1 = self._test_data()
        id_estabelecimento_1 = self._cria_estabelecimento(json_data_1).json['id']

        json_data_2 = {
            'nome': 'estabelecimento teste_',
            'cnpj': '1234567890123_'
        }
        id_estabelecimento_2 = self._cria_estabelecimento(json_data_2).json['id']     
        
        # act
        response = self.client.get('/estabelecimentos/')

        # assert
        for response_item in response.json:
            if response_item['id'] == id_estabelecimento_1:
                estabelecimento_1 = response_item
            if response_item['id'] == id_estabelecimento_2:
                estabelecimento_2 = response_item

        assert estabelecimento_1['nome'] == json_data_1['nome']
        assert estabelecimento_1['cnpj'] == json_data_1['cnpj']
        assert estabelecimento_2['nome'] == json_data_2['nome']
        assert estabelecimento_2['cnpj'] == json_data_2['cnpj']

    def test_atualiza_estabelecimento(self):
        # arrange
        id_estabelecimento = self._cria_estabelecimento(self._test_data()).json['id']

        novo_json_data = {
            'nome': 'estabelecimento teste_',
            'cnpj': '1234567890123_'
        }

        # act
        self.client.put('/estabelecimentos/' + str(id_estabelecimento), json=novo_json_data)

        # assert
        response = self.client.get('/estabelecimentos/' + str(id_estabelecimento))
        assert response.json['id'] == id_estabelecimento
        assert response.json['nome'] == novo_json_data['nome']
        assert response.json['cnpj'] == novo_json_data['cnpj']

    #
    # metodos de suporte
    #

    def _cria_estabelecimento(self, json_data):
        response = self.client.post('/estabelecimentos/', json=json_data)
        self.ids_estabelecimentos_criados.append(response.json['id'])
        return response

    def _test_data(self):
        return {
            'nome': 'estabelecimento teste',
            'cnpj': '12345678901234'
        }
