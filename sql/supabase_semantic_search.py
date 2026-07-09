from supabase import create_client
from openai import OpenAI
import os

supabase = create_client(...)
openai = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

async def semantic_search(query, top_k=5):
    # Embed the query
    query_embedding = openai.embeddings.create(
        model='text-embedding-3-small',
        input=query
    )

    query_vector = query_embedding.data[0].embedding

    # Search for similar vectors
    results = supabase.storage.vectors() \
        .from_('embeddings') \
        .index('documents-openai') \
        .query(
            query_vector={'float32': query_vector},
            topK=top_k,
            return_distance=True,
            return_metadata=True
        )

    return [
        {
            'id': result.key,
            'title': result.metadata.get('title') if result.metadata else None,
            'similarity': 1 - result.distance if result.distance else 0,  # Convert distance to similarity (0-1)
            'metadata': result.metadata
        }
        for result in results.vectors
    ]

# Usage
results = semantic_search('How do I use vector search?')
for result in results:
    print(f'{result["title"]} ({result["similarity"] * 100:.1f}% similar)')