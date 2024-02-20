from booyah.db.base_seed import BaseSeed

class Seed(BaseSeed):
    def __init__(self):
        self.load_models(globals())

    def run(self):
        pass
