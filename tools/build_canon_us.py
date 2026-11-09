"""Build tools/canon-us.json: the outside checklist for the United States, same shape as canon.json (UK).
Sources (fetched 2026-11-08 and copied below, so the file is reproducible without network):
  WR  Wikipedia, List of residences of American writers
  ML  Modern Library 100 Best Novels (Board's list), sites.prh.com/modern-library-top-100 — American authors only
  GAR PBS The Great American Read, 100 titles (2018; top 10 ranked, the rest alphabetical) — American authors only
Tier 1: a writer's residence on WR, or a book in ML top 50 / GAR top 10. Tier 2: everything else on the lists.
Usage: python3 build_canon_us.py <app_dir>"""
import json, sys
APP = sys.argv[1]

# Wikipedia "List of residences of American writers": (writer as we spell the author, residence, city, state, status)
WR = [
 ("F. Scott Fitzgerald", "The Scott and Zelda Fitzgerald Museum", "Montgomery", "AL", "museum"),
 ("Truman Capote", "Faulk home site", "Monroeville", "AL", ""),
 ("Robinson Jeffers", "Tor House", "Carmel", "CA", ""),
 ("Jack London", "Wolf House and Beauty Ranch (Jack London State Historic Park)", "Glen Ellen", "CA", "state park"),
 ("Eugene O'Neill", "Tao House", "Danville", "CA", "NPS site"),
 ("Upton Sinclair", "Upton Sinclair House", "Monrovia", "CA", ""),
 ("John Steinbeck", "Steinbeck House", "Salinas", "CA", ""),
 ("Eugene O'Neill", "Monte Cristo Cottage", "New London", "CT", ""),
 ("Mark Twain", "Mark Twain House", "Hartford", "CT", "museum"),
 ("Harriet Beecher Stowe", "Harriet Beecher Stowe House", "Hartford", "CT", "museum"),
 ("Noah Webster", "Noah Webster House", "West Hartford", "CT", ""),
 ("Ernest Hemingway", "Ernest Hemingway Home", "Key West", "FL", "museum"),
 ("Zora Neale Hurston", "Zora Neale Hurston House", "Fort Pierce", "FL", ""),
 ("Jack Kerouac", "Jack Kerouac House", "Orlando", "FL", ""),
 ("Marjorie Kinnan Rawlings", "Cross Creek", "Cross Creek", "FL", "state park"),
 ("Joel Chandler Harris", "Wren's Nest", "Atlanta", "GA", "museum"),
 ("Carson McCullers", "Carson McCullers Childhood Home", "Columbus", "GA", ""),
 ("Margaret Mitchell", "Margaret Mitchell House and Museum", "Atlanta", "GA", "museum"),
 ("Flannery O'Connor", "Flannery O'Connor Childhood Home", "Savannah", "GA", "museum"),
 ("Flannery O'Connor", "Andalusia", "Milledgeville", "GA", ""),
 ("Ernest Hemingway", "Ernest Hemingway Birthplace", "Oak Park", "IL", "museum"),
 ("Vachel Lindsay", "Vachel Lindsay House", "Springfield", "IL", ""),
 ("Carl Sandburg", "Carl Sandburg State Historic Site", "Galesburg", "IL", "state historic site"),
 ("John Kennedy Toole", "Toole-Hecker House", "New Orleans", "LA", "private"),
 ("Robert Penn Warren", "Robert Penn Warren House (Twin Oaks)", "Prairieville", "LA", "private"),
 ("Stephen King", "Stephen and Tabitha King home", "Bangor", "ME", "private"),
 ("Sarah Orne Jewett", "Sarah Orne Jewett House", "South Berwick", "ME", "museum"),
 ("Harriet Beecher Stowe", "Harriet Beecher Stowe House", "Brunswick", "ME", ""),
 ("Henry Wadsworth Longfellow", "Wadsworth-Longfellow House", "Portland", "ME", "museum"),
 ("H. L. Mencken", "H. L. Mencken House", "Baltimore", "MD", "museum"),
 ("Rachel Carson", "Rachel Carson House", "Colesville", "MD", ""),
 ("Edgar Allan Poe", "Edgar Allan Poe House and Museum", "Baltimore", "MD", "museum"),
 ("Gertrude Stein", "David Bachrach House", "Baltimore", "MD", "private"),
 ("Virginia Lee Burton", "Virginia Lee Burton Writing Cottage", "Gloucester", "MA", ""),
 ("E. E. Cummings", "E. E. Cummings House", "Cambridge", "MA", ""),
 ("Edward Gorey", "Edward Gorey House", "Yarmouth Port", "MA", "museum"),
 ("Emily Dickinson", "Emily Dickinson Museum", "Amherst", "MA", "museum"),
 ("Louisa May Alcott", "The Wayside", "Concord", "MA", "NPS site"),
 ("Louisa May Alcott", "Orchard House", "Concord", "MA", "museum"),
 ("Ralph Waldo Emerson", "Ralph Waldo Emerson House", "Concord", "MA", "museum"),
 ("Henry Wadsworth Longfellow", "Longfellow House–Washington's Headquarters", "Cambridge", "MA", "NPS site"),
 ("Herman Melville", "Arrowhead", "Pittsfield", "MA", "museum"),
 ("Nathaniel Hawthorne", "Nathaniel Hawthorne Birthplace", "Salem", "MA", "museum"),
 ("Nathaniel Hawthorne", "The Wayside", "Concord", "MA", "NPS site"),
 ("Henry David Thoreau", "Thoreau–Alcott House", "Concord", "MA", "private"),
 ("Edith Wharton", "The Mount", "Lenox", "MA", "museum"),
 ("Ernest Hemingway", "Windemere Cottage", "Petoskey", "MI", "private"),
 ("Theodore Roethke", "Roethke Houses", "Saginaw", "MI", ""),
 ("F. Scott Fitzgerald", "F. Scott Fitzgerald House (Summit Terrace)", "Saint Paul", "MN", "private"),
 ("Sinclair Lewis", "Sinclair Lewis Boyhood Home", "Sauk Centre", "MN", "museum"),
 ("William Faulkner", "Rowan Oak", "Oxford", "MS", "museum"),
 ("Eudora Welty", "Eudora Welty House", "Jackson", "MS", "museum"),
 ("Maya Angelou", "Maya Angelou Birthplace", "St. Louis", "MO", ""),
 ("Kate Chopin", "Kate Chopin House", "St. Louis", "MO", ""),
 ("Mark Twain", "Mark Twain Boyhood Home", "Hannibal", "MO", "museum"),
 ("Laura Ingalls Wilder", "Laura Ingalls Wilder House (Rocky Ridge Farm)", "Mansfield", "MO", "museum"),
 ("Willa Cather", "Willa Cather Childhood Home", "Red Cloud", "NE", "museum"),
 ("Robert Frost", "Robert Frost Farm", "Derry", "NH", "state historic site"),
 ("Robert Frost", "The Frost Place", "Franconia", "NH", "museum"),
 ("H. A. Rey", "Curious George Cottage", "Waterville Valley", "NH", ""),
 ("Stephen Crane", "Arbutus Cottage", "Asbury Park", "NJ", ""),
 ("Walt Whitman", "Walt Whitman House", "Camden", "NJ", "museum"),
 ("William Carlos Williams", "William Carlos Williams House", "Rutherford", "NJ", ""),
 ("James Baldwin", "James Baldwin Residence", "New York", "NY", ""),
 ("Washington Irving", "Sunnyside", "Tarrytown", "NY", "museum"),
 ("Langston Hughes", "Langston Hughes House", "New York", "NY", ""),
 ("James Weldon Johnson", "James Weldon Johnson Residence", "New York", "NY", ""),
 ("Herman Melville", "Herman Melville House", "Lansingburgh", "NY", ""),
 ("Carson McCullers", "Carson McCullers House", "South Nyack", "NY", ""),
 ("Edna St. Vincent Millay", "Steepletop", "Austerlitz", "NY", "not open"),
 ("Edgar Allan Poe", "Edgar Allan Poe Cottage", "The Bronx, New York", "NY", "museum"),
 ("Mark Twain", "Quarry Farm", "Elmira", "NY", "scholars' retreat"),
 ("Walt Whitman", "Walt Whitman Birthplace", "West Hills", "NY", "museum"),
 ("Carl Sandburg", "Carl Sandburg Home", "Flat Rock", "NC", "NPS site"),
 ("Thomas Wolfe", "Thomas Wolfe House", "Asheville", "NC", "museum"),
 ("Paul Laurence Dunbar", "Paul Laurence Dunbar House", "Dayton", "OH", "museum"),
 ("Harriet Beecher Stowe", "Harriet Beecher Stowe House", "Cincinnati", "OH", "museum"),
 ("James Thurber", "Thurber House", "Columbus", "OH", "museum"),
 ("Zane Grey", "Zane Grey Cabin", "Rogue River", "OR", ""),
 ("Rachel Carson", "Rachel Carson Homestead", "Springdale", "PA", "museum"),
 ("Pearl S. Buck", "Pearl S. Buck House (Green Hills Farm)", "Perkasie", "PA", "museum"),
 ("John Updike", "John Updike Childhood Home", "Shillington", "PA", ""),
 ("Alex Haley", "Alex Haley House and Museum", "Henning", "TN", "museum"),
 ("Katherine Anne Porter", "Katherine Anne Porter House", "Kyle", "TX", ""),
 ("O. Henry", "O. Henry House", "Austin", "TX", "museum"),
 ("Frederick Douglass", "Frederick Douglass National Historic Site", "Washington", "DC", "NPS site"),
 ("Langston Hughes", "Langston Hughes House (12th Street)", "Washington", "DC", ""),
 ("Robert Frost", "Homer Noble Farm", "Ripton", "VT", ""),
 ("Robert Frost", "Robert Frost Stone House Museum", "Shaftsbury", "VT", "museum"),
 ("Rudyard Kipling", "Naulakha", "Dummerston", "VT", ""),
 ("Willa Cather", "Willa Cather Birthplace", "Gore", "VA", ""),
 ("Willa Cather", "Willow Shade", "Winchester", "VA", ""),
 ("Ellen Glasgow", "Ellen Glasgow House", "Richmond", "VA", ""),
 ("Pearl S. Buck", "Pearl S. Buck Birthplace", "Hillsboro", "WV", "museum"),
]

# Modern Library Board's list, American authors only: (rank, title, author)
ML = [
 (2, "The Great Gatsby", "F. Scott Fitzgerald"), (4, "Lolita", "Vladimir Nabokov"), (6, "The Sound and the Fury", "William Faulkner"),
 (7, "Catch-22", "Joseph Heller"), (10, "The Grapes of Wrath", "John Steinbeck"), (16, "An American Tragedy", "Theodore Dreiser"),
 (17, "The Heart Is a Lonely Hunter", "Carson McCullers"), (18, "Slaughterhouse-Five", "Kurt Vonnegut"), (19, "Invisible Man", "Ralph Ellison"),
 (20, "Native Son", "Richard Wright"), (21, "Henderson the Rain King", "Saul Bellow"), (22, "Appointment in Samarra", "John O'Hara"),
 (23, "U.S.A.", "John Dos Passos"), (24, "Winesburg, Ohio", "Sherwood Anderson"), (26, "The Wings of the Dove", "Henry James"),
 (27, "The Ambassadors", "Henry James"), (28, "Tender Is the Night", "F. Scott Fitzgerald"), (29, "The Studs Lonigan Trilogy", "James T. Farrell"),
 (32, "The Golden Bowl", "Henry James"), (33, "Sister Carrie", "Theodore Dreiser"), (35, "As I Lay Dying", "William Faulkner"),
 (36, "All the King's Men", "Robert Penn Warren"), (37, "The Bridge of San Luis Rey", "Thornton Wilder"), (39, "Go Tell It on the Mountain", "James Baldwin"),
 (42, "Deliverance", "James Dickey"), (45, "The Sun Also Rises", "Ernest Hemingway"), (50, "Tropic of Cancer", "Henry Miller"),
 (51, "The Naked and the Dead", "Norman Mailer"), (52, "Portnoy's Complaint", "Philip Roth"), (53, "Pale Fire", "Vladimir Nabokov"),
 (54, "Light in August", "William Faulkner"), (55, "On the Road", "Jack Kerouac"), (56, "The Maltese Falcon", "Dashiell Hammett"),
 (58, "The Age of Innocence", "Edith Wharton"), (60, "The Moviegoer", "Walker Percy"), (61, "Death Comes for the Archbishop", "Willa Cather"),
 (62, "From Here to Eternity", "James Jones"), (63, "The Wapshot Chronicle", "John Cheever"), (64, "The Catcher in the Rye", "J. D. Salinger"),
 (68, "Main Street", "Sinclair Lewis"), (69, "The House of Mirth", "Edith Wharton"), (73, "The Day of the Locust", "Nathanael West"),
 (74, "A Farewell to Arms", "Ernest Hemingway"), (81, "The Adventures of Augie March", "Saul Bellow"), (82, "Angle of Repose", "Wallace Stegner"),
 (86, "Ragtime", "E. L. Doctorow"), (88, "The Call of the Wild", "Jack London"), (91, "Tobacco Road", "Erskine Caldwell"),
 (92, "Ironweed", "William Kennedy"), (96, "Sophie's Choice", "William Styron"), (97, "The Sheltering Sky", "Paul Bowles"),
 (98, "The Postman Always Rings Twice", "James M. Cain"), (100, "The Magnificent Ambersons", "Booth Tarkington"),
]

# PBS Great American Read, American authors only: (rank or None, title, author)
GAR = [
 (1, "To Kill a Mockingbird", "Harper Lee"), (6, "Gone with the Wind", "Margaret Mitchell"), (7, "Charlotte's Web", "E. B. White"),
 (8, "Little Women", "Louisa May Alcott"),
 (None, "A Confederacy of Dunces", "John Kennedy Toole"), (None, "A Prayer for Owen Meany", "John Irving"), (None, "A Separate Peace", "John Knowles"),
 (None, "A Tree Grows in Brooklyn", "Betty Smith"), (None, "The Adventures of Tom Sawyer", "Mark Twain"), (None, "Another Country", "James Baldwin"),
 (None, "Atlas Shrugged", "Ayn Rand"), (None, "Beloved", "Toni Morrison"), (None, "Bless Me, Ultima", "Rudolfo Anaya"),
 (None, "The Brief Wondrous Life of Oscar Wao", "Junot Díaz"), (None, "The Call of the Wild", "Jack London"), (None, "Catch-22", "Joseph Heller"),
 (None, "The Catcher in the Rye", "J. D. Salinger"), (None, "The Color Purple", "Alice Walker"), (None, "Dune", "Frank Herbert"),
 (None, "Flowers in the Attic", "V. C. Andrews"), (None, "Foundation", "Isaac Asimov"), (None, "A Game of Thrones", "George R. R. Martin"),
 (None, "Ghost", "Jason Reynolds"), (None, "Gilead", "Marilynne Robinson"), (None, "The Giver", "Lois Lowry"), (None, "The Godfather", "Mario Puzo"),
 (None, "Gone Girl", "Gillian Flynn"), (None, "The Grapes of Wrath", "John Steinbeck"), (None, "The Great Gatsby", "F. Scott Fitzgerald"),
 (None, "Hatchet", "Gary Paulsen"), (None, "The Help", "Kathryn Stockett"), (None, "The Hunger Games", "Suzanne Collins"),
 (None, "The Hunt for Red October", "Tom Clancy"), (None, "The Intuitionist", "Colson Whitehead"), (None, "Invisible Man", "Ralph Ellison"),
 (None, "The Joy Luck Club", "Amy Tan"), (None, "Jurassic Park", "Michael Crichton"), (None, "Lonesome Dove", "Larry McMurtry"),
 (None, "Looking for Alaska", "John Green"), (None, "The Lovely Bones", "Alice Sebold"), (None, "The Martian", "Andy Weir"),
 (None, "Memoirs of a Geisha", "Arthur Golden"), (None, "Moby-Dick", "Herman Melville"), (None, "The Notebook", "Nicholas Sparks"),
 (None, "The Outsiders", "S. E. Hinton"), (None, "Ready Player One", "Ernest Cline"), (None, "The Sirens of Titan", "Kurt Vonnegut"),
 (None, "The Stand", "Stephen King"), (None, "The Sun Also Rises", "Ernest Hemingway"), (None, "Swan Song", "Robert R. McCammon"),
 (None, "Tales of the City", "Armistead Maupin"), (None, "Their Eyes Were Watching God", "Zora Neale Hurston"),
 (None, "Watchers", "Dean Koontz"), (None, "Where the Red Fern Grows", "Wilson Rawls"), (None, "The Da Vinci Code", "Dan Brown"),
 (None, "The Clan of the Cave Bear", "Jean M. Auel"), (None, "The Coldest Winter Ever", "Sister Souljah"), (None, "Left Behind", "Tim LaHaye"),
 (None, "This Present Darkness", "Frank E. Peretti"), (None, "The Twilight Saga", "Stephenie Meyer"), (None, "The Shack", "William P. Young"),
 (None, "Mind Invaders", "Dave Hunt"),
]

# authors who already exist in the UK data: spell them exactly the same (packs/existing-ids.json)
EXISTING = {"Henry James", "Jack London", "Washington Irving", "T. S. Eliot", "Rudyard Kipling"}

authors = {}
def add(name, tier, why):
    a = authors.setdefault(name, {"name": name, "tier": 2, "why": []})
    a["tier"] = min(a["tier"], tier); a["why"].append(why)
sites = []
for w, res, city, st, status in WR:
    add(w, 1, f"residence: {res}, {city}, {st}")
    sites.append({"name": f"{res}, {city}", "state": st, "authors": [w], "status": status, "src": ["WR"], "ids": [], "tier": 1})
for r, t, a in ML: add(a, 1 if r <= 50 else 2, f"Modern Library #{r}: {t}")
for r, t, a in GAR: add(a, 1 if r else 2, f"Great American Read{' #' + str(r) if r else ''}: {t}")
books = [{"title": t, "author": a, "src": "ML", "rank": r} for r, t, a in ML] + [{"title": t, "author": a, "src": "GAR", "rank": r} for r, t, a in GAR]
out = {
 "note": "Outside checklist for the United States, same shape as canon.json. Pick new content from the gaps in this list, not from memory; write decisions not to do something into coverage-decisions.json with a reason.",
 "checked": "2026-11-08",
 "country": "us",
 "sources": {
  "WR": ["List of residences of American writers (Wikipedia)", "https://en.wikipedia.org/wiki/List_of_residences_of_American_writers"],
  "ML": ["Modern Library 100 Best Novels, Board's list (American authors only)", "https://sites.prh.com/modern-library-top-100"],
  "GAR": ["PBS The Great American Read, 100 titles, 2018 (American authors only; top 10 ranked)", "https://www.pbs.org/the-great-american-read/books/"],
 },
 "existing_authors_spelling": sorted(EXISTING),
 "authors": sorted(authors.values(), key=lambda a: (a["tier"], a["name"])),
 "sites": sites,
 "big_read": books,
}
json.dump(out, open(f"{APP}/tools/canon-us.json", "w"), ensure_ascii=False, indent=1)
t1 = sum(1 for a in authors.values() if a["tier"] == 1)
print(f"authors {len(authors)} (tier 1: {t1}), sites {len(sites)}, books {len(books)}")
