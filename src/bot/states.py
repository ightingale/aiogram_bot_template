from aiogram.fsm.state import State, StatesGroup


class MainMenuSG(StatesGroup):
    start = State()


class AdminMenuSG(StatesGroup):
    start = State()
