def user_age_filter(age: int, setting: dict) -> bool:
    if not setting["boolRequired"]:
        return True
    elif setting["minAge"] <= 0 and setting["maxAge"] >= 100:
        return True
    else:
        if setting["minAge"] <= 0:
            if age <= setting["maxAge"]:
                return True
            else:
                return False
        elif setting["maxAge"] >= 100:
            if age >= setting["minAge"]:
                return True
            else:
                return False
        else:
            if setting["minAge"] <= age <= setting["maxAge"]:
                return True
            else:
                return False
