import json
from collections import defaultdict
import random
import string
import requests
from src.files import Menu


def parse_menu(text: str) -> dict:
    text = text.replace('/menu', '').strip()

    menu = {
        'offerings': {},
        'active': True,
        'orders': {}
    }
    course = []
    for line in text.split('\n'):
        # print(f"Handling line \"{line}\"")
        line = line.strip()
        if line[0] == '.':
            line = line[1:].strip()
            menu['offerings'][line] = []
            course = menu['offerings'][line]
        else:
            course.append(line)

    # To add the last one
    menu[title].update({curr_level: curr_dishes})

    return menu


def recap(menu: Menu) -> str:
    summary = {category: {dish: 0 for dish in menu['offerings'][category]} for category in menu['offerings']}
    for user, choices in menu['orders'].items():
        for course, meals in choices.items():
            if course not in summary:
                continue
            for meal, amount in meals.items():
                if meal not in summary[course]:
                    continue
                summary[course][meal] += amount
    
    menu_message = ""
    for course, meals in summary.items():
        if not sum(meals.values()):
            continue
        menu_message += f"{course}\n"
        for meal, amount in meals.items():
            if not amount:
                continue
            menu_message += f"\t{amount}x {meal}\n"

    return menu_message


def generate_code(menu_codes: list):
    code = "".join(random.choices(string.ascii_uppercase, k=5))
    while code in menu_codes:
        code = random.choices(string.ascii_uppercase, k=5)

    return code


def upload_to_pantry(menu_code, menu: dict) -> bool:
    # Post a new menu (or overwrite one with the same code)
    try:
        result = requests.post(
            f"https://getpantry.cloud/apiv1/pantry/17474c8e-ea5a-4857-a468-744bad4d466b/basket/{menu_code}",
            data=json.dumps(menu["offerings"]),
            headers={"Content-Type": "application/json"}
        )
        if result.status_code != requests.codes.ok:
            return False
        else:
            return True
    except:
        return False


def delete_from_pantry(menu_code: str) -> bool:
    # Remove a menu
    try:
        result = requests.delete(
            f"https://getpantry.cloud/apiv1/pantry/17474c8e-ea5a-4857-a468-744bad4d466b/basket/{menu_code}"
        )
        if result.status_code != requests.codes.ok:
            return True
    except:
        return False
    return False
