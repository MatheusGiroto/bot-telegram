import datetime
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot_token = '6034207043:AAErGIF7nMFBhHcT0fht9l3syvIbh-zUtbA'
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def enviar_mensagem(horario_definido):
    mensagem = """🔵🔵Entrada Finalizada🔵🔵

🐯Jogo: Fortune Tiger
🎰Nº de Rodadas: 10(Máximo 15)
🔵Entrar: {}

➡️ ENTRE AQUI : https://fwd.cx/wlYEVjJEzGqc""".format(horario_definido)

    await bot.send_message(chat_id='-928882551', text=mensagem)


def verificar_permissao_usuario(user_id):
    usuarios_autorizados = ["1845218557"]  # Lista de IDs de usuários autorizados
    return str(user_id) in usuarios_autorizados


async def enviar_mensagem_intermediario(horario_envio, horario_definido):
    await asyncio.sleep((horario_envio - datetime.datetime.now()).total_seconds())
    await enviar_mensagem(horario_definido)


@dp.message_handler(commands=['alterarhorarios'])
async def alterar_horarios(message: types.Message):
    if not verificar_permissao_usuario(message.from_user.id):
        await message.reply("Desculpe, você não tem permissão para alterar os horários.")
        return

    horarios = message.text.split()[1:]
    tarefas = []
    for horario_definido in horarios:
        if ':' in horario_definido:
            hora_minuto = horario_definido.split(':')
            if len(hora_minuto) == 2:
                hora, minuto = map(int, hora_minuto)
                horario_envio = datetime.datetime.combine(datetime.datetime.today(),
                                                          datetime.time(hour=hora, minute=minuto)) - datetime.timedelta(
                    minutes=2)
                horario_envio_str = horario_envio.strftime('%H:%M')

                tarefa = enviar_mensagem_intermediario(horario_envio, horario_definido)
                tarefas.append(tarefa)
                print("Horário agendado:", horario_definido)
            else:
                print("Horário inválido:", horario_definido)
        else:
            print("Horário inválido:", horario_definido)

    await asyncio.gather(*tarefas)
    await message.reply("Os horários foram alterados com sucesso.")


async def on_startup(dp):
    await bot.send_message(chat_id='-928882551', text='Bot iniciado')


async def start_bot():
    await dp.bot.send_message(chat_id='-928882551', text='Bot iniciado')
    await dp.start_polling()


def main():
    asyncio.run(start_bot())


if __name__ == '__main__':
    main()
