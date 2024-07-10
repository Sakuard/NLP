import ollama
import chromadb

# documents = [
#   "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
#   "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
#   "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
#   "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
#   "Llamas are vegetarians and have very efficient digestive systems",
#   "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
# ]
documents = [
    "動物界,脊索動物門,哺乳綱,嚙齒目,鼠科,大鼠屬,溝鼠",
    "動物界,脊索動物門,哺乳綱,嚙齒目,倉鼠科,田鼠屬,田鼠",
    "動物界,脊索動物門,哺乳綱,嚙齒目,松鼠科,麗松鼠屬,赤腹鼠",
    "動物界,脊索動物門,哺乳綱,雙門齒目,袋鼠科,袋鼠屬,紅大袋鼠",
    "動物界,脊索動物門,哺乳綱,偶蹄目,牛科,牛屬,黃牛",
    "動物界,脊索動物門,哺乳綱,偶蹄目,牛科,水牛屬,水牛",
    "動物界,脊索動物門,哺乳綱,肉食目,貓科,豹屬,孟加拉虎",
    "動物界,脊索動物門,哺乳綱,肉食目,貓科,豹屬,獅子",
    "動物界,脊索動物門,哺乳綱,肉食目,貓科,豹屬,花豹",
    "動物界,脊索動物門,哺乳綱,肉食目,貓科,石虎屬,石虎",
    "動物界,脊索動物門,哺乳綱,肉食目,貓科,獵豹屬,獵豹",
    "動物界,脊索動物門,哺乳綱,兔形目,兔科,穴兔屬,家兔",
    "動物界,脊索動物門,爬蟲綱,有鱗目,眼鏡蛇科,環蛇屬,雨傘節",
    "動物界,脊索動物門,爬蟲綱,有鱗目,蝰科,青竹絲屬,青竹絲",
    "動物界,脊索動物門,哺乳綱,奇蹄目,馬科,馬屬,馬",
    "動物界,脊索動物門,哺乳綱,奇蹄目,馬科,馬屬,斑馬",
    "動物界,脊索動物門,哺乳綱,偶蹄目,牛科,山羊屬,山羊",
    "動物界,脊索動物門,哺乳綱,偶蹄目,牛科,盤羊屬,綿羊",
    "動物界,脊索動物門,哺乳綱,偶蹄目,牛科,鬣羚屬,台灣長鬃山羊",
    "動物界,脊索動物門,哺乳綱,靈長目,猴科,獼猴屬,台灣獼猴",
]

client = chromadb.Client()
collection = client.create_collection(name="docs")

# store each document in a vector embedding database
for i, d in enumerate(documents):
  response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
  embedding = response["embedding"]
  collection.add(
    ids=[str(i)],
    embeddings=[embedding],
    documents=[d]
  )

# an example prompt
prompt = "Which animal is most related to '動物界,脊索動物門,哺乳綱,靈長目,人科,黑猩猩屬,黑猩猩' "

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

ollama.pull(model="llama2")
# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="llama2",
  prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

print(output['response'])