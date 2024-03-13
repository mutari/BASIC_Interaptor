def get_file_input(name):
    cmList = []
    f = open(name, "r")
    for x in f:
        cmList.append(x + " ")
    return cmList


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
