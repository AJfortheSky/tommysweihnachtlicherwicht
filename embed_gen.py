from hikari import Embed, InteractionMember
from datetime import datetime


TUERCHEN_SPAWN_EMBED: Embed = Embed(
    title='Ein Türchen ist gespawned!',
    description='Sei schnell und claime es!',
    colour='#e61405',
    timestamp=datetime.now().astimezone()
)


# noinspection PyPep8Naming
async def GET_TUERCHEN_COMMAND(member: InteractionMember | None, tuerchen: int) -> Embed:
    if not member:
        return Embed(
            title='Türchen',
            description=f'Du hast {tuerchen} Türchen!',
            colour='#e61405'
    )

    else:
        return Embed(
            title='Türchen',
            description=f'{member} hat {tuerchen} Türchen!',
            colour='#e61405'
        )




