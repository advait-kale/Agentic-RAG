
-- 1. pgvector extension
create extension if not exists vector;

-- 2. Chunk table (contract: chunk_id, source, text, embedding)
create table if not exists rag_chunks (
    id          bigint generated always as identity primary key,
    chunk_id    text unique not null,        -- "{base}#{n}", upsert key
    source      text not null,
    text        text not null,
    embedding   vector(1024) not null,       -- MUST match embed dim
    created_at  timestamptz default now()
);

-- 3. Cosine similarity index (IVFFlat). Build after seeding for best recall.
create index if not exists rag_chunks_embedding_idx
    on rag_chunks
    using ivfflat (embedding vector_cosine_ops)
    with (lists = 100);

-- 4. Top-k cosine search RPC
--    Returns search_result contract: {chunk_id, source, text, similarity}
create or replace function match_chunks(
    query_embedding vector(1024),
    match_count int default 4,
    min_similarity float default 0.0
)
returns table (
    chunk_id   text,
    source     text,
    text       text,
    similarity float
)
language sql
stable
as $$
    select
        c.chunk_id,
        c.source,
        c.text,
        1 - (c.embedding <=> query_embedding) as similarity
    from rag_chunks c
    where 1 - (c.embedding <=> query_embedding) >= min_similarity
    order by c.embedding <=> query_embedding
    limit match_count;
$$;
