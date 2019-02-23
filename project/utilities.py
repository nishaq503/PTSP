

class Switch(object):
    """
    Switch statements for python
    """

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """
        returns the matched method once, then stop
        :return:
        """
        yield self.match
        raise StopIteration

    def match(self, *args):
        """
        indicate whether or not to enter a case
        :param args: arguments
        :return: bool whether or not to enter case
        """
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False
