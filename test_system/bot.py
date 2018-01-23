import config
import telebot
import subprocess

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["document"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    try:
        file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        downloaded_file = bot.download_file(file_info.file_path)
        src='downloaded/' + message.document.file_name;
        with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)
        bot.reply_to(message, 'Document "{}" received'.format(file_name))
        
        source_name, source_type = file_name.split('.')
        command = "g++ downloaded/{} -o {}".format(file_name, source_name)
        bot.reply_to(message, 'Compilation process started: executing command "{}"'.format(command))
        subprocess.call(command, shell=True)
        output = subprocess.check_output(r'./{}'.format(source_name))
        bot.reply_to(message, 'Program returned "{}"'.format(output))
        subprocess.call('rm {}'.format(source_name), shell=True)
        bot.reply_to(message, 'Program "{}" deleted'.format(source_name))
    except Exception as e:
        bot.reply_to(message, e)
        
if __name__ == '__main__':
    bot.polling(none_stop=True)
