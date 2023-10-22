from typing import List, Dict, Any


def make_tree(n: int, s: int) -> str:
    """Returns string representing a tree"""
    tree = ""
    for i in range(n):
        for a in range(n - i):
            tree = tree + " "
        tree = tree + "["
        # Added reduce length to half the width (didn't look good on email)
        reduce_length = 0
        for l in range(i << 1):
            if i == n - 1:
                reduce_length = reduce_length + 1
                if reduce_length % 2 == 0:
                    # tree = tree + "_"  # This leads to inconsistent sizing in some emails
                    tree = tree + "~"
            else:
                reduce_length = reduce_length + 1
                if reduce_length % 2 == 0:
                    tree = tree + "~"
        tree = tree + "]\n"
    for o in range(s):
        for i in range(n):
            tree = tree + " "
        tree = tree + "[]\n"
    return tree


def show_dict(dict: Dict[str, Any]) -> str:
    """Output Dictionary Content into String"""
    return "\n".join([f"{key}: {value}" for key, value in dict.items()])


def str_with_ands_between(names: List[str]) -> str:
    return " and ".join(names)
