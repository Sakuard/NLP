# Goal
- Persistent Storage
- Traditional Chinese ***tokenize*** & ***vectorize***
- Document embeddings


## embedding-models

### Pre-install
```bash=
pip install ollama chromadb

# Milvus
# right in Docker op
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
bash standalone_embed.sh start

# Docker-compose
curl -L https://github.com/milvus-io/milvus/releases/download/v2.4.5/milvus-standalone-docker-compose.yml -o docker-compose.yml
```
---
### Milvus Setup
basic connection setup
```Python=
from pymilvus import connections, db

db_name = "docs"
milvus_conn = connections.connect(
    host="127.0.0.1"
    port="19530"
    # db_name = db_name
)

if db_name not in db.list_database():
    db.create_database(db_name)

db.using_database(db_name)
db.list_database()
```

DB Ops
```Python=
from pymilvus import connections, db

conn = connections.connect(host="127.0.0.1", port=19530)

database = db.create_database("book")
db.using_database("book")
db.list_database()
db.drop_database("book")
```

DB Role Permissions
```Python=
from pymilvus import connections, Role

_URI = "http://localhost:19530"
_TOKEN = "root:Milvus"
_DB_NAME = "default"


def connect_to_milvus(db_name="default"):
    print(f"connect to milvus\n")
    connections.connect(
        uri=_URI,
        token=_TOKEN,
        db_name=db_name
    )
_ROLE_NAME = "test_role"
_PRIVILEGE_INSERT = "Insert"

connect_to_milvus()
role = Role(_ROLE_NAME)
role.create()

connect_to_milvus()
role.grant("Collection", "*", _PRIVILEGE_INSERT)
print(role.list_grants())
print(role.list_grant("Collection", "*"))
role.revoke("Global", "*", _PRIVILEGE_INSERT)

# This role will have the insert permission of all collections under foo db,
# excluding the insert permissions of collections under other dbs
role.grant("Collection", "*", _PRIVILEGE_INSERT)
print(role.list_grants())
print(role.list_grant("Collection", "*"))
role.revoke("Global", "*", _PRIVILEGE_INSERT)
```