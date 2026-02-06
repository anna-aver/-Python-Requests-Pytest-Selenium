import requests
import pytest
import names
import random
from info.default_data import Dflt

URL = Dflt.API_URL
TOKEN = Dflt.TRAINER_TOKEN
HEADER = {'Content-Type' : 'application/json', 'trainer_token' : TOKEN}
TRAINER_ID = Dflt.TRAINER_ID
POKEMON_ID = 'ХХХХХ'           # вставьте id вашего покемона
POKEMON_KNOCKOUT = 'ННННН'     # вставьте id покемона, которого хотите отправить в нокаут


# 1. Проверка метода GET/pokemons (получение списка покемонов по ID тренера)
def test_status_code():
    response = requests.get(url = f'{URL}/pokemons',  params={'trainer_id': TRAINER_ID})
    assert response.status_code == 200

# 2. Проверка части ответа метода GET/pokemons (наличие поля name с заданным значением в ответе)
def test_part_of_response():
    response_get = requests.get(url=f'{URL}/pokemons', params={'trainer_id':TRAINER_ID})
    assert response_get.json()['data'][0]['name'] == 'Имя покемона'

# 3. Проверить, что метод GET /pokemons возвращает ответ заданной структуры
@pytest.mark.parametrize('key, value',[('name', 'Имя покемона'), ('trainer_id', TRAINER_ID), ('id', 'id покемона')])
def test_parametrize(key, value):
    response_parametrize = requests.get(url=f'{URL}/pokemons', params={'trainer_id':TRAINER_ID})
    assert response_parametrize.json()['data'][0][key] == value

# 4. Отправить покемона в нокаут
def test_knockout():
    body_knockout = {
        "pokemon_id": POKEMON_KNOCKOUT
    }
    responce_knockout = requests.post(url=f'{Dflt.API_URL}/pokemons/knockout', 
                                        headers=HEADER,
                                        json=body_knockout)
    assert responce_knockout.status_code == 200

# 5. Создать покемона POST/pokemons
def test_create_pokemon():
    body_creation = {
        "name": names.get_first_name(gender=any),
        "photo_id": random.randint(1, 600)
    }
    response_creation = requests.post(url=f'{Dflt.API_URL}/pokemons', 
                                        headers = HEADER, 
                                        json=body_creation,
                                        timeout = 5)
    assert response_creation.status_code == 201

# 6. Изменить имя и фотографию покемона PATCH/pokemons
def test_change_pokemon():
    body_change_name = {
    "pokemon_id": POKEMON_ID,
    "name": names.get_first_name(gender=any),
    "photo_id": random.randint(1, 600)
    }
    response_change_name = requests.patch(url=f'{Dflt.API_URL}/pokemons', headers=HEADER, json=body_change_name)
    print(response_change_name.text)
    assert response_change_name.status_code == 200

# 7. Получить ошибку 500
def test_get_500():
    responce_error = requests.get(url=f'{Dflt.API_URL}/debug_sentry', headers=HEADER)
    print(responce_error.text)
    print(responce_error.status_code)
    assert responce_error.status_code == 500