from aiogram.fsm.state import State, StatesGroup


class BuyUC(StatesGroup):
    choosing_amount = State()
    entering_pubg_id = State()
    sending_receipt = State()


class AdminReject(StatesGroup):
    entering_reason = State()


class AdminPrice(StatesGroup):
    entering_new_price = State()
    entering_new_amount = State()
    entering_new_amount_price = State()


class AdminManage(StatesGroup):
    adding_admin_id = State()
    removing_admin_id = State()
