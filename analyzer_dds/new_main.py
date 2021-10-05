# from main import Suit


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __gt__(self, other):
        if self.rank > other.rank:
            return True
        else:
            return False

    def __repr__(self):
        return f"{self.suit[0].upper()}{self.rank}"

    def __format__(self, format_spec):
        if format_spec == "full":
            return f"{self.rank} of {self.suit}"
        else:
            return self.__repr__()


# __format__
# __getnewargs__


class Parent:
    def __init__(self, name, callbacks):
        self.name = name
        self.callbacks = callbacks

    def make_older(self):
        self.callbacks["age"]()


class ChildA(Parent):
    def __init__(self, name, age):
        super().__init__(name=name, callbacks={"age": self.pass_year})

        self.age = age

    def pass_year(self):
        self.age += 1


class Time:
    def __init__(self, callbacks):
        self.callbacks = callbacks

    def pass_year(self):
        self.callbacks["age"](43)


class ChildB:
    def __init__(self, name, age):
        self.time = Time(callbacks={"age": self.pass_year})
        self.name = name
        self.age = age

    def pass_year(self, increment=1):
        self.age += increment


if __name__ == "__main__":
    peter = ChildA("peter", 32)
    print(peter.age)
    peter.make_older()
    print(peter.age)

    andi = ChildB("andi", 32)
    print(andi.age)
    andi.time.pass_year()
    print(andi.age)

    # peter.make_older()
    # print(peter.age)

    # sp3 = Card(3, "spade")
    # sp5 = Card(5, "spade")
    # cards = [sp3, sp5]

    # print(sp3 > sp5)
    # print(sp3 < sp5)

    # print(sp3)
    # print(max(cards))
    # print(f"{sp3:full}")
    # print(f"{sp3:ba2z}")

    pass
