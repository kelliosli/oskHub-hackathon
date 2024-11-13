from aiogram.fsm.state import State, StatesGroup

class FriendForm(StatesGroup):
    adding = State()
    removing = State()
    editing_select = State()
    editing_username = State()
    