from aiogram.fsm.state import State, StatesGroup

class HeroForm(StatesGroup):
    waiting_category = State()
    waiting_description = State()
    waiting_contacts = State()

class PartnerForm(StatesGroup):
    waiting_info = State()

# Можно добавить другие формы при необходимости