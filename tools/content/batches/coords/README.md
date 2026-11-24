# Coordinates for the batch scripts

Each `add_<name>.py` in the folder above takes a coordinates file as its second argument. The files here are those
inputs, kept so that a batch can be run again:

    python3 -I add_tr1.py <app_dir> coords/add_tr1.json <wikisource_root>

- `add_ru1.json` serves both `add_ru1.py` and `add_ru2.py` (one file for the two packs). It was rebuilt from the data
  on 2026-11-24 with `rebuild_from_data.py`, the original having been lost, and it still lists the two Yalta places,
  which the scripts no longer use (they are written by `add_ua1.py`, decision A-22).
- `add_ru4.json` and `add_ru5.json` are the originals for `add_ru4.py` and `add_ru5.py`.
- The files of the older batches (add_batch*, add_ca1, add_es*, add_gr*, add_ie*, add_it1–3, add_jp1–4 and others)
  were not kept. `rebuild_from_data.py` writes one from the place records, which carry the same values.

Checked on 2026-11-24: the Russian scripts (ru1–ru5) and add_fi1, add_tr1, add_ua1, add_ro1 run from these files
give the data in the repository, entry for entry (photos apart).
