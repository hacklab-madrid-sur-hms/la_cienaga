class Plugin(object):
    """
    La clase Plugin implementa la funcionalidad básica del parseado y de la
    robotización.
    """
    def parse(self):
        raise NotImplementedError('subclasses of Plugin must provide a parse() method.')