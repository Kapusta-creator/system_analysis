import json
import sys
from pprint import pprint

graph = dict()
neighbours_map = dict()
child_map = dict()
visited = list()
nodes = set()
general = ""


def get_r1(node, graph):
    return len(graph[node])


def get_r2(node, graph):
    for ribsList in graph.values():
        if node in ribsList:
            return 1
    return 0


def get_r3(node, graph, child_map):
    return len(child_map[node]) - len(graph[node])


def get_r4(node, child_map):
    cnt = 0
    for children in child_map.values():
        if node in children:
            cnt += 1
    return max(0, cnt - 1)


def get_r5(node, neighbours):
    return len(neighbours[node])


def fill_neighbours(neighbours):
    for i in range(len(neighbours)):
        neighbours_map[neighbours[i]] = list()
        for j in range(len(neighbours)):
            if i != j:
                neighbours_map[neighbours[i]].append(neighbours[j])


def dfs(g, v):
    visited.append(v)
    fill_neighbours(g[v])
    children = list()
    for node in g[v]:
        children.append(node)
        if node not in visited:
            node_children = dfs(g, node)
            child_map[node] = node_children
            children.extend(node_children)
    return children


def json_to_graph(json_graph):
    keys = list()
    global general
    for key, val in json_graph.items():
        if general == "":
            general = key
        keys.append(key)
        children_keys = json_to_graph(val)
        graph[key] = children_keys
    for key in keys:
        nodes.add(key)
    return keys


def main(json_str: str):
    json_to_graph(json.loads(json_str))
    child_map[general] = dfs(graph, general)
    neighbours_map[general] = []

    extensional_lengths = dict()
    for node in nodes:
        extensional_lengths[node] = [
            get_r1(node, graph),
            get_r2(node, graph),
            get_r3(node, graph, child_map),
            get_r4(node, child_map),
            get_r5(node, neighbours_map)
        ]

    return extensional_lengths


if __name__ == "__main__":
    example_str = """{
        "1": {
            "2": {
            },
            "3": {
                "4": {},
                "5": {}
            }
        }
    }"""
    lengths = main(example_str)
    for node in sorted(lengths.keys(), key=lambda x: int(x)):
        print(f"{node}: {lengths[node]}")



