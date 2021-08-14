import abc

class Plugin(metaclass=abc.ABCMeta):
    """
    La clase Plugin implementa la funcionalidad básica del parseado y de la
    robotización.
    """
    @abc.abstractmethod
    def parse(self):
        pass
