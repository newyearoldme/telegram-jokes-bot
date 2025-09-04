from aiogram.fsm.state import StatesGroup, State

class FavoritesState(StatesGroup):
    viewing_list = State()
    viewing_joke = State()
