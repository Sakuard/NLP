from fastapi import FastAPI
from pydantic import BaseModel
from pymilvus import connections, db

# milvus_conn = connections.connect(host="127.0.0.1", port=19530)

class DatabaseSwitchRequest(BaseModel):
    database_name: str

current_db = "docs"
# db.using_database("book")
milvus_conn = connections.connect(
    host="127.0.0.1",
    port="19530",
    # db_name="book"
)

app = FastAPI()

@app.get("/v1/database")
async def get_database():
    return {"database": current_db}

@app.get("/v1/databases")
async def get_databases():
    return {"databases": db.list_database()}

# @app.get("/v1/databases/{database_name}")

@app.post("/v1/database/switch")
async def switch_database(request: DatabaseSwitchRequest):
    global current_db
    if request.database_name in db.list_database():
        # print(f"request: {request.database_name}")
        current_db = request.database_name
        db.using_database(current_db)
        return {f"result": "Switched to database : {request.database_name}"}
    raise HTTPException(status_cod400, detail=f"Invalid database name: {request.database_name}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6000)