import pickle


def to_pickle(text):
    pickle_out = open("user_input.pickle", "wb")
    pickle.dump(text, pickle_out)
    pickle_out.close()
    '''
    file = open('user_input.txt', 'w')
    file.writelines(text)
    file.close()'''

# File('Hello')


def fetch_data():
    file = open("user_input.pickle", "rb")
    data = pickle.load(file)
    file.close()
    return data
