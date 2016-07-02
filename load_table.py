import pickle

''' read k shortest paths table and print '''
with open('full_test_write.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data = pickle.load(f)

print(data)