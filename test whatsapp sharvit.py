import pickle
import os

def print_objects():
    objects = []
    with (open("data/whatsapp/wa_sublets.pickle", "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    print(objects)
    #
    # dict_of_sublets = pickle.load(open("data_utils/sublets_from_whatsapp.p", 'rb')) if os.path.exists(
    #     "dict_of_sublets.p") else {}
    # for key in dict_of_sublets.keys():
    #     posts_by_group = dict_of_sublets[key]
    #     text += ([x[0] for x in posts_by_group])

    # posts = pkl.load(open("data_utils/sublets_from_whatsapp.p", "rb"))
    # text, dates, sender_phone, group_name, start_date, end_date, price, location, location, phone_number, rooms = \
    #     [], [], [], [], [], [], [], [], [], [], [],
    # for key in posts.keys():
    #     posts_by_group = posts[key]
    #     text += [x[0] for x in posts_by_group]
    #     print(text)

# dict_of_sublets.p
# data_utils/sublets_from_whatsapp.p


def main():
    print_objects()


if __name__ == "__main__":
    main()