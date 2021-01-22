from collections import defaultdict

class Node:
    """Node in a rooted, ordered tree"""
    def __init__(self, name, children=None):
        self.name = name
        self.children = children if children is not None else ()
        self._dfs_string = None

    def __repr__(self):
        if self.children:
            children = repr(self.children)
            return f"{self.__class__.__name__}(name='{self.name}', children={children})"
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __eq__(self, other):
        return self.dfs_string == other.dfs_string

    def __lt__(self, other):
        return self.dfs_string in other.dfs_string and self != other

    def __le__(self, other):
        return self.dfs_string in other.dfs_string

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return other <= self

    @property
    def dfs_string(self):
        if self._dfs_string:
            return self._dfs_string
        tokens = []
        tokens = self._compute_dfs_string(tokens)
        self._dfs_string = " ".join((str(x) for x in tokens))
        return self._dfs_string

    def _compute_dfs_string(self, tokens):
        tokens.append(self.name)
        for child in self.children:
            tokens = child._compute_dfs_string(tokens)
        tokens.append(-1)
        return tokens

    @property
    def prefix_equivalence_class(self):
        tokens = self.dfs_string.split(" ")
        return " ".join(tokens[:-2])

    @property
    def subtrees(self):
        # enumerate subtrees using pre-order traversal
        nodes = []
        return self._subtrees(nodes)

    def _subtrees(self, nodes):
        nodes.append(self)
        for node in self.children:
            nodes = node._subtrees(nodes)
        return nodes


def bottom_up_subtree_frequencies(trees):
    # enumerate all bottom up subtrees
    SUBTREE = 0
    TREE_IDX = 1
    SUBTREE_NODE_IDX = 2
    subtrees = []
    n_subtrees = 0
    for tree_idx, tree in enumerate(trees):
        for subtree_node_idx, subtree in enumerate(tree.subtrees):
            subtrees.append((subtree, tree_idx, subtree_node_idx))
            n_subtrees += 1
    # sort subtrees
    subtrees.sort(key=lambda t: t[SUBTREE])
    # compute frequencies
    results = {}
    for t in subtrees:
        subtree, tree_idx, subtree_node_idx = t[SUBTREE], t[TREE_IDX], t[SUBTREE_NODE_IDX]
        key = str(subtree)
        if key not in results:
            results[key] = {
                "occurences": [],
                "frequency": 0,
            }
        results[key]['occurences'].append({'tree_index': tree_idx, 'subtree_node_index': subtree_node_idx})
        results[key]['frequency'] += 1 / n_subtrees

    results = [
        {
            'subtree': subtree,
            **stats
        }
        for subtree, stats in results.items()
    ]
    return {
        'trees': [str(tree) for tree in trees],
        'frequencies': list(sorted(results, key=lambda d: d['frequency'], reverse=True))
    }


if __name__ == '__main__':
    trees = [
        Node('A'),
        Node('B'),
        Node('C'),
        Node('A', children=(Node('B'), )),
        Node('A', children=(Node('C'), )),
        Node('A', children=(Node('B'), Node('C'))),
    ]
    from pprint import pprint
    pprint(bottom_up_subtree_frequencies(trees))
