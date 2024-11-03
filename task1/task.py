import json
import sys

graph = dict()
neighbours_map = dict()
child_map = dict()
visited = list()
general = ""


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
    return keys


def main(json_str: str):
    json_to_graph(json.loads(json_str))
    child_map[general] = dfs(graph, general)
    neighbours_map[general] = []
    return neighbours_map, child_map


if __name__ == "__main__":
    example_str = """{
            "1": {
                "2": {
                    "3": {
                        "5": {},
                        "6": {}
                    },
                    "4": {
                        "7": {},
                        "8": {}
                    }
                },
                "9": {
                    "10": {
                        "11":{},
                        "12":{}
                    },
                    "13":{}
                }
            }
        }"""

    neighbours, children = main(example_str)
    print("Братья:")
    for node in sorted(neighbours_map.keys(), key=lambda x: int(x)):
        print(f"{node}: {neighbours_map[node]}")
    print("Потомки:")
    for node in sorted(child_map.keys(), key=lambda x: int(x)):
        print(f"{node}: {child_map[node]}")
