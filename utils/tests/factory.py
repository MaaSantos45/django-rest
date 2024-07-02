from random import randint, choice
from faker import Faker

faker = Faker("pt_BR")


def rand_ratio():
    return randint(840, 900), randint(473, 573)


def make_recipes(qtd=1):
    recipes = []

    for _ in range(qtd):
        recipes.append({
            "id": randint(1, 1000),
            "title": faker.sentence(nb_words=4),
            "description": faker.sentence(nb_words=12),
            "preparation_time": faker.random_number(digits=2, fix_len=True),
            "preparation_time_unit": choice(["Minutos", "Horas"]),
            "preparation_steps": faker.text(3000),
            "servings": faker.random_number(digits=2, fix_len=True),
            "servings_unit": choice(["Porção", "Pessoa"]),
            "created_at": faker.date_time(),
            "author": {
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
            },
            "category": faker.word(),
            "cover": {
                "url": "https://loremflickr.com/%s/%s/food,cook" % rand_ratio(),
            }
        })

    if qtd == 1:
        return recipes[0]
    return recipes
