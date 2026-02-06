# -*- coding: utf-8 -*-
import requests
import names
import random
import time
from info.default_data import Dflt

# Объявление переменных
URL = Dflt.API_URL
TOKEN = Dflt.TRAINER_TOKEN
TRAINER_ID = Dflt.TRAINER_ID

HEADER = {'Content-Type' : 'application/json', 'Trainer_token' : Dflt.TRAINER_TOKEN } 
POKEMON_NAME = names.get_first_name(gender=any)
POKEMON_PHOTO = random.randint(1, 600)
POKEMON_ID = "15257"                    # вставьте id вашего покемона
POKEMON_NEW_NAME = names.get_first_name(gender=any)
POKEMON_NEW_PHOTO = random.randint(1, 600)

body_change_name = {
    "pokemon_id": POKEMON_ID,
    "name": POKEMON_NEW_NAME,
    "photo_id": POKEMON_NEW_PHOTO
}

body_auth = {
    "email": Dflt.VALID['email'],
    "password": Dflt.VALID['password']

}

# Авторизация на сайте
'''responce_authorization = requests.post(url=f'{Dflt.API_URL}/auth', headers=HEADER, json=body_auth)
print(responce_authorization.text)'''

# Получить информацию о своем тренере
'''responce_trainer_information = requests.get(url=f'{Dflt.API_URL}/me', headers=HEADER)
print(responce_trainer_information.text)
print(responce_trainer_information.status_code)
CURRENT_TRAINER_ID = responce_trainer_information.json()['data'][0]['id']
print(CURRENT_TRAINER_ID)'''

# Изменить имя и фотографии покемона
'''response_change_name = requests.put(url=f'{Dflt.API_URL}/pokemons', headers=HEADER, json=body_change_name)
print(response_change_name.text, response_change_name.status_code)'''

# Получение информации о конкретном покемоне
'''responce_pokemon_information = requests.get(url=f'{Dflt.API_URL}/pokemons/{POKEMON_ID}', headers=HEADER)
print(responce_pokemon_information.text)
print(responce_pokemon_information.status_code)'''

# Получить ошибку 500
'''responce_error = requests.get(url=f'{Dflt.API_URL}/debug_sentry', headers=HEADER)
print(responce_error.text)
print(responce_error.status_code)'''

# Получить список своих живых покемонов
responce_pokemons_list = requests.get(url=f'{Dflt.API_URL}/pokemons?trainer_id={TRAINER_ID}&status=1', headers=HEADER)
print('Список моих живых покемонов: ', responce_pokemons_list.text)
# print('Статус ответа от сервера: ', responce_pokemons_list.status_code)

# Посчитать количество своих живых покемонов
count_my_pokemons = 0
if "data" in responce_pokemons_list.json():
    count_my_pokemons = len(responce_pokemons_list.json()['data'])
    print(f'Количество моих живых покемонов: {count_my_pokemons}')
    POKEMON_FOR_FIGHT_ID = responce_pokemons_list.json()['data'][count_my_pokemons-1]['id']
    print('ID моего покемона, выбранного для сражения:',POKEMON_FOR_FIGHT_ID)

# Если живых покемонов равно 1, то создаем 4 новых покемона, чтобы поддерживать их количество
if count_my_pokemons == 1:
    while count_my_pokemons < 5 :
        try:
            body_creation = {
            "name": names.get_first_name(gender=any),
            "photo_id": random.randint(1, 600)
            }
            response_creation = requests.post(url=f'{Dflt.API_URL}/pokemons', 
                                            headers = HEADER, 
                                            json=body_creation,
                                            timeout = 5)
            if response_creation.status_code == 201:
                count_my_pokemons += 1
                # print('Количество моих живых покемонов после создания нового: ', count_my_pokemons)
            else:
                print(f'Ошибка сервера: {response_creation.status_code} - {response_creation.text}')            
        except requests.exceptions.Timeout:
            print('Время ожидания ответа превысило таймаут')
        except requests.exceptions.RequestException as e:
            print(f'Ошибка сети: {e}')
        time.sleep(1) # пауза между запросами
    print('Создали 4 новых покемона')

# НАЧАТЬ БИТВУ
print('Начать битву')
# Получить список всех живых покемонов в покеболе
responce_pokemons_list = requests.get(url=f'{Dflt.API_URL}/pokemons?in_pokeball=1&status=1&sort=asc_attack', headers=HEADER)
# print(responce_pokemons_list.text)
print('Получаем список всех живых покемонов для выбора соперника')

# Выбрать покемона для битвы
ENEMY_ID = responce_pokemons_list.json()['data'][6]['id']
print('ID покемона соперника: ', ENEMY_ID)

# Поймать своего покемона в покебол
body_add_pokeball = {
   "pokemon_id": POKEMON_FOR_FIGHT_ID
} 
response_add_pokeball = requests.post(url=f'{Dflt.API_URL}/trainers/add_pokeball', headers=HEADER, json=body_add_pokeball)
print('Ловим своего покемона в покебол')
# print(response_add_pokeball.status_code)

# Создать body для проведения битвы
body_battle = {
    "attacking_pokemon": POKEMON_FOR_FIGHT_ID,
    "defending_pokemon": ENEMY_ID
}

# Провести битву покемонов
responce_battle = requests.post(url=f'{Dflt.API_URL}/battle', headers=HEADER, json=body_battle)
# print(responce_battle.text)
print('Проводим битву покемонов')

# Проверка не исчерпан ли лимит битв на сегодня
if responce_battle.json()["message"] == "Твой лимит боёв исчерпан. Текущее ограничение: 50 в день":
    print("Твой лимит боёв исчерпан. Текущее ограничение: 50 в день")
else:
    # Вывести результат битвы
    battle_result = responce_battle.json()["result"]
    #print(battle_result)
    if battle_result == "Твой покемон проиграл": 
        print("Результат - твой покемон проиграл. Сочувствую!")
    else: 
        print("Результат - твой покемон победил! Поздравляю!") 
        # Выселить покемона из покебола
        response_delete_pokeball = requests.put(url=f'{Dflt.API_URL}/trainers/delete_pokeball', headers=HEADER, json=body_add_pokeball) 
        print('Твой покемон отвязан от покебола')
        # print(response_delete_pokeball.status_code)
    print('Битва завершена')