import tinydb
from tinydb import TinyDB, Query
import hikari

db: TinyDB = TinyDB('storage.json')

User: tinydb.queries.Query = Query()


async def add_türchen(member: hikari.Member, amount: int) -> bool:
    try:
        res: list[dict] = db.search(User.id == member.id)
        türchen: int = res[0]['türchen']
        türchen += amount
        db.update({'türchen': türchen}, User.id == member.id)
        return True
    except ValueError:
        return False


async def gen_leaderboard() -> hikari.Embed:
    results: list[dict[str, int]] = db.all()
    scores: list[str, int] = list()
    for res in results:
        scores.append([res['name'], res["türchen"]])

    scores.sort(key=lambda x: x[1], reverse=True)

    embed: hikari.Embed = hikari.Embed(
        title="Leaderboard",
        colour='#f50515'
    )

    for score in scores:
        embed.add_field(name=score[0], value=score[1], inline=True)

    return embed


async def subtract_türchen(member: hikari.Member, amount: int) -> bool:
    res: list[dict] = db.search(User.id == member.id)
    türchen: int = res[0]['türchen']
    try:
        assert türchen >= amount
        türchen -= amount
        db.update({'türchen': türchen}, User.id == member.id)
        return True
    except AssertionError:
        return False


async def insert_user(member: hikari.Member, türchen: int) -> None:
    if not db.contains(User.id == member.id):
        db.insert({'name': member.username, 'id': member.id, 'türchen': türchen})
        return
    else:
        await add_türchen(member, 1)
