#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p cache
curl -fL https://en.wikipedia.org/wiki/Hannibal,_Missouri -o cache/hannibal.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Memphis,_Tennessee -o cache/memphis.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Helena,_Arkansas -o cache/helena.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Dubuque,_Iowa -o cache/dubuque.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Burlington,_Iowa -o cache/burlington.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Davenport,_Iowa -o cache/davenport.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Minneapolis -o cache/minneapolis.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Saint_Paul,_Minnesota -o cache/saint-paul.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/New_Orleans -o cache/new-orleans.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Cairo,_Illinois -o cache/cairo.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Louisville,_Kentucky -o cache/louisville.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Chicago -o cache/chicago.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Indianapolis -o cache/indianapolis.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Pepin,_Wisconsin -o cache/pepin.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Monroeville,_Alabama -o cache/monroeville.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Eatonton,_Georgia -o cache/eatonton.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Oxford,_Mississippi -o cache/oxford.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Eatonville,_Florida -o cache/eatonville.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Jacksonville,_Florida -o cache/jacksonville.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Seney,_Michigan -o cache/seney.html
sleep 1
curl -fL 'https://en.wikipedia.org/wiki/Fox_River_(Michigan)' -o cache/fox-river.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Fort_Smith,_Arkansas -o cache/fort-smith.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/San_Antonio -o cache/san-antonio.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Mark_Twain -o cache/author-Mark_Twain.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Harriet_Beecher_Stowe -o cache/author-Harriet_Beecher_Stowe.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Theodore_Dreiser -o cache/author-Theodore_Dreiser.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Laura_Ingalls_Wilder -o cache/author-Laura_Ingalls_Wilder.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Harper_Lee -o cache/author-Harper_Lee.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Alice_Walker -o cache/author-Alice_Walker.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/William_Faulkner -o cache/author-William_Faulkner.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Zora_Neale_Hurston -o cache/author-Zora_Neale_Hurston.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Ernest_Hemingway -o cache/author-Ernest_Hemingway.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Larry_McMurtry -o cache/author-Larry_McMurtry.html
sleep 1
curl -fL https://www.gutenberg.org/cache/epub/245/pg245.txt -o cache/pg245.txt
sleep 1
curl -fL https://www.gutenberg.org/cache/epub/203/pg203.txt -o cache/pg203.txt
sleep 1
curl -fL https://www.gutenberg.org/cache/epub/233/pg233.txt -o cache/pg233.txt
sleep 1
curl -fL https://en.wikipedia.org/wiki/Little_House_in_the_Big_Woods -o cache/little-house.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/To_Kill_a_Mockingbird -o cache/mockingbird.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/The_Color_Purple -o cache/color-purple.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/The_Sound_and_the_Fury -o cache/sound-fury.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Their_Eyes_Were_Watching_God -o cache/their-eyes.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Lonesome_Dove -o cache/lonesome-dove.html
sleep 1
curl -fL https://www.michiganhemingwaysociety.org/publications/hemingway-in-seney/ -o cache/nick-adams.html
sleep 1
curl -fL https://en.wikipedia.org/wiki/Big_Two-Hearted_River -o cache/nick-scene.html
sleep 1
curl -fL https://www.storychasers.com/big-woods -o cache/pepin-scene.html
sleep 1
curl -fL https://alabama.travel/plan-your-trip/road-trips/monroeville-the-to-kill-a-mockingbird-experience/ -o cache/maycomb-prototype.html
sleep 1
curl -fL 'https://catalog.afi.com/Film/67174-THE-COLOR-PURPLE?cxt=ymal' -o cache/eatonton-prototype.html
sleep 1
