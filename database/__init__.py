from bson import ObjectId
from pymongo import MongoClient
from slugify import slugify
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
  settings_collection = client[config.DATABASE_NAME][config.SETTINGS_COLLECTION_NAME]

  found = settings_collection.find_one({
    "cluster_defined": True
  })

  if found:
    print("Clusters ya se han definido")
    return

  for laptop in laptop_list:
    collection.update_one(
      { "_id": ObjectId(laptop["_id"]) },
      {
        "$set": { "cluster": laptop["cluster"] },
      }
    )

  settings_collection.insert_one({
    "cluster_defined": True
  })
  print("Laptops actualizadas!")

def find_category(category):
  client = get_client()
  collection = client[config.DATABASE_NAME][config.CATEGORIES_COLLECTION_NAME]
  slug = slugify(category)
  found = collection.find_one({
    "slug" : { "$eq" : slug }
  })
  return found

def insert_category(category, cluster):
  client = get_client()
  collection = client[config.DATABASE_NAME][config.CATEGORIES_COLLECTION_NAME]
  slug = slugify(category)
  result = collection.insert_one({
      "name": category,
      "slug": slug,
      "clusters": [int(cluster)]
  })
  return result.acknowledged

def find_edge_laptops():
  client = get_client()
  collection = client[config.DATABASE_NAME][config.LAPTOPS_COLLECTION_NAME]
  # @TODO Cambiar los valores dinamicamente
  columns = {
    "manufacturer": 1,
    "model": 1,
    "cpu": 1,
    "storage": 1,
    "gpu": 1,
    "ram_size": 1,
    "cluster": 1,
    "price": 1,
  }
  laptop_cluster_0 = collection.find_one({ "cluster" : 0 }, columns)
  laptop_cluster_1 = collection.find_one({ "cluster" : 1 }, columns)
  laptop_cluster_2 = collection.find_one({ "cluster" : 2 }, columns)
  laptop_cluster_3 = collection.find_one({ "cluster" : 3 }, columns)
  laptop_cluster_4 = collection.find_one({ "cluster" : 4 }, columns)
  return [
    laptop_cluster_0,
    laptop_cluster_1,
    laptop_cluster_2,
    laptop_cluster_3,
    laptop_cluster_4
  ]

def find_laptops(cluster, budget = 0):
  client = get_client()
  collection = client[config.DATABASE_NAME][config.LAPTOPS_COLLECTION_NAME]

  match = {
    "cluster": cluster
  }

  if budget > 0:
    match["price"] = { "$lte": budget }

  cursor = collection.aggregate([
    { "$match": match },
    { "$sample": { "size": 3 } }
  ])

  return list(cursor)

"""
Funcion para insertar los valores dados por los usuarios de nivel de satisfaccion
"""
def insert_satisfaction(satisfaction):
  client = get_client()
  collection = client[config.DATABASE_NAME][config.SATISFACTION_COLLECTION_NAME]
  result = collection.insert_one({
      "satisfaction": satisfaction,
  })
  return result.acknowledged

"""
Funcion para obtener el promedio de satisfaccion en la base de datos
"""
def get_avg_satisfaction():
  client = get_client()
  collection = client[config.DATABASE_NAME][config.SATISFACTION_COLLECTION_NAME]
  result = collection.aggregate([
    {
      "$group": {
        "_id": None,
        "avg_val": {
          "$avg": "$satisfaction"
        }
      }
    }
  ])

  count = collection.count_documents({})
  entries = list(result)

  if len(entries) == 0:
    return {
      "count": 0,
      "avg": 0
    }

  return {
    "count": count,
    "avg": entries[0]["avg_val"]
  }
