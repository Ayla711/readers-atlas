# Western fragment — first batch only

10 books, 22 places, 20 lines (11 exact public-domain excerpts, 9 original scene summaries), one optional photo. All lines are draft. No website data modified and no second batch generated.

## Coverage

AK Wrangell; AZ Flagstaff; CA Weedpatch Camp / San Francisco; CO Denver / Leadville; HI Honolulu; ID Kuna; MT Billings; NV Virginia City; NM Gallup; OR Mount Hood; UT Salt Lake City; WA Seattle / Tacoma; WY Medicine Bow; ND Fargo; SD Ordway; KS Marysville; NE Lincoln / Omaha. Also Sallisaw, OK, coordinated with the central fragment author.

Coordinates come from fetched Wikipedia coordinate fields. Most HTML requests hit HTTP 429, so the browser research tool fetched those pages and their coordinate excerpts are retained in `cache/coordinate-web-evidence*.json`. Ordway's full successful HTML is `cache/Ordway.html`, showing 45°34′43″N 98°24′43″W. All coordinates rounded to four decimals; source values and states remain in evidence.json rather than places.json. The generic Honolulu coordinate appeared offshore. Honolulu now uses the separately fetched Honolulu Hale civic-center coordinate (21.304650,-157.857217), with a clear note that it represents the city and does not place Twain's fruit passage at the building. See cache/honolulu-land-coordinate.json.

## Selection rationale

The canon supplies tier-1 authors Mark Twain, Willa Cather, John Steinbeck and Jack Kerouac; Wallace Stegner is tier 2. The Grapes of Wrath, On the Road and Angle of Repose directly match its Modern Library book entries. Roughing It fills Kansas, Utah, Nevada and Hawaii through explicit text rather than assumed routes. My Ántonia and O Pioneers! supply real Nebraska city passages alongside the canon's Cather author coverage. Travels with Charley adds North Dakota and Montana with scene summaries only.

Three authors outside the supplied canon have explicit public grounds for inclusion:

- John Muir: [National Park Service historic site](https://www.nps.gov/jomu/index.htm) preserves his home and literary legacy; Travels in Alaska gives actual Alaska and Pacific Northwest passages.
- Owen Wister: [Medicine Bow Museum](https://travelwyoming.com/listing/medicine-bow-museum/735/) publicly presents his cabin; The Virginian opens explicitly at Medicine Bow and is suggested in the US brief.
- Hamlin Garland: [Academy of American Poets](https://poets.org/poet/hamlin-garland) records his 1922 Pulitzer Prize. Main-Travelled Roads is suggested by the US brief. The selected Ordway excerpt is clearly labeled as the author's autobiographical Foreword, not one of the fictional stories.

Canon residences were not silently equated with city markers. More detailed pilgrimage sites require separate content research and belong to later expansion; this fragment follows the first batch's needed geography and directly verified book passages. Weedpatch is explicitly a prototype, with its relationship to the fictional government camp explained. It has an optional CC BY 3.0 photo; all other selected points are original textual locations with no mandatory photo requirement.

## Reproducibility and validation

`python3 tools/us-work/west/build.py` regenerates the five fragment JSONs from the cached Gutenberg byte files and researched data in the script. Each quote uses explicit start/end markers; full download SHA-256, character offsets and exact source URL are in evidence.json. CRLFs are intentionally preserved, including line breaks in sentences; compare with read_bytes().decode('utf-8-sig'), not universal-newline read_text(). The only exact quotations are from authors deceased by 1955. All four protected books have scenes only, including Travels with Charley even though a Canadian Gutenberg version was consulted as factual evidence.

The script asserts 10 books/20 lines, reference highlight containment, and draft status. Separate inspection found no IDs colliding with either packs/existing-ids.json or tools/us-work/shared/current-ids.json. Root task performs the integrated 30-book/60-line schema and 51-region checks; running its full-pack counts on this fragment alone would intentionally fail.

## Editorial limits

City markers explicitly represent whole cities, never unverified houses, shops or railway tanks. Sallisaw marks the town and surrounding fictional farm setting, not a discovered Joad farm. Mount Hood's sourced summit represents the mountain, not Muir's observing position. Ordway is the settlement, not the Garland homestead. The Virginian source has chapter titles; selected Chapter 1 is “Enter the Man.” Roughing It's body headings are only numbered CHAPTER III, XIII, XLII, LXIII; expanded contents descriptions are not titles and were not invented as such.

Angle of Repose scenes use broad section labels because no stable chapter number was established from the consulted sources; Kuna is explicitly confirmed by its encyclopedia page with a reference to the 1971 edition, p.375. Leadville's role is supported by the novel's plot overview. Scenes stay conservative. The final literary review should assess translations and these broad location labels before approving drafts.

The Commons file page was successfully fetched to `cache/weedpatch-photo.html`; it explicitly contains CC BY 3.0 / Creative Commons Attribution 3.0 Unported. No image was downloaded. Every emitted quote’s correct ebook title and source match were checked.

The replacement Honolulu Hale point remains outside the coarse polygon despite being an identified land building; a documented boundary exception is still necessary. All other 21 points fall in their expected state polygons.

Independent central QA verified all 11 quote positions and 9 scene/place associations. Source section labels corrected to Foreword; Book 3, Lena Lingard, Chapter 1; and Part 2, Neighboring Fields, Chapter 7, with paired Chinese labels.
