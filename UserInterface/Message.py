import typing
import conversion


class Message():
    def __init__(self, mode, arr: typing.List[int], received=False):
        self.arr = arr
        self.mode = mode
        self.received = received

    def get_string_message(self):
        return conversion.intarray_to_str(self.arr)

    def get_int_message(self):
        return self.arr

    def get_mode(self):
        return self.mode

    def toString(self):
        sign = "@server " if self.received else "@me "
        return sign + self.get_string_message()
