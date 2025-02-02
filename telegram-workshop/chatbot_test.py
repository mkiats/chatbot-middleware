import asyncio
from chatbot import main

async def get_response():
    user_query = input("Input your query: ")
    query_response = await main(str(user_query))
    return query_response

# Option 2: If running in a synchronous context
response = asyncio.run(get_response())
print(response)