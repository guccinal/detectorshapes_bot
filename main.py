import cv2
import telebot
token = '5825979927:AAFUmnWKBL1R4yt_r8yaO8jDqgOpQD3wdIk'
bot = telebot.TeleBot(token)
@bot.message_handler(content_types=["photo"])
def photo(message):

    chatId = message.chat.id
    if message.chat.type == 'private':
        f_id = message.photo[-1].file_id
        file_info = bot.get_file(f_id)
        down_file = bot.download_file(file_info.file_path)
        with open('img.jpg', 'wb') as file:
            file.write(down_file)

    def getContours(img):
        global Tri
        global Sq
        global Rect
        global Pent
        global Hexa
        global Circ
        Tri = 0
        Sq = 0
        Rect = 0
        Pent = 0
        Hexa = 0
        Circ = 0
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                cv2.drawContours(imgContours, cnt, 2, (102, 255, 0), 2)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                objectCor = len(approx)
                x, y, w, h = cv2.boundingRect(approx)
                if objectCor == 3:
                    objectType = "ТРЕУГОЛЬНИК"
                    Tri += 1
                elif objectCor == 4:
                    assRatio = w / float(h)
                    if assRatio > 0.95 and assRatio < 1.05:
                        objectType = "КВАДРАТ"
                        Sq += 1
                    else:
                        objectType = "ПРЯМОУГОЛЬНИК"
                        Rect += 1
                elif objectCor == 5:
                    objectType = "ПЯТИУГОЛЬНИК"
                    Pent += 1
                elif objectCor == 6:
                    objectType = "ШЕСТИУГОЛЬНИК"
                    Hexa += 1
                elif objectCor > 6:
                    objectType = "КРУГ"
                    Circ += 1
                else:
                    objectType = "None"
                cv2.putText(imgContours, objectType, (x + (w // 2) - 50, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX,
                            0.55, (102, 255, 0), 1)

    path = "img.jpg"
    img = cv2.imread(path)
    imgContours = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    getContours(imgCanny)
    cv2.imwrite('imgtosend.jpg', imgContours)
    cv2.waitKey(0)
    otpravka = open('imgtosend.jpg', 'rb')
    bot.send_photo(chatId, otpravka)

    bot.send_message(chatId, ('Треугольников: ' + ((str(Tri // 4)) * (Tri // Tri))))
    bot.send_message(chatId, ('Квадратов: ' + ((str(Sq // 4)) * (Sq // Sq))))
    bot.send_message(chatId, ('Прямоугольников: ' + ((str(Rect // 4)) * (Rect // Rect))))
    bot.send_message(chatId, ('Пятиугольников: ' + ((str(Pent // 4)) * (Pent // Pent))))
    bot.send_message(chatId, ('Шестиугольников: ' + ((str(Hexa // 4)) * (Hexa // Hexa))))
    bot.send_message(chatId, ('Кругов: ' + ((str(Circ // 4)) * (Circ // Circ))))
bot.infinity_polling()
