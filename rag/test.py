import ollama
import chromadb
import os

path2dataset = './dataset/'

# Function to read all txt files in the ./dataset/ directory
def read_documents_from_directory(directory):
    documents = []
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                documents.append(file.read())
                filenames.append(filename)
    return documents, filenames

# Read documents and filenames from the dataset directory
# documents, filenames = read_documents_from_directory('./dataset/')
documents, filenames = read_documents_from_directory(path2dataset)

client = chromadb.Client()

# 檢查 collection 是否存在，如果存在則刪除
try:
    existing_collections = client.list_collections()
    if "docs" in [col['name'] for col in existing_collections]:
        client.delete_collection(name="docs")
except Exception as e:
    print(f"Failed to delete collection: {e}")

# 創建新的 collection
collection = client.create_collection(name="docs")

# store each document in a vector embedding database
for i, (d, filename) in enumerate(zip(documents, filenames)):
    response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
    embedding = response["embedding"]
    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[d],
        metadatas=[{"filename": filename}]
    )

# an example prompt
prompt = "What animals are llamas related to?"

# generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
  prompt=prompt,
  model="mxbai-embed-large"
)
results = collection.query(
  query_embeddings=[response["embedding"]],
  n_results=1
)
data = results['documents'][0][0]
filename = results['metadatas'][0][0]['filename']

# 確保模型已經被下載
ollama.pull(model="llama2")

# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="llama2",
  prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

print(f"The most relevant document is from the file: {filename}")
print(output['response'])
