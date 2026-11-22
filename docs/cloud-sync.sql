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

-- ---------------------------------------------------------------------------------------------------------------
-- Where a reader stands among readers (11-22). Run this part in the SQL Editor too; safe to run again.
-- reader_rank() takes nothing from the page: it reads the caller's own saved row, counts the places they have
-- visited and the books they have read, and compares each count with every other reader's. It returns numbers
-- only (no ids, emails, places or books of anyone else):
--   places / books      the caller's own count, as saved with their account
--   *_readers           readers with at least one (accounts with none are not counted)
--   *_rank              1 + readers with more than the caller (equal counts share a rank)
--   *_behind            readers with at least one but fewer than the caller
-- It runs with the owner's rights, because row-level security lets a reader see only their own row; the search
-- path is fixed and only signed-in readers may call it.
create or replace function public.reader_rank()
returns json
language sql
stable
security definer
set search_path = ''
as $$
  with counts as (
    select d.user_id,
      (select count(distinct e->>'place_id')
         from jsonb_array_elements(case when jsonb_typeof(d.data->'user_places') = 'array' then d.data->'user_places' else '[]'::jsonb end) e
        where e->>'kind' = 'visited') as p,
      (select count(distinct e->>'book_id')
         from jsonb_array_elements(case when jsonb_typeof(d.data->'user_books') = 'array' then d.data->'user_books' else '[]'::jsonb end) e
        where e->>'shelf' = 'read') as b
    from public.user_data d
  ),
  me as (
    select coalesce(max(p), 0) as p, coalesce(max(b), 0) as b from counts where user_id = (select auth.uid())
  )
  select json_build_object(
    'places', me.p,
    'places_readers', (select count(*) from counts where p > 0),
    'places_rank', (select count(*) from counts where p > me.p) + 1,
    'places_behind', (select count(*) from counts where p > 0 and p < me.p),
    'books', me.b,
    'books_readers', (select count(*) from counts where b > 0),
    'books_rank', (select count(*) from counts where b > me.b) + 1,
    'books_behind', (select count(*) from counts where b > 0 and b < me.b)
  ) from me;
$$;

revoke all on function public.reader_rank() from public, anon;
grant execute on function public.reader_rank() to authenticated;
