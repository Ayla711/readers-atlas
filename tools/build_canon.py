"""Builds tools/canon.json: the outside checklist the coverage check compares the database against.
Every entry names the list it came from, so the checklist does not depend on what is already in the database.
Usage: python3 tools/build_canon.py   (writes tools/canon.json next to this file)"""
import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canon.json")
SOURCES = {
    "PC": ["Poets' Corner, Westminster Abbey (Wikipedia)", "https://en.wikipedia.org/wiki/Poets%27_Corner"],
    "WH": ["Writer's home (Wikipedia)", "https://en.wikipedia.org/wiki/Writer%27s_home"],
    "ST": ["Historic writers' houses you can visit in England (Slow Travel UK)", "https://www.slow-travel.uk/post/historic-writers-houses-you-can-visit-in-england"],
    "SC": ["Language & literature museums in Scotland (Which Museum)", "https://whichmuseum.co.uk/place/scotland-6/t-language-literature"],
    "WA": ["Welsh writing spots (Visit Wales)", "https://www.visitwales.com/explore/literature/welsh-writing-spots"],
    "NI": ["A book lover's guide to Northern Ireland (Discover Northern Ireland)", "https://discovernorthernireland.com/blog/post/a-book-lovers-guide-to-northern-ireland/"],
    "BR": ["BBC Big Read top 100, 2003", "https://www.nicholaswhyte.info/100books/bbcbigread.htm"],
    "LG": ["Legends and medieval anonymous works set in Britain (the Matter of Britain and after): compiled 2026-11-09 after the user found the Arthurian legend missing; the published lists above are author- and bestseller-based and never reach anonymous or legendary material", "https://en.wikipedia.org/wiki/Matter_of_Britain"],
    "FV": ["Foreign-language works about Britain: shortlist compiled 2026-11-09 from the chat (famous works, any genre, that name real British places), ranked by the user; the five tier-1 titles were the user's pick", "docs/week1-uk-spec.md 6.4.1"],
}
CHECKED = "2026-11-09"

# Writers buried in or commemorated at Poets' Corner, as listed by the source (non-writers left out)
PC_BURIED = ["Geoffrey Chaucer", "Edmund Spenser", "John Dryden", "Robert Browning", "Alfred, Lord Tennyson", "Charles Dickens",
             "Thomas Hardy", "Samuel Johnson", "Rudyard Kipling", "Richard Brinsley Sheridan", "John Gay", "John Masefield",
             "Francis Beaumont", "Abraham Cowley", "Matthew Prior", "Thomas Macaulay"]
PC_MEMORIAL = ["Joseph Addison", "Matthew Arnold", "Jane Austen", "W. H. Auden", "John Betjeman", "William Blake", "Charlotte Brontë",
               "Anne Brontë", "Emily Brontë", "Elizabeth Barrett Browning", "Fanny Burney", "Robert Burns", "Samuel Butler", "Lord Byron",
               "Lewis Carroll", "John Clare", "Samuel Taylor Coleridge", "George Eliot", "T. S. Eliot", "Elizabeth Gaskell",
               "Oliver Goldsmith", "Thomas Gray", "Robert Herrick", "Gerard Manley Hopkins", "A. E. Housman", "Ted Hughes", "Henry James",
               "Ben Jonson", "John Keats", "Charles Kingsley", "Philip Larkin", "D. H. Lawrence", "Edward Lear", "C. S. Lewis",
               "Christopher Marlowe", "John Milton", "Alexander Pope", "John Ruskin", "Walter Scott", "William Shakespeare",
               "Percy Bysshe Shelley", "Robert Southey", "William Makepeace Thackeray", "James Thomson", "Dylan Thomas",
               "Anthony Trollope", "Oscar Wilde", "William Wordsworth", "Rupert Brooke", "Robert Graves", "Ivor Gurney",
               "Wilfred Owen", "Isaac Rosenberg", "Siegfried Sassoon", "Edward Thomas", "Laurence Binyon", "Edmund Blunden"]

def S(name, authors, src, ids=(), names=(), tier=1, zh=None):
    return dict(name=name, name_zh=zh, authors=authors, src=src, ids=list(ids), names=list(names), tier=tier)
sites = [
    S("Poets' Corner, Westminster Abbey", PC_BURIED + PC_MEMORIAL, ["PC"], ids=["poets-corner"], zh="西敏寺诗人角"),
    # England (WH, ST)
    S("Brontë Parsonage Museum, Haworth", ["Charlotte Brontë", "Emily Brontë", "Anne Brontë"], ["WH", "ST"], ids=["bronte-parsonage"]),
    S("Jane Austen's House, Chawton", ["Jane Austen"], ["WH", "ST"], ids=["chawton"]),
    S("Newstead Abbey", ["Lord Byron"], ["WH", "ST"], ids=["newstead-abbey"]),
    S("Carlyle's House, Chelsea", ["Thomas Carlyle"], ["WH", "ST"], names=["Carlyle"]),
    S("Greenway", ["Agatha Christie"], ["WH", "ST"], ids=["greenway"]),
    S("John Clare Cottage, Helpston", ["John Clare"], ["WH", "ST"], names=["Clare Cottage", "Helpston"]),
    S("Coleridge Cottage, Nether Stowey", ["Samuel Taylor Coleridge"], ["WH", "ST"], names=["Coleridge", "Nether Stowey"]),
    S("Cowper and Newton Museum, Olney", ["William Cowper"], ["WH"], names=["Cowper", "Olney"]),
    S("Charles Dickens Museum, Doughty Street", ["Charles Dickens"], ["WH", "ST"], ids=["dickens-museum"]),
    S("Charles Dickens Birthplace Museum, Portsmouth", ["Charles Dickens"], ["ST"], names=["Dickens Birthplace", "Portsmouth"]),
    S("Elizabeth Gaskell's House, Manchester", ["Elizabeth Gaskell"], ["WH", "ST"], ids=["gaskell-house"]),
    S("Hardy's Cottage, Higher Bockhampton", ["Thomas Hardy"], ["WH", "ST"], ids=["hardys-cottage"]),
    S("Max Gate, Dorchester", ["Thomas Hardy"], ["WH", "ST"], names=["Max Gate"]),
    S("World of James Herriot, Thirsk", ["James Herriot"], ["WH", "ST"], names=["Herriot", "Thirsk"]),
    S("Dr Johnson's House, Gough Square", ["Samuel Johnson"], ["WH", "ST"], ids=["dr-johnsons-house"]),
    S("Samuel Johnson Birthplace Museum, Lichfield", ["Samuel Johnson"], ["WH"], names=["Lichfield"]),
    S("Keats House, Hampstead", ["John Keats"], ["WH", "ST"], ids=["keats-house"]),
    S("Bateman's, Burwash", ["Rudyard Kipling"], ["WH", "ST"], names=["Bateman"]),
    S("Clouds Hill", ["T. E. Lawrence"], ["WH", "ST"], names=["Clouds Hill"], tier=2),
    S("Milton's Cottage, Chalfont St Giles", ["John Milton"], ["WH", "ST"], names=["Milton's Cottage", "Chalfont"]),
    S("Shakespeare's Birthplace, Stratford-upon-Avon", ["William Shakespeare"], ["WH", "ST"], ids=["shakespeare-birthplace"]),
    S("Shandy Hall, Coxwold", ["Laurence Sterne"], ["WH"], names=["Shandy Hall", "Coxwold"]),
    S("Farringford, Isle of Wight", ["Alfred, Lord Tennyson"], ["WH"], names=["Farringford"]),
    S("Strawberry Hill House, Twickenham", ["Horace Walpole"], ["WH", "ST"], names=["Strawberry Hill"], tier=2),
    S("Monk's House, Rodmell", ["Virginia Woolf"], ["WH", "ST"], ids=["monks-house"]),
    S("Dove Cottage, Grasmere", ["William Wordsworth"], ["WH", "ST"], ids=["dove-cottage"]),
    S("Rydal Mount", ["William Wordsworth"], ["WH", "ST"], names=["Rydal"]),
    S("Hill Top, Near Sawrey", ["Beatrix Potter"], ["WH", "ST"], ids=["hill-top-sawrey"]),
    S("D. H. Lawrence Birthplace Museum, Eastwood", ["D. H. Lawrence"], ["ST"], ids=["lawrence-birthplace"]),
    S("Shaw's Corner, Ayot St Lawrence", ["George Bernard Shaw"], ["ST"], names=["Shaw's Corner"], tier=2),
    S("Gilbert White's House, Selborne", ["Gilbert White"], ["ST"], names=["Selborne"], tier=2),
    S("Knole", ["Vita Sackville-West", "Virginia Woolf"], ["ST"], names=["Knole"], tier=2),
    S("Izaak Walton's Cottage, Shallowford", ["Izaak Walton"], ["ST"], names=["Walton"], tier=2),
    S("Shibden Hall, Halifax", ["Anne Lister"], ["ST"], names=["Shibden"], tier=2),
    S("Richard Jefferies Museum, Swindon", ["Richard Jefferies"], ["ST"], names=["Jefferies"], tier=2),
    S("Lamb House, Rye", ["Henry James"], ["ST"], names=["Lamb House"], tier=2),
    S("Penshurst Place", ["Philip Sidney"], ["ST"], names=["Penshurst"], tier=2),
    S("Kelmscott Manor", ["William Morris"], ["ST"], names=["Kelmscott"], tier=2),
    # Scotland (WH, SC)
    S("Burns Cottage, Alloway", ["Robert Burns"], ["WH", "SC"], ids=["burns-cottage"]),
    S("Burns House, Dumfries", ["Robert Burns"], ["SC"], names=["Dumfries"]),
    S("Abbotsford, Melrose", ["Walter Scott"], ["WH", "SC"], ids=["abbotsford"]),
    S("Writers' Museum, Edinburgh", ["Robert Burns", "Walter Scott", "Robert Louis Stevenson"], ["SC"], ids=["writers-museum"]),
    S("J. M. Barrie's Birthplace, Kirriemuir", ["J. M. Barrie"], ["SC"], names=["Kirriemuir", "Barrie's Birthplace"]),
    S("Dunbeath Heritage Centre", ["Neil M. Gunn"], ["SC"], names=["Dunbeath"], tier=2),
    # Wales (WH, WA)
    S("Dylan Thomas Boathouse, Laugharne", ["Dylan Thomas"], ["WH", "WA"], ids=["dylan-thomas-boathouse"]),
    S("Dylan Thomas Birthplace, 5 Cwmdonkin Drive, Swansea", ["Dylan Thomas"], ["WA"], names=["Cwmdonkin", "Swansea"]),
    S("Yr Ysgwrn, Trawsfynydd", ["Hedd Wyn"], ["WH"], names=["Ysgwrn", "Trawsfynydd"]),
    S("Plas yn Rhiw", ["R. S. Thomas"], ["WA"], names=["Plas yn Rhiw"], tier=2),
    S("Roald Dahl Plass and the Norwegian Church, Cardiff Bay", ["Roald Dahl"], ["WA"], names=["Norwegian Church"]),
    S("Alice Town Trail, Llandudno", ["Lewis Carroll"], ["WA"], names=["Llandudno"], tier=2),
    S("Plas Tan yr Allt, Porthmadog", ["Percy Bysshe Shelley"], ["WA"], names=["Tan yr Allt", "Tan-yr-Allt"], tier=2),
    # Northern Ireland (NI)
    S("Seamus Heaney HomePlace, Bellaghy", ["Seamus Heaney"], ["NI"], names=["Heaney", "Bellaghy"]),
    S("C. S. Lewis Square, Belfast", ["C. S. Lewis"], ["NI"], names=["C. S. Lewis Square", "C.S. Lewis Square", "Dundela"]),
    S("Kilbroney Park, Rostrevor", ["C. S. Lewis"], ["NI"], ids=["rostrevor"]),
]

# BBC Big Read titles by British or Irish-born authors whose story is set in, or modelled on, a real place in the UK.
# Rank 1-50 is tier 1, the rest tier 2. Books set wholly abroad or in an invented world without a UK model are left out.
# Tier 2 regardless of rank where the setting is mostly invented and no real UK place stands behind it.
INVENTED = {"The Hitchhiker's Guide to the Galaxy", "The Pillars of the Earth", "Goodnight Mister Tom", "Charlie and the Chocolate Factory",
            "The Shell Seekers"}
def R(rank, title, author, also=()):
    return dict(rank=rank, title=title, author=author, also=list(also), tier=1 if rank <= 50 and title not in INVENTED else 2, src=["BR"])
big_read = [
    R(1, "The Lord of the Rings", "J. R. R. Tolkien"), R(2, "Pride and Prejudice", "Jane Austen"),
    R(3, "His Dark Materials", "Philip Pullman", ["Northern Lights", "The Amber Spyglass", "The Subtle Knife"]),
    R(4, "The Hitchhiker's Guide to the Galaxy", "Douglas Adams"), R(5, "Harry Potter and the Goblet of Fire", "J. K. Rowling"),
    R(7, "Winnie-the-Pooh", "A. A. Milne"), R(8, "Nineteen Eighty-Four", "George Orwell", ["1984"]),
    R(9, "The Lion, the Witch and the Wardrobe", "C. S. Lewis"), R(10, "Jane Eyre", "Charlotte Brontë"),
    R(12, "Wuthering Heights", "Emily Brontë"), R(14, "Rebecca", "Daphne du Maurier"), R(16, "The Wind in the Willows", "Kenneth Grahame"),
    R(17, "Great Expectations", "Charles Dickens"), R(22, "Harry Potter and the Philosopher's Stone", "J. K. Rowling"),
    R(23, "Harry Potter and the Chamber of Secrets", "J. K. Rowling"), R(24, "Harry Potter and the Prisoner of Azkaban", "J. K. Rowling"),
    R(25, "The Hobbit", "J. R. R. Tolkien"), R(26, "Tess of the d'Urbervilles", "Thomas Hardy"), R(28, "Middlemarch", "George Eliot"),
    R(30, "Alice's Adventures in Wonderland", "Lewis Carroll"),
    R(33, "The Pillars of the Earth", "Ken Follett"), R(34, "David Copperfield", "Charles Dickens"),
    R(35, "Charlie and the Chocolate Factory", "Roald Dahl"), R(36, "Treasure Island", "Robert Louis Stevenson"),
    R(38, "Persuasion", "Jane Austen"), R(40, "Emma", "Jane Austen"), R(42, "Watership Down", "Richard Adams"),
    R(45, "Brideshead Revisited", "Evelyn Waugh"), R(46, "Animal Farm", "George Orwell"), R(47, "A Christmas Carol", "Charles Dickens"),
    R(48, "Far from the Madding Crowd", "Thomas Hardy"), R(49, "Goodnight Mister Tom", "Michelle Magorian"),
    R(50, "The Shell Seekers", "Rosamunde Pilcher"), R(51, "The Secret Garden", "Frances Hodgson Burnett"), R(56, "The BFG", "Roald Dahl"),
    R(57, "Swallows and Amazons", "Arthur Ransome"), R(58, "Black Beauty", "Anna Sewell"), R(63, "A Tale of Two Cities", "Charles Dickens"),
    R(66, "The Magic Faraway Tree", "Enid Blyton"), R(68, "Good Omens", "Terry Pratchett"),
    R(72, "The Ragged Trousered Philanthropists", "Robert Tressell"), R(74, "Matilda", "Roald Dahl"),
    R(75, "Bridget Jones's Diary", "Helen Fielding"), R(77, "The Woman in White", "Wilkie Collins"), R(79, "Bleak House", "Charles Dickens"),
    R(82, "I Capture the Castle", "Dodie Smith"), R(86, "Brave New World", "Aldous Huxley"), R(88, "Cold Comfort Farm", "Stella Gibbons"),
    R(95, "Katherine", "Anya Seton"),
]

# Foreign-language works about Britain (FV). Not a published list: the coverage check had no source for this category at all
# (6.4.1 blind spot found 11-09), so the shortlist from the chat is recorded here with the user's ranking. Tier 1 = the five
# the user chose; tier 2 = the rest, to be decided later.
def F(title, author, tier, also=()):
    return dict(rank=0, title=title, author=author, also=list(also), tier=tier, src=["FV"])
big_read += [
    F("The Three Musketeers", "Alexandre Dumas", 1, ["Les Trois Mousquetaires"]), F("Around the World in Eighty Days", "Jules Verne", 1),
    F("Commentaries on the Gallic War", "Julius Caesar", 1, ["De Bello Gallico", "The Gallic War"]), F("The Man Who Laughs", "Victor Hugo", 1, ["L'Homme qui rit"]),
    F("Black Butler", "Yana Toboso", 1, ["Kuroshitsuji"]),
    F("Twenty Years After", "Alexandre Dumas", 2), F("The Underground City", "Jules Verne", 2, ["Les Indes noires", "The Child of the Cavern"]),
    F("The Green Ray", "Jules Verne", 2, ["Le Rayon vert"]), F("The Spanish-English Lady", "Miguel de Cervantes", 2, ["La española inglesa"]),
    F("Agricola", "Tacitus", 2), F("Winter Notes on Summer Impressions", "Fyodor Dostoevsky", 2), F("My Past and Thoughts", "Alexander Herzen", 2),
    F("Letters on England", "Voltaire", 2, ["Letters Concerning the English Nation", "Lettres philosophiques"]),
    F("The Carlyle Museum", "Natsume Sōseki", 2, ["カーライル博物館"]), F("Letters from England", "Karel Čapek", 2, ["Anglické listy"]),
    F("Mary Stuart", "Stefan Zweig", 2, ["Maria Stuart"]), F("Gitanjali", "Rabindranath Tagore", 2), F("A Visit to Charles Dickens", "Hans Christian Andersen", 2),
    F("English Fragments", "Heinrich Heine", 2, ["Englische Fragmente"]), F("Beyond the Tweed", "Theodor Fontane", 2, ["Jenseits des Tweed"]),
    F("In Praise of Folly", "Erasmus", 2, ["Moriae Encomium"]), F("Emma", "Kaoru Mori", 2, ["エマ", "Emma: A Victorian Romance"]),
    F("Silver Kites over London", "Xiao Qian", 2, ["银风筝下的伦敦"]),
]

# Legends and medieval anonymous works (LG). Tier 1: the Arthurian core the user asked for on 11-09 plus the medieval works
# already in the database (Chaucer, Robin Hood); tier 2: to decide. Beowulf is left out on purpose: it is set in Scandinavia.
def LG(title, author, tier, also=()):
    return dict(rank=0, title=title, author=author, also=list(also), tier=tier, src=["LG"])
big_read += [
    LG("Le Morte d'Arthur", "Thomas Malory", 1, ["Morte Darthur"]), LG("Idylls of the King", "Alfred, Lord Tennyson", 1),
    LG("Sir Gawain and the Green Knight", "Anonymous (the Gawain Poet)", 1), LG("Roman de Brut", "Wace", 1, ["Arthurian Chronicles"]),
    LG("The Once and Future King", "T. H. White", 1, ["The Sword in the Stone"]), LG("The Canterbury Tales", "Geoffrey Chaucer", 1),
    LG("The Merry Adventures of Robin Hood", "Howard Pyle", 1, ["Robin Hood"]),
    LG("History of the Kings of Britain", "Geoffrey of Monmouth", 2, ["Historia Regum Britanniae"]), LG("Brut", "Layamon", 2),
    LG("The Mabinogion", "Anonymous (Welsh)", 2, ["Mabinogi"]), LG("Piers Plowman", "William Langland", 2),
    LG("Pearl", "Anonymous (the Gawain Poet)", 2), LG("Bede's Ecclesiastical History", "Bede", 2, ["Historia ecclesiastica gentis Anglorum"]),
    LG("The Anglo-Saxon Chronicle", "Anonymous (Anglo-Saxon Chronicle)", 2), LG("The Lais of Marie de France", "Marie de France", 2, ["Lanval", "Chevrefoil"]),
    LG("Tristan", "Gottfried von Strassburg", 2), LG("Chronicles", "Jean Froissart", 2, ["Froissart's Chronicles"]),
]

# Writers who must have at least one book. Tier 1: a writer's house in the lists above, buried in Poets' Corner, or a
# Big Read top-50 book; tier 2: the rest of the lists. Names follow the spelling the database uses.
t1 = set()
for s in sites:
    if s["tier"] == 1 and s["name"] != "Poets' Corner, Westminster Abbey":
        t1.update(s["authors"])
t1.update(PC_BURIED[:12])
t1.update(r["author"] for r in big_read if r["tier"] == 1)
t2 = set(PC_MEMORIAL) | {a for s in sites for a in s["authors"]} | {r["author"] for r in big_read}
t2 -= t1
t2 -= {"Joseph Addison", "Samuel Butler", "James Thomson", "Laurence Binyon", "Edmund Blunden", "Ivor Gurney", "Isaac Rosenberg"}  # kept in the Poets' Corner link check only
authors = [dict(name=a, tier=1) for a in sorted(t1)] + [dict(name=a, tier=2) for a in sorted(t2)]
json.dump(dict(note="Outside checklist for tools/check_coverage.js. Built by build_canon.py from the sources below; do not add entries from memory without marking them.",
               checked=CHECKED, sources=SOURCES, authors=authors, sites=sites, big_read=big_read),
          open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(authors), "authors (tier 1:", len(t1), ")", len(sites), "sites", len(big_read), "Big Read titles")
