"""
Client module
Módulo principal para solicitações na api Vix
"""

import os
import sys
import json
import uuid
import logging
import requests


class VIXClient(object):
    """
    VIXClient class
    class principal para solicitações na api Vix
    @return: VIXClient object
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # logging.basicConfig(level=logging.INFO)
        self.session = requests.Session()
        self.guest_id = str(uuid.uuid1())
        self.file = 'vix.json'
        self.endpoints = {
            'login': 'https://api-edge.pongalo.com/api/members/login-guest',
            'metadata': 'https://api-edge.pongalo.com/api/catalog/static/show/{0}/webdesktop/BR/pt/metadata',
            'watch': 'https://api-edge.pongalo.com/api/catalog/watch/{0}/{1}/{2}'
        }
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
        self.authorization = self.login()

    def login(self):
        """Iniciando o login e salvando o token em um arquivo json."""
        self.logger.info('login em vix...')
        if os.path.isfile(self.file):
            self.logger.info('arquivo de token antigo encontrado, usando.')
            return self.open_file()
        resp = self.session.post(
            url=self.endpoints['login'],
            json={
                'guestId': '{0}'.format(self.guest_id)
            },
            headers={
                'accept': 'application/json, text/plain, */*',
                'user-agent': self.user_agent
            }
        )
        if resp.status_code == 200:
            self.logger.info('login feito com sucesso.')
            resp_json = resp.json()
            self.save_file(resp_json)
        else:
            self.logger.error('Erro ao fazer login.')
            self.logger.error('status code: {0}'.format(resp.status_code))
            self.logger.error('response: {0}'.format(resp.text))
            sys.exit(1)

        return resp_json

    def get_headers(self):
        """Retorna os cabeçalhos necessários para as solicitações."""
        return {
            'accept': 'application/json, text/plain, */*',
            'authorization': 'Bearer {0}'.format(self.authorization['meta']['jwt']),
            'x-device-os': 'Windows',
            'x-device-platform': 'Chrome',
            'x-device-version': '95.0.4638.69',
            'user-agent': self.user_agent
        }

    def open_file(self):
        """Retorna um objeto json de um arquivo de token."""
        with open(self.file, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        return data

    def save_file(self, tokens=''):
        """Salva o token em um arquivo no formato json após o primeiro login."""
        with open(self.file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(tokens, indent=4))
        return True

    def get_episodes_info(self, content_id):
        """Retorna os metadados e hls para um determinado id de conteúdo."""
        metadata = self.get_metadata(content_id)
        category = metadata.get('categoryKey')
        title = metadata.get('title')
        year = metadata.get('year')

        self.logger.info('obtendo metadados:')
        self.logger.info('categoria: {0} - título: {1} - data de lançamento: {2} '.format(category, title, year))

        episodes = []
        metadata_episodes = metadata.get('episodes', [])
        for m in metadata_episodes:
            episodes.append({
                'name': title,
                'year': year,
                'season': str(m.get('season')).zfill(2),
                'episode': str(m.get('number')).zfill(2),
                'episode_title': m.get('title'),
                'duration': m.get('runningTimeSeconds'),
                'description': m.get('summary'),
                'id': m.get('id'),
                'type': category,
                'hls': self.get_hls(content_id, m.get('season'), m.get('number'))
            })

        return episodes

    def get_metadata(self, content_id):
        """Retorna os metadados para um determinado id de conteúdo."""
        resp = self.session.get(
            url=self.endpoints['metadata'].format(content_id),
            headers=self.get_headers()
        )
        if resp.status_code == 200:
            resp_json = resp.json()
        else:
            self.logger.error('Erro ao obter metadados.')
            self.logger.error('status code: {0}'.format(resp.status_code))
            self.logger.error('response: {0}'.format(resp.text))
            sys.exit(1)

        return resp_json['data']

    def get_hls(self, content_id, season, number):
        """Retorna o hls para um determinado id de conteúdo."""
        resp = self.session.get(
            url=self.endpoints['watch'].format(content_id, season, number),
            headers=self.get_headers()
        )
        if resp.status_code == 200:
            resp_json = resp.json()
        else:
            self.logger.error('Erro ao obter hls.')
            self.logger.error('status code: {0}'.format(resp.status_code))
            self.logger.error('response: {0}'.format(resp.text))
            sys.exit(1)

        return resp_json['data']['playKey']