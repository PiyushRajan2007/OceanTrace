from app.services.demo_repository import DemoRepository


class ProviderFactory:
    def __init__(self):
        self.demo_repository = DemoRepository()

    def repository(self):
        return self.demo_repository


provider_factory = ProviderFactory()
