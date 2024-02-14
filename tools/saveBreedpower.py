import sqlite3

from breedpower import getBreedpower


# 连接 SQLite 数据库
conn = sqlite3.connect('palworld.db')
cursor = conn.cursor()


# 添加新的字段
try:
    cursor.execute('''ALTER TABLE pet ADD COLUMN breed_power INTEGER''')
    conn.commit()
    print("新字段添加成功")
except sqlite3.Error as e:
    print("添加新字段时出错:", e)

list = getBreedpower()

for pet in list:
    cursor.execute('UPDATE pet SET breed_power = ? WHERE name = ?', (pet['breedpower'], pet['name']))
    conn.commit()
    print(pet['name'], "繁殖能力值", pet['breedpower'], "更新成功")

# 关闭数据库连接
conn.close()