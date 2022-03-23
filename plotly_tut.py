from collections import Counter

# x = {'both1':1, 'both2':2, 'only_x': 100 }
# y = {'both1':10, 'both2': 20, 'only_y':200 }

test={'both1':1, 'both2':2, 'only_x': 100 }

def count_dict():
    test.update(dict(Counter(test)+Counter({'both1':1, 'both2':2, 'only_x': 100 })))

count_dict()
print(test)
