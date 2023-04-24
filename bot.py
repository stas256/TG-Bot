import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# https://api.kinopoisk.dev/v1/documentation
# токен тг бота
TOKEN = ""
# токен апи кинопоиска
token = ''

def getInfoByID(_id):
    url = f"https://api.kinopoisk.dev/v1/movie/{_id}"
    headers = {
        'accept': 'application/json',
        'X-API-KEY': '7Z5EJVE-QGB49XN-PSEJ2X9-T3VWW83'
    }
    response = requests.get(url, headers=headers)
    return response.json()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Команды:\n'
    text += '/random - Случайный фильм'
    text += '/search {название} - Поиск фильма по названию'
    text += '/like {ID} - Поиск похожих фильмв'
    text += 'ID можно узнать с помощью /search'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text ='Выбираю фильм...'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    url = f"https://api.kinopoisk.dev/v1/movie/random"
    headers = {
        'accept': 'application/json',
        'X-API-KEY': '7Z5EJVE-QGB49XN-PSEJ2X9-T3VWW83'
    }
    while True:
        response = requests.get(url, headers=headers)
        answer = response.json()

        try:
            if answer['shortDescription'] == None:
                continue
            res = f'''
{answer['name']} ({answer['premiere']['world'][:4]} год)
ID: {answer['id']}
Рейтинг КиноПоиск: {answer['rating']['kp']}
Рейтинг IMDB: {answer['rating']['imdb']}

{answer['shortDescription']}
{answer['poster']['url']}'''
            break
        except:
            pass
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=res)

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search = ' '.join(context.args)
    if search == '':
        text = 'Отправлен пустой запрос\n'
        text += 'Отправьте запрос в формате /search {название}'
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    text ='Ищу фильм...'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    url = f"https://api.kinopoisk.dev/v1.2/movie/search?page=1&limit=1&query='{search}'"
    headers = {
        'accept': 'application/json',
        'X-API-KEY': '7Z5EJVE-QGB49XN-PSEJ2X9-T3VWW83'
    }
    response = requests.get(url, headers=headers)
    answer = response.json()
    print(answer)
    if answer['docs'][0]['name'] == '':
        text = 'По вашему запросу ничего не найдено\n'
        text += 'Попробуйте еще раз'
        return await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    text = f'''
{answer['docs'][0]['name']} ({answer['docs'][0]['year']} год)
ID: {answer['docs'][0]['id']}
Рейтинг КиноПоиск: {answer['docs'][0]['rating']}

{answer['docs'][0]['shortDescription']}
{answer['docs'][0]['poster']}'''
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _id = ' '.join(context.args)
    if not _id.isdigit():
        text = 'Отправлен неверный запрос\n'
        text += 'Отправьте запрос в формате /like {ID}'
        text += 'ID можно узнать с помощью команды /search'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    
    text ='Ищу похожие фильмы...'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    answer = getInfoByID(_id)
    text = ''
    for i in range(len(answer["similarMovies"][:10])):
        text += f"{i + 1}) {answer['similarMovies'][i]['name']}\n"
        text += f"ID: {answer['similarMovies'][i]['id']}\n"
    text = text[:-1]

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    random_handler = CommandHandler('random', random)
    search_handler = CommandHandler('search', search)
    like_handler = CommandHandler('like', like)
    application.add_handler(start_handler)
    application.add_handler(random_handler)
    application.add_handler(search_handler)
    application.add_handler(like_handler)
    
    application.run_polling()
