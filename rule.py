#encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class EllaRule(object):

	def rule(self, command):
		t = ["уже включаю", "уже выключаю"]
		#Вкл/Выкл голос 
		if command == "M_ON_MICPHN":
			return "ON_VOICE", 1, t[0]
		elif command == "M_OFF_MICPHN":
			return "OFF_VOICE", 0, t[1]
		#Комманда для включение вентиляторов стенда
		elif command == "M_FAN_ON":
			return "M_FAN_ON", 1, t[0]
		#Комманда для выключение вентиляторов стенда
		elif command == "M_FAN_OFF":
			return "M_FAN_OFF", 1, t[1]
		#Комманда для включение нагревательного элмента стенда
		elif command == "M_HTR_ON":
			return "M_HTR_ON", 1, t[0]
		#Комманда для выключение нагревательного элмента стенда
		elif command == "M_HTR_OFF":
			return "M_HTR_OFF", 1, t[1]
		#Комманда для включение двигателя стенда
		elif command == "M_DRV_ON":
			return  "M_DRV_ON", 1, t[1]
		#Комманда для выключение двигателя стенда
		elif command == "M_DRV_OFF":
			return "M_DRV_OFF", 1, t[1]
		#Выбор режима управления
		
		#Комманда для запуска стенда в автматическом режиме


		else:
			return "Я не поняла вашу команду"
