from pymongo import MongoClient

def query_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    
    db = client["mi_base_de_datos"]
    collection = db["mi_coleccion"]

    query = collection.find({})
    
    for document in query:
        print(document)

if __name__ == "__main__":
    query_mongodb()