# handles adapting navigation of modules 

# abstracts a get_data to be accessed by the modules so they can display current database table stats
class DataHandler(ABC):
    @abstractmethod
    def get_data(self, data_type):
        pass

# this handles taking the abstracted data value that was requested and retrieve it from the database
# kinda like an adapter?
class MockDataHandler(DataHandler):
    def __init__(self, data):
        self.data = data

    def get_data(self, data_type):
        return self.data.get(data_type, {})
        # edit this to access the current database table