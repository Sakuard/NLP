from pymilvus import connections, db, Collection, CollectionSchema, FieldSchema, DataType
import random

# milvus_conn = connections.connect(host="127.0.0.1", port=19530)

database_name = "docs"
collection_name = "quick_setup"
# db.using_database("book")
milvus_conn = connections.connect(
    host="127.0.0.1",
    port="19530",
    # db_name="book"
)

if database_name not in db.list_database():
    db.create_database(database_name)

db.using_database(database_name)
db.list_database()

def switch_database(database_name):
    db.using_database(database_name)

colors = ['green', 'blue', 'yellow', 'red', 'black']
data = []
for i in range(50):
    current_color = random.choice(colors)
    data.append({
        "id": i,
        "vector": [ random.uniform(-1, 1) for _ in range(5)],
        "color": current_color,
        "collor_tag": f"{current_color}_{str(random.randint(1000, 9999))}"
    })


# db.create_collection(
#     collection_name = collection_name,
#     dimension = 5,
#     metric_type = "IP"
# )
id = FieldSchema(
    name = "id",
    dtype = DataType.INT64,
    is_primary = True,
)
vector = FieldSchema(
    name = "vector",
    dtype = DataType.FLOAT_VECTOR,
    dim = 5,
    # index = "IVF_FLAT",
)
color = FieldSchema(
    name = "color",
    dtype = DataType.STRING,
)
color_tag = FieldSchema(
    name = "color_tag",
    dtype = DataType.STRING,
)
schema = CollectionSchema(
    fields = [id, vector, color, color_tag],
    primary_field = "id"
)
collection_name = "quick_setup"

collection = Collection(collection_name)
res = collection.insert(data)

print(res)