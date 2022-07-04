from examples.prepare.mocks import InsertData


class RunExample:

    def __init__(self):
        self.mock = InsertData()

    def prepare_data(self):
        self.mock.insert_person()
        self.mock.insert_books()

