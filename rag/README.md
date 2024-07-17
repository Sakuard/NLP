## Introduction
This document outlines the steps to set up persistent storage, tokenize and vectorize Traditional Chinese text, and create document embeddings.

Difficulty : ★★★☆☆
Prerequisite Knowledge : NLP, vectorize, Embeddings models

## Table of Contents
1. [Goal](#goal)
2. [Missions](#missions)
3. [Prerequisites](#prerequisites)
4. [Installation and Setup](#installation-and-setup)
   - [Pre-installation](#pre-installation)
   - [Milvus Setup](#milvus-setup)
5. [Usage](#usage)
   - [Basic Connection Setup](#basic-connection-setup)
   - [Database Operations](#database-operations)
   - [Database Role Permissions](#database-role-permissions)
6. [FAQs](#faqs)
7. [Contact Information](#contact-information)
8. [Reference](#ref)

## Goal
<p id='goal'></p>

Build a Backend Server with RESTFul API call to
1. Documents embeddings
2. Response

## Missions
<p id='missions'></p>

- Persistent Storage (Milvus)
- Traditional Chinese ***tokenize*** & ***vectorize*** ([ckip-transformers](https://github.com/ckiplab/ckip-transformers?tab=readme-ov-file))
- Document embeddings


## Prerequisites
Before starting, ensure you have the following:
<p id='prerequisites'></p>

- Python installed
- Docker installed
- Internet connection for downloading dependencies

## Installation and Setup
<p id='installation-and-setup'></p>

### Pre-installation
Install necessary packages and set up Milvus:
<p id='pre-installation'></p>

```bash=
pip install ollama chromadb

# Milvus in Docker
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
bash standalone_embed.sh start

# Docker-compose
curl -L https://github.com/milvus-io/milvus/releases/download/v2.4.5/milvus-standalone-docker-compose.yml -o docker-compose.yml
```

### Milvus Setup
Basic connection setup:
<p id='milvus-setup'></p>

```python=
from pymilvus import connections, db

db_name = "docs"
milvus_conn = connections.connect(
    host="127.0.0.1",
    port="19530"
)

if db_name not in db.list_database():
    db.create_database(db_name)

db.using_database(db_name)
db.list_database()
```

## Usage
<p id='usage'></p>

### Basic Connection Setup
<p id='basic-connection-setup'></p>

```python=
from pymilvus import connections, db

conn = connections.connect(host="127.0.0.1", port=19530)
```

### Database Operations
<p id='database-operations'></p>

```python=
from pymilvus import connections, db

conn = connections.connect(host="127.0.0.1", port=19530)

database = db.create_database("book")
db.using_database("book")
db.list_database()
db.drop_database("book")
```

### Database Role Permissions
<p id='database-role-permissions'></p>

```python=
from pymilvus import connections, Role

_URI = "http://localhost:19530"
_TOKEN = "root:Milvus"
_DB_NAME = "default"

def connect_to_milvus(db_name="default"):
    print(f"Connecting to Milvus\n")
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
```

## FAQs
<p id='faqs'></p>

1. **What is Milvus?**
   - Milvus is an open-source vector database built for scalable similarity search and AI applications.

2. **How do I install dependencies?**
   - Follow the steps in the [Pre-installation](#pre-installation) section.

## Contact Information
<p id='contact-information'></p>

For further assistance, please contact:
- **Email:** matt.web.tw@gmail.com

<p id='ref'></p>

Ref: [YungHuiHsu](https://hackmd.io/@YungHuiHsu)