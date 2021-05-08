# edamam.com - food recipes

import requests
import json
import sqlite3

# get url

search = input("search all recipes by an ingredient: ") # example: "chicken"
payload = {"q":search,"app_id":"5425c89e","app_key":"8717cf755015c692be732e27c9da5e83"}
response = requests.get("https://api.edamam.com/search", params=payload)
output1 = response.json()
# print(response.text)
# print(response.status_code)
output2 = json.dumps(output1,indent=4)
# print(output2)

# save a json file

with open("munchies.json","w") as recipes:
    json.dump(output1,recipes,indent=4)

# print names of food and ingredients

for each in output1["hits"]:
    print(each["recipe"]["label"])
    ingredient_list = []
    for ing in each["recipe"]["ingredients"]:
        ingredient_list.append(ing["text"])
    print(ingredient_list)

# create a food database

foodbase = sqlite3.connect("Food_Data.sqlite")
cursor = foodbase.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS food
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_name VARCHAR(50),
                URL VARCHAR(255),
                ingredients VARCHAR(255))
''')

full_info = []

for every in output1["hits"]:
    fname = every["recipe"]["label"]
    url = every["recipe"]["url"]
    ingr = ""
    for each in every["recipe"]["ingredientLines"]:
        ingr += each
    info = (fname, url, ingr)
    full_info.append(info)

cursor.executemany('''INSERT INTO food (food_name,URL,ingredients)
                      VALUES (?,?,?)''',full_info)


foodbase.commit()
foodbase.close()


