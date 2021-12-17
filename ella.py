#encoding=utf8
from Tkinter import *
from PIL import Image, ImageTk
import aiml, os, sys, win32ui
import OpenOPC, pyttsx3, threading
import speech_recognition as sr

# настройка кодировки
reload(sys)
sys.setdefaultencoding('utf8')

# список комман управления механизмами стенда
lst_command1 = ["M_FAN_ON", "M_FAN_OFF", "M_DRV_ON", "M_DRV_OFF", "M_HTR_ON", "M_HTR_OFF",
				"M_MILL_ON", "M_MILL OFF", "M_CTRL_MODE_ON", "M_CTRL_MODE_OFF", "M_SLCT_PID"]
# Управления голосом бота
lst_command2 =["M_ON_VOICE", "M_OFF_VOICE", "M_ON_WINCC", "M_OFF_WINCC"]
#
firstCallVar = True


# Установка соединие с Server WinCC
try:
    opc = OpenOPC.client()
    opc.connect('OPCServer.WinCC.1')
    win32ui.MessageBox("Good connection with Server", "Alarm")
except Exception:
	win32ui.MessageBox("No connection with Server", "Error")

# загрузка шаблон aiml в мозг brain.brn
kernel = aiml.Kernel()
#if os.path.isfile("bot_brain.brn"):
#    kernel.bootstrap(brainFile = "bot_brain.brn")
#else:
#    kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
#    kernel.saveBrain("bot_brain.brn")
#kernel now ready for use
kernel.learn("aiml\std-startup.xml")
kernel.respond("load aiml b")

# Создаем Tkinter окно для chatbot
root = Tk()
# Размеры окна
width  = 300
height = 420
# ширина экрана
wscreen = root.winfo_screenwidth()
# высота экрана
hscreen = root.winfo_screenheight()
cntr_screenW = (wscreen - width) // 2
cntr_screenH = (hscreen - height) // 2

# Предварительна загружаем все картинки с помошью библиотеки PIL

img2 = Image.open('image\Ella.png')
img2 = ImageTk.PhotoImage(img2)

img3 = Image.open('image\micmphone.png')
img3 = img3.resize((40, 40), Image.BILINEAR)
img3 = ImageTk.PhotoImage(img3)

img4 = Image.open('image\sendbtn2.png')
img4 = img4.resize((35, 35), Image.BILINEAR)
img4 = ImageTk.PhotoImage(img4)

# Создаем переменные для включение Голоса, и Микрофона
onVoice  = False
onMicphn = False
onWinCC  = False
get_rule = ()
get_rule_old = ()
voice = ""

# Функция для потоков используется для декоратора
def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper

# Инициализация. Функция вызивается только один раз
def initial():
	chatText.config(state='normal')
	chatText.insert(END,'Привет меня зовут Элла.\n')
	chatText.insert(END, 'Вот что я умею: \n')
	chatText.insert(END, '1) Управлять станом \n')
	chatText.insert(END, '2) Контролировать стан \n')
	chatText.insert(END, '3) Выводить сообщения об авариях\n')
	chatText.insert(END, 'Чем я могу Вам помочь ...\n')
	chatText.config(state='disabled')

# Функция обработка сообщения от кнопки SEND
def sendMessage():
	readMessageInp()



# Функция включение микрофона
def onMicrophone():
	listenMicrophone()
	
@thread
def listenMicrophone():
	voiceMessage = ""
	r = sr.Recognizer()
	with sr.Microphone() as source:
		# Пишем боту чтобы бот нас слушал
		bot_response = answerBot("Слушать")
		# Загружаем ответ бота к чат окно
		LoadBotEntry(bot_response)
		# Устанавливаем паузу, чтобы прослушивание
		# началось лишь по прошествию 1 секунды
		#r.pause_threshold = 1
		# используем adjust_for_ambient_noise для удаления
		# посторонних шумов из аудио дорожки
		#r.adjust_for_ambient_noise(source, duration=1)
		# Полученные данные записываем в переменную audio
		# пока мы получили лишь mp3 звук
		audio = r.listen(source)
	try: # Обрабатываем все при помощи исключений
		voiceMessage = r.recognize_google(audio, language="ru-RU").lower()
		# Просто отображаем текст что сказал пользователь
		#chatText.insert(END,'{}'.format('Вы сказали'))
	# Если не смогли распознать текст, то будет вызвана эта ошибка
	except Exception:
		LoadBotEntry("Извените я вас не понела или у вас нету соединение с сервером")
		# Здесь просто проговариваем слова "Я вас не поняла"
	# Вызиваем функцию обработчика сообщение
	messageProcess(voiceMessage)

def readMessageInp():
	#Получаем текст от поле ввода
	textMessage = writText.get('1.0', END)
	#После того как прочли удаляем поле
	writText.delete('1.0', END)
	# Вызиваем функцию обработчика сообщение
	messageProcess(textMessage)

def messageProcess(message):
	# Загружаем в чат сообщение пользователья
	LoadMyEntry(message)
	# Задаем вопрос и получаем ответ от бота
	bot_response = answerBot(message)
	print("yes11")
	# Загружаем сообщение бота в чат окно
	if bot_response in lst_command1:
		in_message = ctrlMill(bot_response)
		in_message = answerBot(in_message)
		LoadBotEntry(in_message)
	elif bot_response in lst_command2:
		in_message = ctrlVoice(bot_response)
		in_message = answerBot(in_message)
		LoadBotEntry(in_message)
	else:
		LoadBotEntry(bot_response)

def answerBot(message):
	if message == "save":
		kernel.saveBrain("bot_brain.brn")
	else:
		bot_response = kernel.respond(message)
		return bot_response

def LoadBotEntry(text):
	global onVoice
	global voice
	if text != "":
		voice = text
		text = "Ella: " + text
		chatText.config(state='normal')
		LineNumber = float(chatText.index('end'))-1.0
		chatText.insert(END,'{}'.format(text))
		chatText.insert(END,'\n')
		chatText.tag_add("Ella", LineNumber, LineNumber+0.5)
		chatText.tag_config("Ella", foreground="#FF8000", font=("Arial", 12, "bold"))
		chatText.config(state=DISABLED)
		chatText.yview(END)
		if onVoice == True:
			voiceThread()


def LoadMyEntry(text):
	if text != "":
		text = "User: " + text
		chatText.config(state='normal')
		LineNumber = float(chatText.index('end'))-1.0
		chatText.insert(END,'{}'.format(text))
		chatText.insert(END,'\n')
		chatText.tag_add("User", LineNumber, LineNumber+0.5)
		chatText.tag_config("User", foreground="#04B404", font=("Arial", 12, "bold"))
		chatText.config(state=DISABLED)
		chatText.yview(END)

def voiceThread():
	t = threading.Thread(target=readWithVoice, )
	t.daemon = True
	t.start()


def readWithVoice():
	global voice
	engine = pyttsx3.init()
	engine.setProperty('rate', 160)
	engine.say(voice)
	engine.runAndWait()
	

def ctrlMill(message):
	global onWinCC
	global get_rule
	get_rule = ruleCtrl(message)
	print(get_rule)
	if onWinCC == True:
	    return get_rule[2]

def ctrlVoice(message):
	global onVoice
	global onWinCC

	get_rule = ruleCtrl(message)
	if get_rule[0] == "ON_VOICE":
		onVoice = True
	if get_rule[0] == "OFF_VOICE":
		onVoice = False
	if get_rule[0] == "ON_WINCC":
		onWinCC = True
	if get_rule[0] == "OFF_WINCC":
		onWinCC = False
	return get_rule[2]

def ruleCtrl(command):
	print command
	message = ["уже включаю", "уже выключаю"]
	#Вкл/Выкл голос
	if command == "M_ON_VOICE":
		return "ON_VOICE",  1, message[0]
	elif command == "M_OFF_VOICE":
		return "OFF_VOICE", 0, message[1]
	elif command == "M_ON_WINCC":
		return "ON_WINCC",  1, message[0]
	elif command == "M_OFF_WINCC":
		return "OFF_WINCC", 0, message[1]
	#Комманда для включение вентиляторов стенда
	elif command == "M_FAN_ON":
		return "M_FAN_ON",  1, message[0]
	#Комманда для выключение вентиляторов стенда
	elif command == "M_FAN_OFF":
		return "M_FAN_OFF", 1, message[1]
	#Комманда для включение нагревательного элмента стенда
	elif command == "M_HTR_ON":
		return "M_HTR_ON",  1, message[0]
	#Комманда для выключение нагревательного элмента стенда
	elif command == "M_HTR_OFF":
		return "M_HTR_OFF", 1, message[1]
	#Комманда для включение двигателя стенда
	elif command == "M_DRV_ON":
		return  "M_DRV_ON", 1, message[0]
	#Комманда для выключение двигателя стенда
	elif command == "M_DRV_OFF":
		return "M_DRV_OFF", 1, message[1]
	#Выбор режима управления

	#Комманда для запуска стенда в автматическом режиме
	else:
		return "Я не поняла вашу команду"


root.resizable(False,False)
root.title('ELLA')
root.geometry('{}x{}+{}+{}'.format(width, height, cntr_screenW, cntr_screenH))

headFrame = Frame(root)
logoImg = Label(headFrame, width = 64, height = 64, image = img2)
logoImg.pack(side = LEFT)
logoText = Label(headFrame, font='tahoma 8', justify = LEFT, text='ЭЛЛА\nИсскуственный\nинтеллект')
logoText.pack(side = LEFT)
logoMicr = Button(headFrame, width=40, height=40, relief='flat', bd=1, image= img3, command = onMicrophone)
logoMicr.pack(side=RIGHT, padx =5)
headFrame.pack(anchor=N, fill=X)

#Chat Frame
chatFrame = Frame(root)
scrollbar = Scrollbar(chatFrame)
scrollbar.pack(side=RIGHT, fill=Y)
chatText = Text(chatFrame, font = '14', width =55, height = 15, wrap=WORD, relief='flat', yscrollcommand=scrollbar.set)

chatText.config(state='disabled')
chatText.pack(side="left")
chatFrame.pack(padx = 5, pady=5)

#Write Frame
writeFrame = Frame(root)
writText = Text(writeFrame, font = '14', width=27, height = 3, wrap=WORD, relief='flat')
writText.pack(side=LEFT)
sendBtn = Button(writeFrame, image=img4, height=54, width=45, bg='white', relief='flat', bd=1, command=sendMessage)
sendBtn.pack(side=LEFT)
writeFrame.pack(padx = 5)

#Вызов функции инициализации
if firstCallVar == True:
	initial()
	firstCallVar =False
def opcTrans():
	if onWinCC == True:
		global get_rule
		global get_rule_old
		if get_rule != get_rule_old:
			print("Yes get_rule")
			opc.write((get_rule[0], int(get_rule[1])))
			opc.write((get_rule[0], 0))
			get_rule_old = get_rule
	root.after(1000, opcTrans)
opcTrans()
root.mainloop()
