from itertools import product
def recur_get_states(dic: dict, keys: list[str], remain: list[str]):
    if len(keys) == 1:
        return [[remain.append(dic[keys[0]]) for i in dic[keys[0]]]]

    fn = []
    for k in keys:
        for i in range(len(dic[k])):
            remain.append(dic[k][i])
            r = recur_get_states(dic, keys[1:], remain)
            fn += r
    return fn

dic = {
    'a': [1, 2, 3],
    'b': [4, 5, 6],
    'c': [7, 8, 9]
}

for items in product(*dic.values()):
    print(items)
