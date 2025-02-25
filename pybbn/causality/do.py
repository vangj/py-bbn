import itertools
from collections import namedtuple
from typing import Any, Dict, List

import networkx as nx

Graph = namedtuple("Graph", "u, d")


def get_undirected_graph(d: nx.DiGraph) -> nx.Graph:
    u = nx.Graph()

    for n in d.nodes():
        u.add_node(n)

    for p, c in d.edges():
        u.add_edge(p, c)

    return u


def get_graph(d: nx.DiGraph) -> Graph:
    u = get_undirected_graph(d)
    g = Graph(u, d)
    return g


def get_all_paths(g: Graph, start: Any, stop: Any) -> Any:
    return nx.all_simple_paths(g.u, start, stop)


def get_path_triplets(path: List[Any]) -> List[List[Any]]:
    if len(path) < 3:
        return [path]
    else:
        return [path[i : i + 3] for i in range(0, len(path) - 2)]


def get_triplet_type(g: Graph, x: Any, z: Any, y: Any) -> str:
    x_children = set(g.d.successors(x))
    z_children = set(g.d.successors(z))
    y_children = set(g.d.successors(y))

    if z in x_children and y in z_children:
        return "serial"
    if z in y_children and x in z_children:
        return "serial"
    if x in z_children and y in z_children:
        return "diverging"
    if z in x_children and z in y_children:
        return "converging"
    raise Exception(f"cannot determine triplet configuration: x={x}, z={z}, y={y}")


def is_active_triplet(g: Graph, x: Any, z: Any, y: Any, evidence=set()):
    triplet_type = get_triplet_type(g, x, z, y)

    if triplet_type in {"serial", "diverging"}:
        if z in evidence:
            return False
        else:
            return True
    else:
        z_set = nx.descendants(g.d, z)
        z_set.add(z)

        if len(z_set & evidence) > 0:
            return True
        else:
            return False


def is_active_path(g: Graph, path: List[Any], evidence=set()):
    if len(path) < 3:
        if path[0] in evidence or path[-1] in evidence:
            return False
        else:
            return True

    path_triplets = get_path_triplets(path)

    for x, z, y in path_triplets:
        if not is_active_triplet(g, x, z, y, evidence):
            return False
    return True


def get_colliders(g: Graph, path: List[Any]):
    if len(path) < 3:
        return []

    path_triplets = get_path_triplets(path)
    return [
        z for x, z, y in path_triplets if get_triplet_type(g, x, z, y) == "converging"
    ]


def get_paths(g: Graph, x: Any, y: Any) -> List[Dict[str, Any]]:
    def is_backdoor_path(p):
        if g.d.has_edge(p[1], p[0]):
            return True
        return False

    def is_frontdoor_path(p):
        if g.d.has_edge(p[0], p[1]):
            return True
        return False

    def get_path_metadata(p):
        xy = {x, y}
        colliders = get_colliders(g, p)
        confounders = list(set(p) - xy - set(colliders))

        return {
            "x": x,
            "y": y,
            "z": confounders,
            "path": p,
            "is_active": is_active_path(g, p),
            "colliders": colliders,
            "backdoor": is_backdoor_path(p),
            "frontdoor": is_frontdoor_path(p),
        }

    paths = get_all_paths(g, x, y)
    return [get_path_metadata(p) for p in paths]


def get_all_confounders(g: Graph, x: Any, y: Any) -> set[Any]:
    paths = get_paths(g, x, y)

    colliders = [
        p["colliders"]
        for p in paths
        if p["is_active"] is False and p["backdoor"] is True
    ]
    colliders = itertools.chain(*colliders)
    colliders = set(colliders)
    # print(f'{colliders=}')

    descendants = nx.descendants(g.d, x)
    # print(f'{descendants=}')

    exclude = colliders | descendants | {x, y}
    # print(f'{exclude=}')

    candidates = [
        [n for n in p["path"] if n not in exclude]
        for p in paths
        if p["is_active"] is True and p["backdoor"] is True
    ]
    # print(f'{candidates=}')
    candidates = itertools.chain(*candidates)
    candidates = set(candidates)

    return candidates


def find_minimal_confounders(
    g: Graph, path: List[Any], x: Any, y: Any, z: Any
) -> List[Any]:
    keep = []
    for _i, _c in enumerate(z):
        _z = keep + [_c]

        if not is_active_path(g, path, _z):
            if len(keep) < 1:
                keep.append(_c)
                break

    return keep


def get_minimal_confounders(g: Graph, x: Any, y: Any) -> List[Any]:
    paths = get_paths(g, x, y)
    paths = filter(lambda p: p["is_active"] is True and p["backdoor"] is True, paths)

    confounders = [find_minimal_confounders(g, p["path"], x, y, p["z"]) for p in paths]
    confounders = itertools.chain(*confounders)
    confounders = set(confounders)
    return list(confounders)


def find_minimal_mediator(
    g: Graph, path: List[Any], x: Any, y: Any, z: Any
) -> List[Any]:
    colliders = get_colliders(g, path)
    exclude = {x, y} | set(colliders)
    candidates = set(path) - exclude

    keep = []
    for _i, _c in enumerate(candidates):
        _z = keep + [_c]

        if not is_active_path(g, path, _z):
            if len(keep) < 1:
                keep.append(_c)
                break

    return keep


def get_minimal_mediators(g: Graph, x: Any, y: Any) -> List[Any]:
    all_paths = get_paths(g, x, y)
    fontdoor_paths = filter(
        lambda p: p["is_active"] is True and p["frontdoor"] is True, all_paths
    )

    mediators = [
        find_minimal_mediator(g, p["path"], x, y, p["z"]) for p in fontdoor_paths
    ]
    mediators = itertools.chain(*mediators)
    mediators = set(mediators)

    colliders = [p["colliders"] for p in all_paths]
    colliders = itertools.chain(*colliders)
    colliders = set(colliders)

    return list(mediators - colliders)
