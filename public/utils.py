def get_choices_value(choices, key):
    for choice in choices:
        if choice[0] == key:
            ret = choice[1]
            break
    return ret