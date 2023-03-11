from pymongo import MongoClient
client = MongoClient('mongodb+srv://nrm4206a:9dfe351b@dbsae.ohuhcxc.mongodb.net/?retryWrites=true&w=majority')

if __name__ == '__main__':
    print(client)