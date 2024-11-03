import json


def get_elem_to_index(range_list):
    elem_to_index = dict()
    i = 0
    for elem_or_list in range_list:
        if type(elem_or_list).__name__ == "list":
            for elem in elem_or_list:
                elem_to_index[elem] = i
        else:
            elem_to_index[elem_or_list] = i
        i += 1
    return elem_to_index


def get_trans_matrix(mat):
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat))]


def get_range_matrix(elem_to_index):
    range_matrix = [[0 for i in range(len(elem_to_index))] for j in range(len(elem_to_index))]
    for i in range(len(range_matrix)):
        for j in range(len(range_matrix[i])):
            if elem_to_index[i + 1] >= elem_to_index[j + 1]:
                range_matrix[i][j] = 1
    return range_matrix


def mult_matrices(a, b):
    res = [[0 for i in range(len(a))] for j in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            res[i][j] = a[i][j] * b[i][j]
    return res


def main(a: str, b: str):
    r_a = json.loads(a)
    r_b = json.loads(b)
    range_mat_a = get_range_matrix(get_elem_to_index(r_a))
    range_mat_b = get_range_matrix(get_elem_to_index(r_b))
    tr_range_mat_a = get_trans_matrix(range_mat_a)
    tr_range_mat_b = get_trans_matrix(range_mat_b)
    y_ab = mult_matrices(range_mat_a, range_mat_b)
    tr_y_ab = mult_matrices(tr_range_mat_a, tr_range_mat_b)
    core = []
    for i in range(len(y_ab)):
        for j in range(i, len(y_ab[0])):
            if y_ab[i][j] + tr_y_ab[i][j] == 0:
                core.append([i + 1, j + 1])
    return core


if __name__ == "__main__":
    range_json_a = "[1,[2,3],4,[5,6,7],8,9,10]"
    range_json_b = "[[1,2],[3,4,5],6,7,9,[8,10]]"
    print(main(range_json_a, range_json_b))
