"""
数据来源
https://www.gamersky.com/tools/palworldwiki/#/
"""

import requests
import json
import sqlite3

resList = []

# 请求url
listUrl = 'https://router2.gamersky.com/@/palworld/list'
detailUrl = 'https://router2.gamersky.com/@/palworld/detail'

# 请求头
headers = {
    'Content-Type': 'application/json'
}

def getList(pageIndex = 0):



    # 请求参数
    data = {
        'pageIndex': pageIndex,
    }

    # 转换数据为JSON格式
    json_data = json.dumps(data)

    # 发送请求
    response = requests.post(listUrl, data=json_data, headers=headers)

    # 获取返回的json数据
    res_json = response.json()

    # 打印数据
    # print(res_json)
    for pet in res_json['pets']:
        # print(pet['base']['name'])
        saveData(pet)
        resList.append(pet)

    if res_json['hasMore']:
        getList(pageIndex + 1)

def saveData(data):
    # 插入数据
    base = data['base']
    workInfo = data['workInfo']

    cursor.execute('''INSERT INTO pet
            (petNo, name, attribute, description, dropItem, food, imageUrl, workInfo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
    (base['petNo'], base['name'],  base['attribute'], base['description'], base['dropItem'], base['food'], base['imageUrl'], workInfo['workInfo']))


    # 详情信息
    params = {
        'petNo': base['petNo']
    }

    response = requests.get(detailUrl, params=params, headers=headers)

    # 获取返回的json数据
    res_json = response.json()

    property_data = res_json['property']
    cursor.execute('''INSERT INTO pet_properties
                    (attackMelee, attackShooting, endurance, hp, name, petNo, price, speedRun, speedWalk, weight)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
               (property_data['attackMelee'], property_data['attackShooting'], property_data['endurance'], property_data['hp'], property_data['name'], property_data['petNo'], property_data['price'], property_data['speedRun'], property_data['speedWalk'], property_data['weight']))


    partners_skill_data = res_json['partnersSkill']
    cursor.execute('''INSERT INTO pet_partners_skill
                        (effect, name, pairpetName, petNo)
                        VALUES (?, ?, ?, ?)''',
                (partners_skill_data['effect'], partners_skill_data['name'], partners_skill_data['pairpetName'], partners_skill_data['petNo']))

    for skill in res_json['skills']:
        cursor.execute('''INSERT INTO pet_skills
                            (coolTime, skillName, skillRange, power, type, unlockLevel, petNo)
                            VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (skill['coolTime'], skill['skillName'], skill['skillRange'], skill['power'], skill['type'], skill['unlockLevel'], skill['petNo']))



# 连接 SQLite 数据库
conn = sqlite3.connect('palworld.db')
cursor = conn.cursor()

# 删除已存在的表
cursor.execute('DROP TABLE IF EXISTS pet')
cursor.execute('DROP TABLE IF EXISTS pet_properties')
cursor.execute('DROP TABLE IF EXISTS pet_partners_skill')


# 创建表 基础属性
cursor.execute('''CREATE TABLE IF NOT EXISTS pet (
    id INTEGER PRIMARY KEY,
    petNo TEXT,
    name TEXT,
    attribute TEXT,
    description TEXT,
    dropItem TEXT,
    food TEXT,
    imageUrl TEXT,
    workInfo TEXT
)''')

# 属性
cursor.execute('''CREATE TABLE IF NOT EXISTS pet_properties (
    id INTEGER PRIMARY KEY,
    attackMelee TEXT,
    attackShooting TEXT,
    endurance TEXT,
    hp TEXT,
    name TEXT,
    petNo TEXT,
    price TEXT,
    speedRun TEXT,
    speedWalk TEXT,
    weight TEXT
)''')

# 合作技能
cursor.execute('''CREATE TABLE IF NOT EXISTS pet_partners_skill (
    id INTEGER PRIMARY KEY,
    effect TEXT,
    name TEXT,
    pairpetName TEXT,
    petNo TEXT
)''')

# 技能
cursor.execute('''CREATE TABLE IF NOT EXISTS pet_skills (
    id INTEGER PRIMARY KEY,
    coolTime TEXT,
    skillName TEXT,
    skillRange TEXT,
    power TEXT,
    type TEXT,
    unlockLevel TEXT,
    petNo TEXT
)''')

getList()

# with open('palworld.json', 'w') as f:
#     json.dump(resList, f)

# 提交更改
conn.commit()

# 关闭数据库连接
conn.close()
