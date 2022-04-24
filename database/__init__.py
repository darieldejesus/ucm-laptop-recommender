from bson import ObjectId
from pymongo import MongoClient
import pandas
import config

def get_client():
  client = MongoClient(config.DATABASE_CONNECTION_STRING)
  return client

def init_laptops():
  client = get_client()
  databases = client.list_database_names()

  if config.DATABASE_NAME in databases:
    db = client[config.DATABASE_NAME]
    collections = db.list_collection_names()
    if config.LAPTOPS_COLLECTION_NAME in collections:
      print("Coleccion de laptops encontrado.")
      return

  print("Coleccion de laptops no encontrado. Cargando los registros correspondientes")
  laptops_df = pandas.read_csv("notebook/laptops.csv")
  collection = client[config.DATABASE_NAME][config.LAPTOPS_COLLECTION_NAME]
  for index, row in laptops_df.iterrows():
    collection.insert_one({
      "manufacturer": row["Manufacturer"],
      "model": row["Model.Name"],
      "category": row["Category"],
      "screen": row["Screen"],
      "cpu": row["CPU"],
      "storage": row["Storage"],
      "gpu": row["GPU"],
      "os": row["Operating.System"],
      "weight": float(row["Weight"]),
      "price": float(row["Price"]),
      "cpu_speed": float(row["CPU.Speed"]),
      "storage_type": int(row["Storage.Type"]),
      "gpu_rank": int(row["GPU.Rank"]),
      "storage_size": int(row["Storage.Size"]),
      "ram_size": int(row["RAM.Size"]),
      "screen_size": float(row["Screen.Size"]),
      "category_type": int(row["Category.Type"]),
      "gpu_speed": float(row["GPU.Speed"]),
      "performance": float(row["CPU.Speed"]) * int(row["RAM.Size"]) + float(row["GPU.Speed"])
    })

  laptops_count = collection.count_documents({})
  print("Se han insertado {} documentos.".format(laptops_count))

def load_laptops_for_cluster():
  client = get_client()
  collection = client[config.DATABASE_NAME][config.LAPTOPS_COLLECTION_NAME]
  cursor = collection.find({}, {
    "_id": 1,
    "performance": 1,
    "price": 1
  })
  laptop_list = list(cursor)
  for index, laptop in enumerate(laptop_list):
    laptop_list[index]["_id"] = str(laptop["_id"])
  return laptop_list

def update_laptops_with_cluster(laptop_list):
  client = get_client()
  collection = client[config.DATABASE_NAME][config.LAPTOPS_COLLECTION_NAME]

  for laptop in laptop_list:
    collection.update_one(
      { "_id": ObjectId(laptop["_id"]) },
      {
        "$set": { "cluster": laptop["cluster"] },
      }
    )
  print("Laptops actualizadas!")
