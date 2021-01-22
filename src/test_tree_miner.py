import pytest

from .tree_miner import Node


@pytest.fixture(scope="function")
def singleton():
    return Node(name='A')


@pytest.fixture(scope='function')
def abc_tree():
    return Node(
        name='A',
        children=(
            Node(
                name='B',
                children=()
            ),
            Node(
                name='C',
                children=()
            )
        )
    )


@pytest.fixture(scope='function')
def abcdef_tree():
    return Node(
        name='A',
        children=(
            Node(name='B'),
            Node(
                name='C',
                children=(
                    Node(name='D'),
                    Node(name='E'),
                )),
            Node(name='F'),
        )
    )


@pytest.fixture(scope="function")
def tree_from_survey():
    return Node(
        name='A',
        children=(
            Node(
                name='B',
                children=(
                    Node(name='D'),
                    Node(name='E'),
                    Node(name='F'),
                )
            ),
            Node(
                name='C',
                children=(
                    Node(name='G'),
                )
            )
        )
    )


def test_tree_instantiation(abc_tree):
    assert abc_tree


def test_repr(abc_tree):
    assert repr(abc_tree) == "Node(name='A', children=(Node(name='B'), Node(name='C')))"


def test_dfs_string(singleton, abc_tree, abcdef_tree, tree_from_survey):
    assert singleton.dfs_string == "A -1"
    assert abc_tree.dfs_string == "A B -1 C -1 -1"
    assert abcdef_tree.dfs_string == "A B -1 C D -1 E -1 -1 F -1 -1"
    assert tree_from_survey.dfs_string == "A B D -1 E -1 F -1 -1 C G -1 -1 -1"


def test_tree_equality():
    assert Node('A') == Node('A')
    assert Node('A') != Node('B')
    assert Node('A', children=(Node('B'), Node('C'))) == Node('A', children=(Node('B'), Node('C')))
    assert Node('A', children=(Node('B'), Node('C'))) != Node('A', children=(Node('C'), Node('B')))


def test_bottom_up_subtree():
    assert Node('A') <= Node('A')
    assert not Node('A') < Node('B')
    assert Node('B') <= Node('A', children=(Node('B'),))
    assert Node('B') < Node('A', children=(Node('B'),))
    assert Node('A') >= Node('A')
    assert not Node('B') > Node('A')
    assert Node('A', children=(Node('B'),)) >= Node('B')
    assert Node('A', children=(Node('B'),)) > Node('B')


def test_enumerate_subtrees(singleton, abc_tree, tree_from_survey):
    assert singleton.subtrees == [singleton]
    assert abc_tree.subtrees == [
        abc_tree,
        Node('B'),
        Node('C')
    ]
    assert tree_from_survey.subtrees == [
        tree_from_survey,
        Node(
            name='B',
            children=(
                Node(name='D'),
                Node(name='E'),
                Node(name='F'),
            )
        ),
        Node('D'),
        Node('E'),
        Node('F'),
        Node(
            name='C',
            children=(
                Node(name='G'),
            )
        ),
        Node('G')
    ]

