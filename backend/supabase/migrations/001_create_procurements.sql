create table if not exists procurements (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  description text not null default '',
  status text not null default 'Draft',
  created_at timestamptz not null default now()
);

alter table procurements enable row level security;

create policy "Allow all access" on procurements
  for all
  using (true)
  with check (true);
