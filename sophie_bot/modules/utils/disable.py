from sophie_bot import OPERATORS
from sophie_bot.services.mongo import db
from sophie_bot.utils.logger import log

DISABLABLE_COMMANDS = []


def disableable_dec(command):
    log.debug(f'Adding {command} to the disableable commands...')

    if command not in DISABLABLE_COMMANDS:
        DISABLABLE_COMMANDS.append(command)

    def wrapped(func):
        async def wrapped_1(*args, **kwargs):
            message = args[0]

            chat_id = message.chat.id
            user_id = message.from_user.id
            cmd = command

            if command in (aliases := message.conf['cmds']):
                cmd = aliases[0]

            check = await db.disabled_v2.find_one({'chat_id': chat_id, 'cmds': {'$in': [cmd]}})
            if check and user_id not in OPERATORS:
                return
            return await func(*args, **kwargs)

        return wrapped_1

    return wrapped
