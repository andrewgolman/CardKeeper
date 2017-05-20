from db import queries
from packs import packfile

sources = ["db/samples/5000.txt"]
n = 50

for s in sources:
    new_cards = packfile.load(open(s))
    for i in range(len(new_cards) // n):
        queries.new_pack(
            name=str(s[:-4]) + ": pack #" + str(i),
            owner=0,
            cards=new_cards[i*n:(i+1) * n]
        )
    queries.new_group("Learn " + str(s), 0)

supersource = "db/samples/google-10000-english.txt"
new_cards = packfile.load(open(supersource))
queries.new_pack(
    name="Google popular words!",
    owner=0,
    cards=new_cards
)
