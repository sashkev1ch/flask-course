from typing import Dict, List


def validate_creation(users_list: List[Dict[str, str]], new_data: Dict[str, str]) -> Dict[str, str]:

    errors = {}
    emails = [user["email"].lower() for user in users_list]
    names = [user["nickname"].lower() for user in users_list]

    name = new_data.get("nickname") 
    email = new_data.get("email")

    if not name:
        errors["nickname"] = "Set nickname"

    if not email:
        errors["email"] = "Set email"

    if name in names:
        errors["nickname"] = "Already exists"

    if email in emails:
        errors["email"] = "Already exists"

    return errors


def validate_update(users_list: List[Dict[str, str]], new_data: Dict[str, str]) -> Dict[str, str]:

    errors = {}
    emails = [user["email"].lower() for user in users_list if user["id"] != new_data["id"]]
    names = [user["nickname"].lower() for user in users_list if user["id"] != new_data["id"]]

    name = new_data.get("nickname") 
    email = new_data.get("email")
    
    if not name:
        errors["nickname"] = "Can't be empty"

    elif not email:
        errors["email"] = "Can't be empty"

    elif name in names or email in emails:
        errors["nickname"] = "Already exists"
        errors["email"] = "Already exists"

    return errors