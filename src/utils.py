import json
def parse_menu(text):
    KEYWORDS = ["FIRST", "SECOND", "CONTOUR", "SWEET", "DRINK"]
    
    # Split the text and filter out possible empty rows, remove the first, the command
    tokens = list(filter(lambda s: len(s)>0, text.split("\n")))[1:]
    
    # The first token must be the menu name
    title = tokens[0].strip()
    menu = { title: {}}
    
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
    
    
        
    
    