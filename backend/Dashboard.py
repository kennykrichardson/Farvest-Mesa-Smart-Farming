"""Read-only dashboard data adapter."""
class Dashboard:
    def __init__(self, model):
        self.model = model

    def statistics(self):
        return self.model.statistics()

    def crop_rows(self):
        return [crop.statistics() for crop in self.model.crops]

    def farmer_rows(self):
        return [farmer.statistics() for farmer in self.model.farmers]
