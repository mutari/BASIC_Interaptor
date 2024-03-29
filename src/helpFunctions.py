def get_file_input(name):
    command_list = []
    f = open(name, "r")
    for x in f:
        command_list.append(x + " ")
    return command_list


def create_hash_map(cm_list):
    cm_map = {}
    for x in cm_list:
        split = x.split(" ")
        number = split[0]
        del split[0]
        if not number.isdecimal():
            continue
        cm_map[number] = " ".join(split)
    return cm_map


def token_row_slice(dic, start, end=None):
    return dict(list(dic.items())[start:end])
