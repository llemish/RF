class int(int):
    RESERVED_NAMES = [1, 2, 3]
    def __init__(self, val):
        super().__init__()
        self.val = round(float(val))

    def __str__(self):
        return str(self.val)

    def __add__(self, other):
        return self.val - other.val

    def __eq__(self, other):
        if abs(self.val - other.val) <= 3:
            print(self.RESERVED_NAMES)
            ans = True
        else:
            ans = False
        return ans



a = int(input('a: '))
b = int(input('b: '))
print(a + b)























