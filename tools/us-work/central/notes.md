# Central and Southern US — first-batch shard

10 books, 23 places, exactly 20 draft lines: 10 public-domain extracts and 10 original scene descriptions. No pilgrimage or film-location entries; photos.json is intentionally empty. All mapped cities represent the named settlement as a whole. Fox River uses the coordinate explicitly embedded in the fetched Wikipedia mapframe and is an inspiration/prototype, not an asserted exact fictional fishing spot.

## Reproduction

Run `sh fetch.sh` to refresh the recorded public sources, then `python3 build.py`. The build reads Gutenberg bytes as UTF-8 without newline normalization, finds specified start/end strings, and copies the complete substring including CRLF. `extractions.json` records boundaries and character offsets; `evidence.json` records original file hashes and sources. A refreshed edition can shift offsets or fail an anchor; do not silently adjust quotes. The sources were fetched over the network with curl -fL. An unrelated exploratory Gutenberg download (64310) was not used in any content.

## Selection and copyright

Selection follows tools/canon-us.json. Twain, Stowe, Dreiser, Wilder, Lee, Faulkner, Hurston and Hemingway are tier 1 authors. Walker and McMurtry are tier 2, with The Color Purple and Lonesome Dove explicitly listed by Great American Read. Sister Carrie and The Sound and the Fury are Modern Library selections; Mockingbird and Their Eyes are Great American Read selections. Life on the Mississippi, Uncle Tom’s Cabin, Little House in the Big Woods and The Nick Adams Stories are author-based selections for reliable regional coverage. The Michigan Hemingway Society supplies the Nick Adams geographical rationale. Each book has one to seven lines.

Copyright follows the specified UK death-year cutoff, not US publication dates. Death dates were read from fetched biography infoboxes; see evidence.json. No Hemingway, Wilder, Faulkner, Hurston, Lee, Walker or McMurtry wording is quoted.

- Mark Twain: Died  April 21, 1910 (1910-04-21) — https://en.wikipedia.org/wiki/Mark_Twain
- Harriet Beecher Stowe: Died  July 1, 1896 (1896-07-01) — https://en.wikipedia.org/wiki/Harriet_Beecher_Stowe
- Theodore Dreiser: Died  December 28, 1945 (1945-12-28) — https://en.wikipedia.org/wiki/Theodore_Dreiser
- Laura Ingalls Wilder: Died  February 10, 1957 (1957-02-10) — https://en.wikipedia.org/wiki/Laura_Ingalls_Wilder
- Harper Lee: Died  February 19, 2016 (2016-02-19) — https://en.wikipedia.org/wiki/Harper_Lee
- Alice Walker: Fetched biography has no death field; treated as living and copyrighted. — https://en.wikipedia.org/wiki/Alice_Walker
- William Faulkner: Died  July 6, 1962 (1962-07-06) — https://en.wikipedia.org/wiki/William_Faulkner
- Zora Neale Hurston: Died  January 28, 1960 (1960-01-28) — https://en.wikipedia.org/wiki/Zora_Neale_Hurston
- Ernest Hemingway: Died  July 2, 1961 (1961-07-02) — https://en.wikipedia.org/wiki/Ernest_Hemingway
- Larry McMurtry: Died  March 25, 2021 (2021-03-25) — https://en.wikipedia.org/wiki/Larry_McMurtry

## State coverage

{'AL': 1, 'AR': 2, 'FL': 2, 'GA': 1, 'IA': 3, 'IL': 2, 'IN': 1, 'KY': 1, 'LA': 1, 'MI': 2, 'MN': 2, 'MO': 1, 'MS': 1, 'TN': 1, 'TX': 1, 'WI': 1}

Oklahoma is delegated to the west shard's Sallisaw / The Grapes of Wrath entry and is not falsely assigned to a Lonesome Dove river scene. The Canadian River sequence in that novel was not used to claim an Oklahoma coordinate.

## Scope and editorial limits

Indianapolis is a place explicitly mentioned by Ames in dialogue, not the location of that dialogue; the place note says so. Eatonton is marked as a prototype, supported by AFI’s production history linking the novel to Walker’s childhood landscape. Oxford and Monroeville are prototypes for Jefferson and Maycomb. San Antonio is a regional marker for the nearby fictional burial site and does not claim an identifiable orchard. The population inventory in Life on the Mississippi is historical narration, not present-day demographic information. Draft status is retained throughout.

Reserved proposals Huckleberry Finn, Tom Sawyer, The Awakening and Gone with the Wind were replaced in this shard to cover more states within ten books. No second batch has been started.
