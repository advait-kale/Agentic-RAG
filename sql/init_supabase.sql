
-- 1. pgvector extension
create extension if not exists vector;

-- 2. chunk table
-- embedding dim = qwen3-embedding:0.6b output (1024). Must match services/embeddings.py.
create table if not exists rag_chunks (
  id         bigserial primary key,
  chunk_id   text unique not null,
  source     text,
  text       text,
  embedding  vector(1024)
);

-- 2b. row level security
-- public-schema tables are reachable via PostgREST with the anon key; lock it down.
-- app uses the service_role key (bypasses RLS), so enabling RLS with no policy
-- = service-role-only access. Add explicit policies if the anon client needs read.
alter table rag_chunks enable row level security;

-- 3. match_chunks RPC (cosine similarity, threshold + count)
-- similarity = 1 - cosine_distance; higher = closer.
-- search_path pinned so the function can't be hijacked via a mutable path.
create or replace function match_chunks (
  query_embedding vector(1024),
  match_count     int   default 5,
  min_similarity  float default 0.0
)
returns table (chunk_id text, source text, text text, similarity float)
language sql stable
set search_path = public, pg_catalog
as $$
  select c.chunk_id, c.source, c.text,
         1 - (c.embedding <=> query_embedding) as similarity
  from rag_chunks c
  where 1 - (c.embedding <=> query_embedding) >= min_similarity
  order by c.embedding <=> query_embedding
  limit match_count;
$$;

-- 4. HNSW cosine index
-- HNSW (not IVFFlat): no centroid training, so it's safe to create on an empty
-- table and needs no lists/probes tuning. Better recall/latency for a small,
-- write-light RAG store.
create index if not exists rag_chunks_embedding_idx
  on rag_chunks using hnsw (embedding vector_cosine_ops);
