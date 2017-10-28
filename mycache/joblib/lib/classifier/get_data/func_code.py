# first line: 22
@mem.cache
def get_data():
    data = load_svmlight_file("/tmp/teste.libsvm")
    return data[0], data[1]
