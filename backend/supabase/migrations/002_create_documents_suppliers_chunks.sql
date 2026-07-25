create extension if not exists vector;

create table if not exists documents (
  id uuid default gen_random_uuid() primary key,
  procurement_id uuid not null references procurements(id) on delete cascade,
  filename text not null,
  document_type text not null default 'Unknown',
  storage_path text,
  document_status text not null default 'processing',
  ai_summary text,
  uploaded_at timestamptz not null default now()
);

create table if not exists suppliers (
  id uuid default gen_random_uuid() primary key,
  procurement_id uuid not null references procurements(id) on delete cascade,
  document_id uuid not null references documents(id) on delete cascade,
  supplier_name text,
  price numeric,
  currency text,
  warranty text,
  delivery_days integer,
  payment_terms text,
  compliance_score numeric,
  raw_extraction jsonb,
  created_at timestamptz not null default now()
);

create table if not exists document_chunks (
  id uuid default gen_random_uuid() primary key,
  document_id uuid not null references documents(id) on delete cascade,
  chunk_index integer not null,
  chunk_text text not null,
  embedding vector(384),
  metadata jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_documents_procurement on documents(procurement_id);
create index if not exists idx_suppliers_procurement on suppliers(procurement_id);
create index if not exists idx_suppliers_document on suppliers(document_id);
create index if not exists idx_chunks_document on document_chunks(document_id);

alter table documents enable row level security;
alter table suppliers enable row level security;
alter table document_chunks enable row level security;

create policy "Allow all access" on documents for all using (true) with check (true);
create policy "Allow all access" on suppliers for all using (true) with check (true);
create policy "Allow all access" on document_chunks for all using (true) with check (true);
