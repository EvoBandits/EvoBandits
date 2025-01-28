class Singleton:
    """
    A singleton class that ensures only one instance of the class exists.

    This design pattern restricts the instantiation of a class to a single object. The
    `__new__` method is overridden to check if an instance already exists. If it does,
    the existing instance is returned; otherwise, a new instance is created and stored.

    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def reset(cls):
        """Resets the singleton instance, allowing the creation of a new instance."""
        cls._instance = None
