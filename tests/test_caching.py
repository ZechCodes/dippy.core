from bevy import Context
from dippy.core.cache.manager import CacheManager
from dippy.core.model import Model, Field


def test_cache_controller():
    class TestModelA(Model, cache_type="test_model_a"):
        id: int = Field(index=True)

    class TestModelB(Model, cache_type="test_model_b"):
        id: int = Field(index=True)
        name: str

    manager = Context().build(CacheManager)
    manager.update(TestModelA, {"id": 0})
    manager.update(TestModelA, {"id": 1})
    manager.update(TestModelB, {"id": 10, "name": "Bob"})

    assert manager.get(TestModelA, 2) is None
    assert isinstance(manager.get(TestModelA, 0), TestModelA)
    assert manager.get(TestModelB, 1) is None
    assert isinstance(manager.get(TestModelB, 10), TestModelB)
    assert manager.get(TestModelB, 10).name == "Bob"
    assert manager.get(TestModelA, 1).id == 1


def test_complex_attributes():
    class Child(Model, cache_type="child"):
        id: int = Field(index=True)

    class Parent(Model):
        child: Child

    context = Context()
    cache = context.build(CacheManager)
    context.add(cache)
    parent = context.build(Parent, {"child": {"id": 1}})

    assert isinstance(parent.child, Child)


def test_complex_container_attributes():
    class Child(Model, cache_type="child"):
        id: int = Field(index=True)

    class Parent(Model):
        children: list[Child]

    context = Context()
    cache = context.build(CacheManager)
    context.add(cache)
    parent = context.build(Parent, {"children": [{"id": 1}, {"id": 2}]})

    assert isinstance(parent.children, list)
    assert len(parent.children) == 2
    assert isinstance(parent.children[0], Child)


def test_complex_container_attributes_tuple():
    class Child(Model, cache_type="child"):
        id: int = Field(index=True)

    class Parent(Model):
        children: tuple[Child]

    context = Context()
    cache = context.build(CacheManager)
    context.add(cache)
    parent = context.build(Parent, {"children": [{"id": 1}, {"id": 2}]})

    assert isinstance(parent.children, tuple)
    assert len(parent.children) == 2
    assert isinstance(parent.children[0], Child)
