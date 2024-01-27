import json
from collections import defaultdict
import random
import string
import requests

def parse_menu(text : str) -> dict:
    KEYWORDS = ["FIRST", "SECOND", "CONTOUR", "SWEET", "DRINK"]
    
    # Split the text and filter out possible empty rows, remove the first, the command
    tokens = list(filter(lambda s: len(s)>0, text.split("\n")))[1:]
    
    # The first token must be the menu name
    # title = tokens[0].strip()
    title = "Offerings"
    menu = { "Offerings": {}, "Active" : True}
    
    curr_level = ""
    curr_dishes = []
    for token in tokens[1:]:
        # Sanitize
        token = token.strip()
        
        if token in KEYWORDS:
            # If it is not the first menu level, save the previous with all of its dishes
            if curr_level != "":
                menu[title].update({curr_level : curr_dishes})
                curr_dishes = []
            curr_level = token
        
        else:
            curr_dishes.append(token)
            
    # To add the last one
    menu[title].update({curr_level : curr_dishes})    
    
    return menu
    
def recap(sender : str, menu_code : str) -> str:  
    orders = json.load(open(".\\Data\\order.json", "r")) 
    
    # TODO add the selection by menu code
    orders = orders[menu_code]
    
    recap_dict = defaultdict(lambda: 0)
    
    for single_order in orders.values():
        for plate, amount in single_order.items():
            recap_dict[plate] += amount

    recap_dict = json.dumps(dict(recap_dict))
    
    return recap_dict
        
def generate_code(menu_codes: list):
    code = "".join(random.choices(string.ascii_uppercase, k=5)   )
    while code in menu_codes:
        code = random.choices(string.ascii_uppercase, k=5) 
    
    return code

def load_menu(menu_code, menu : dict) -> bool:
    # Post a new menu (or overwrite one with the same code)
    try:
        result = requests.post(
            f"https://getpantry.cloud/apiv1/pantry/17474c8e-ea5a-4857-a468-744bad4d466b/basket/{menu_code}",
            data=json.dumps(menu["Offerings"]),
            headers={"Content-Type":"application/json"}
        )
        if result.status_code != requests.codes.ok:
            return  False
        else:
            return True
    except:
        return False
