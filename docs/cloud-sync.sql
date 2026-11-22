-- The Reader's Atlas: one row per reader, holding their records as one JSON document
-- (wishlist, visited places, trips, shelf, favourites, notes, diary text, chosen portrait).
-- Run once in the Supabase SQL Editor. Safe to run again.
-- Written by js/cloud.js with the publishable key; row-level security lets a signed-in reader
-- read and write their own row and nobody else's.

create table if not exists public.user_data (
  user_id    uuid primary key default auth.uid() references auth.users (id) on delete cascade,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.user_data enable row level security;

-- signed-in readers only; nothing for visitors who are not signed in
revoke all on public.user_data from anon;
grant select, insert, update on public.user_data to authenticated;

drop policy if exists "readers read their own row" on public.user_data;
create policy "readers read their own row" on public.user_data
  for select to authenticated using ((select auth.uid()) = user_id);

drop policy if exists "readers create their own row" on public.user_data;
create policy "readers create their own row" on public.user_data
  for insert to authenticated with check ((select auth.uid()) = user_id);

drop policy if exists "readers change their own row" on public.user_data;
create policy "readers change their own row" on public.user_data
  for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
