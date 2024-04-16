import typing
import conversion
class Message():
    def __init__(self,arr:typing.List[int]):
        self.arr = arr

    def get_string_message(self):
        return conversion.intarray_to_str(self.arr)

    def get_int_message(self):
        return self.arr
