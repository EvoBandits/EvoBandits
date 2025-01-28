from gmab.utils.singleton import Singleton


def test_singleton_property() -> None:
    s1 = Singleton()
    s2 = Singleton()
    assert s1 == s2  # objects are the same = Singleton is created exactly once


def test_reset() -> None:
    s1 = Singleton()
    Singleton.reset()
    s2 = Singleton()
    assert s1 is not s2  # objects are separate Singletons since reset was called
