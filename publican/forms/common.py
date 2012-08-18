
class Filing(object):
    def __init__(self):
        self.pages = []

    def new_page(self, number):
        p = Page(number)
        self.pages.append(p)
        return p


class Page(object):
    def __init__(self, number):
        self.number = number
