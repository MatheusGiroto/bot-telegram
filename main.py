import telebot
import datetime
import schedule
import time
import threading

bot = telebot.TeleBot('6034207043:AAErGIF7nMFBhHcT0fht9l3syvIbh-zUtbA')


def enviar_mensagem(horario_definido):
    mensagem = """🔵🔵Entrada Finalizada🔵🔵

🐯Jogo: Fortune Tiger
🎰Nº de Rodadas: 10(Máximo 15)
🔵Entrar: {}

➡️ ENTRE AQUI : https://fwd.cx/wlYEVjJEzGqc""".format(horario_definido)

    bot.send_message(chat_id='-928882551', text=mensagem)

def verificar_permissao_usuario(user_id):
    usuarios_autorizados = ["1845218557"]  # Lista de IDs de usuários autorizados
    return str(user_id) in usuarios_autorizados

@bot.message_handler(commands=['alterarhorarios'])
def alterar_horarios(message):
    if not verificar_permissao_usuario(message.from_user.id):
        bot.reply_to(message, "Desculpe, você não tem permissão para alterar os horários.")
        return

    horarios = message.text.split()[1:]
    schedule.clear()

    for horario_definido in horarios:
        if ':' in horario_definido:
            hora, minuto = map(int, horario_definido.split(':'))
            horario_envio = datetime.datetime.combine(datetime.datetime.today(),
                                                      datetime.time(hour=hora, minute=minuto)) - datetime.timedelta(
                minutes=2)
            horario_envio_str = horario_envio.strftime('%H:%M')
            schedule.every().day.at(horario_envio_str).do(enviar_mensagem, horario_definido=horario_definido)
            print("Horário alterado:", horario_definido)
        else:
            print("Horário inválido:", horario_definido)

    bot.reply_to(message, "Os horários foram alterados com sucesso.")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
    bot.polling()

if __name__ == '__main__':
    main()