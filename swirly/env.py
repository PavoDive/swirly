# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 PavoDive


import pickle
import os


class LessonEnv:
    def __init__(self):
        self.vars = {}
        self.progress = 0
        self.lesson = None

    def save(self, path='lesson_state.pkl'):
        ctx_copy = {
            k: v for k, v in self.vars.items()
            if not k.startswith("__") and not callable(v)
            and not isinstance(v, type(os))
        }
        temp = LessonEnv()
        temp.vars = ctx_copy
        temp.progress = self.progress
        temp.lesson = self.lesson

        with open(path, 'wb') as f:
            pickle.dump(temp, f)

    @staticmethod
    def load(path='lesson_state.pkl'):
        try:
            with open(path, 'rb') as f:
                env = pickle.load(f)

            if not env.lesson:
                raise ValueError("Corrupted state: lesson name is missing.")
            return env
        except (EOFError, pickle.UnpicklingError, AttributeError, ValueError):
            print("⚠️  Corrupted or incomplete state. Starting fresh.")
            return LessonEnv()
    # @staticmethod
    # def load(path='lesson_state.pkl'):
    #     # with open(path, 'rb') as f:
    #     #     return pickle.load(f)
    #     if not env.lesson:
    #         raise ValueError("Corrupted state: lesson name is missing.")
        
    #     try:
    #         with open(path, "rb") as f:
    #             return pickle.load(f)
    #     except (EOFError, pickle.UnpicklingError):
    #         print("⚠️ Corrupted state file. Starting fresh.")
    #         return LessonEnv()
