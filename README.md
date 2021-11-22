# pyvix
Biblioteca Python para interação com [Vix](https://www.vix.com/tv) Brasil API

- [Uso](#uso)
  * [Obter informações sobre o conteúdo](#obter-informações-sobre-o-conteúdo)
    + [Exemplo de saída](#exemplo-de-saída)
- [Exemplo para uso básico](#exemplo-para-uso-básico)

# Uso:

Inicializar classe principal VIXClient:

```python
client = pyvix.VIXClient()
```

# Obter informações sobre o conteúdo:

Usando a classe inicializada, solicite informações do filme ou série(todos os episódios) com:

```python
episodes = client.get_episodes_info(media_id)
```

O id de conteúdo pode ser encontrado no URL do conteúdo.
Por exemplo, id de conteúdo para <br /> 
filme: `https://www.vix.com/tv/movie/movies/doomsday_pt` é `doomsday_pt` <br />
série: `https://www.vix.com/tv/serie/series/haven_pt` é `haven_pt`.

# Exemplo de saída:
```
Filmes:
[{
    "name": "Juízo Final",
    "year": "2008",
    "season": "01",
    "episode": "01",
    "episode_title": "Juízo Final",
    "duration": 6480,
    "description": "Trinta anos após devastar a Escócia, um vírus mortal atinge a Inglaterra. Com milhões de vidas em jogo, o governo corre contra o tempo para encontrar uma solução.",
    "id": "611ef094a15a31a2e4fd9fd6",
    "type": "movies",
    "hls": "https://prod.pongalo.com/play.m3u8?access-key=7bb4397d4960b4acf5f18c97451ef4716089179b"
}]
Series:
[{
    "name": "Haven",
    "year": "2010",
    "season": "01",
    "episode": "01",
    "episode_title": "Bem-vinda a Haven",
    "duration": 2640,
    "description": "A agente do FBI Audrey Parker chega a Haven, Maine, em um caso de rotina - mas sua investigação e uma série de fenômenos inexplicáveis ​​a levam a descobrir misterios e segredos obscuros da cidade.",
    "id": "5f2451e44293590001d9771e",
    "type": "series",
    "hls": "https://prod.pongalo.com/play.m3u8?access-key=e02b7ea456c8a5fd0528da243b663f7150be1945"
},
{
    "name": "Haven",
    "year": "2010",
    "season": "01",
    "episode": "02",
    "episode_title": "Borboleta",
    "duration": 2640,
    "description": "Audrey deve resolver o enigma do que ou quem está cometendo atos aparentemente aleatórios e perigosos pela cidade - mesmo quando ela se torna o alvo.",
    "id": "5f2451e44293590001d9771f",
    "type": "series",
    "hls": "https://prod.pongalo.com/play.m3u8?access-key=157bb0072b72b1aa0bcadc0e792de9ed44d2ed66"
}]
```

# Exemplo para uso básico:

```python
>>> import pyvix
>>> client = pyvix.VIXClient()
>>> client.get_episodes_info('doomsday_pt')
[{'name': 'Juízo Final', 'year': '2008', ...
```
