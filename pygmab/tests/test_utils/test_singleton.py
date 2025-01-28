from gmab.utils.singleton import Singleton


def test_singleton() -> None:
    s1 = Singleton()
    s2 = Singleton()
    assert s1 == s2  # objects are the same = Singleton is created exactly once
