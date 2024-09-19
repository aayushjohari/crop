from pymongo import MongoClient
connectionstring = "mongodb+srv://aayushjohari0403:FnNFgW9QjZ69IHgt@farmerdb.nczd5.mongodb.net/?retryWrites=true&w=majority&ssl=true&appName=FARMERDB"

client = MongoClient(connectionstring) #client == conn
database = client['farmer']
collection = database['FarmerData']

documents = collection.find()  # select * from table;
for document in documents: 
    print(document) 
print("thank you!")