from abc import abstractmethod

class Command():
    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def set_arguments(self, arguments: str, user_id: int):
        pass

    @abstractmethod
    def execute(self, dbUrl):
        pass



    