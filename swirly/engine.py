# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 Your Name


from swirly.env import LessonEnv
from swirly import commands

COMMANDS = {
    'bye': commands.bye,
    'next': commands.next,
    'play': commands.play,
    'reveal': commands.reveal,
    'info': commands.info,
    # add more later
}


def dispatch(user_input: str, env: LessonEnv):
    cmd = user_input.strip()
    if cmd in COMMANDS:
        COMMANDS[cmd](env)
        return True
    return False
