import pickle
import os

def print_objects():
    a = pickle.load(open("test_airbnb_db.p", 'rb'))
    for obj in a:
        # print(vars(obj))
        print(obj.name)
    # We can also access instances attributes
    # as list[0].name, list[0].roll and so on.

def main():
    print_objects()


if __name__ == "__main__":
    main()