from data import data


def test_forloop():
    for i in range(10):
        print(i)


def print_titles():
    for prod in data:
        print(prod["title"])


def print_sum():
    sum = 0
    for item in data:
        sum += item["price"]

    print(f"The sum is: {sum}")


def print_test2(limit):
    for item in data:
        if(item["price"] > limit):
            print(f"{item['title']} - ${item['price']}")

def print_categories_list():
    categories = []
    for item in data:
        cat = item["category"]

        if(cat not in categories):
            categories.append(cat)

    print(categories)

def run_test():
    print("Running tests")

    print_titles()
    print_sum()
    print_test2(10)
    print_test2(20)


run_test()
