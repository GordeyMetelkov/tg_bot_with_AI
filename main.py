from imageai.Detection import ObjectDetection
import telebot

#Создаем токен и экземпляр класса telebot
TOKEN = ''
bot = telebot.TeleBot(TOKEN, parse_mode=None)


def detect_obj(image):
    """ Функция определения объектов, принимает в себя путь к фотографии, возвращает
    список строк (объект и вероятность, с которой этот объект определен верно) """
    # Создаем объект класса ObjectDetection и устанавливаем тип модели сети, указываем путь к
    # с моделью и подгружаем ее
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath('yolov3.pt')
    detector.loadModel()

    detections = detector.detectObjectsFromImage(input_image=image,
                                                 output_image_path='output_image.jpg',
                                                 minimum_percentage_probability=30)

    objs = []
    for eachObj in detections:
        obj = (f"{eachObj['name']} : {eachObj['percentage_probability']}")
        objs.append(obj)
    return objs

@bot.message_handler(commands=['start', 'help'])
def start(message):
    name = message.from_user.first_name
    mes = f'Привет, {name}, кидай фото, а я попробую узнать, кто там расположен'
    bot.reply_to(message, mes)


@bot.message_handler(content_types='photo')
def get_photo(message):
    # При отправке фото сохраняет его на сервер под именем input.jpg и отправляет в функцию
    # определения объектов, вводит обратным сообщением фото с определенными объектами и список
    # объектов и вероятностей, с которыми эти объекты определены верно
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    photo_path = 'input.jpg'
    with open(photo_path, 'wb') as file:
        file.write(downloaded_file)
    objs = detect_obj(photo_path)
    new_objs = f'{[obj for obj in objs]}'[1:-1]
    bot.send_photo(message.chat.id, photo=open('output_image.jpg', 'rb'))
    bot.send_message(message.chat.id, new_objs)


bot.polling()
