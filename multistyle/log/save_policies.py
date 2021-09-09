import pickle


class SaveData:

    @staticmethod
    def save_data(data, filename):
        filehandler = open(filename, 'w')
        pickle.dump(data, filehandler)
        filehandler.close()


