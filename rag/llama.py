import asyncio
from ollama import AsyncClient

async def chat():
  message = {'role': 'user', 'content': 'Why is the sky blue?'}
  async for part in await AsyncClient().chat(model='llama3', messages=[message], stream=True):
    print(part['message']['content'], end='', flush=True)

asyncio.run(chat())

def main():
  asyncio.run(chat())

if __name__ == "__main__":
  main()