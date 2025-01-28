from gmab.utils.singleton import Singleton


def test_singleton_property() -> None:
    s1 = Singleton()
    s2 = Singleton()
    assert s1 == s2  # Both variables reference the same instance


def test_reset() -> None:
    s1 = Singleton()
    Singleton.reset()
    s2 = Singleton()
    assert s1 is not s2  # The new instance is different from the previous one
