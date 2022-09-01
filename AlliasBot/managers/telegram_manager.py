import aioschedule as schedule

from telebot.types import Message
from telebot import types, asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup

from Allias.constants.settings import API_TOKEN, GAME_DURATION
from Allias.models.team import Team
from Allias.models.counter import Counter
from Allias.repositories.inserts import save_team
from Allias.repositories.base import Base, engine, Session
from Allias.repositories.retreives import get_team_by_position, get_max_score_teams
from Allias.repositories.updates import update_team_score_by_id
from Allias.utils.file_utils import get_random_name, get_random_word, get_translation
from Allias.utils.string_utils import get_team_registered_message, get_end_message, get_start_message, get_score_message

bot = AsyncTeleBot(API_TOKEN, state_storage=StateMemoryStorage())
translation = get_translation()

Base.metadata.create_all(engine)
session = Session()
counter = Counter()
team = Team()


class States(StatesGroup):
    rate_word: type(rate_word.__str__()) = State()
    create_team: type(create_team.__str__()) = State()
    update_limit: type(update_limit.__str__()) = State()
    save_custom_name: type(save_custom_name.__str__()) = State()


async def router(message: Message):
    if counter.total < counter.limit:
        await select_team(message)
    else:
        await start_game(message)
        return


@bot.message_handler(commands=['start'])
async def start(message: Message):
    await bot.send_message(message.chat.id, translation.team_count_request)
    await bot.set_state(message.from_user.id, States.update_limit, message.chat.id)


async def select_team(message: Message):
    markup_request = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup_request.add(
        types.InlineKeyboardButton(translation.team_random),
        types.InlineKeyboardButton(translation.team_custom)
    )
    await bot.send_message(message.chat.id, translation.team_name_request, reply_markup=markup_request)
    await bot.set_state(message.from_user.id, States.create_team, message.chat.id)


@bot.message_handler(state=States.update_limit)
async def update_limit(message: Message):
    limit = int(message.text) if message.text.isnumeric() else message.text

    if type(limit) == int:
        counter.limit = limit
        await router(message)
    else:
        await bot.send_message(message.chat.id, translation.unsupported_request)


@bot.message_handler(state=States.create_team)
async def create_team(message: Message):
    name = message.text

    if name == translation.team_custom:
        await bot.send_message(message.chat.id, translation.team_name_request)
        await bot.set_state(message.from_user.id, States.save_custom_name, message.chat.id)
    elif name == translation.team_random:
        await save_random_name(message)
    else:
        await bot.send_message(message.chat.id, translation.unsupported_request)


@bot.message_handler(state=States.save_custom_name)
async def save_custom_name(message: Message):
    name = message.text

    if type(name) == str:
        save_team(counter.total, name)
        counter.total += 1

        await bot.send_message(message.chat.id, translation.team_registered)
        await router(message)
    else:
        await bot.send_message(message.chat.id, translation.unsupported_request)


async def save_random_name(message: Message):
    name = get_random_name()

    save_team(counter.total, name)
    counter.total += 1

    await bot.send_message(message.chat.id, get_team_registered_message(name, translation.team_registered),
                           parse_mode='html')
    await router(message)


async def start_game(message: Message):
    teams = get_team_by_position(counter.total)

    if len(teams) == 0:
        await end_game(message)
        return

    t = teams.pop()
    team.id = t.id
    team.name = t.name
    team.score = t.score
    team.position = t.position

    schedule \
        .every(GAME_DURATION).seconds \
        .do(switch_team, message) \
        .tag(message.chat.id)

    await bot.send_message(message.chat.id, get_start_message(team.name, translation.start_message), parse_mode='html')
    await show_word(message)


async def end_game(message: Message):
    teams = get_max_score_teams()
    winners = [t.name for t in teams] if len(teams) > 1 else teams.pop().name

    await bot.send_message(message.chat.id, get_end_message(winners, translation.end_message), parse_mode='html',
                           reply_markup=None)
    await bot.delete_state(message.from_user.id, message.chat.id)


async def show_word(message: Message):
    word = get_random_word()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton(translation.plus),
               types.InlineKeyboardButton(translation.minus))

    await bot.send_message(message.chat.id, f'<b>{word}</b>', reply_markup=markup, parse_mode='html')
    await bot.set_state(message.from_user.id, States.rate_word, message.chat.id)


@bot.message_handler(state=States.rate_word)
async def rate_word(message: Message):
    if message.text == translation.plus:
        team.score += 1
        update_team_score_by_id(team.id, team.score)
        await bot.send_message(message.chat.id, get_score_message(team.score), parse_mode='html')
        await show_word(message)
    elif message.text == translation.minus:
        team.score -= 1
        update_team_score_by_id(team.id, team.score)
        await bot.send_message(message.chat.id, get_score_message(team.score), parse_mode='html')
        await show_word(message)


async def switch_team(message: Message):
    schedule.clear(message.chat.id)
    counter.total -= 1
    await start_game(message)


@bot.message_handler(state="*")
async def any_state(message):
    await bot.send_message(message.chat.id, translation.unsupported_request)


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
