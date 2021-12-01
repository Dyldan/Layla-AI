import wolframalpha
import speech_recognition as sr
import pyttsx3
import wikipedia

file_name = r"C:\Users\Dylan\PycharmProjects\Layla\res\layla_user_info.txt"
file = open(file_name, "r")
file_data = file.read()
name = file_data[5:]


def save_name(name_change):
	f = open(file_name, "w")
	f.write("name:" + name_change)
	f.close()


def is_client_query(client_query):
	global name
	if 'name' in client_query or 'call' in client_query:
		if 'my name is' in client_query or 'call me' in client_query:
			words = client_query.split()
			if len(words) < 3 or words[-1] == 'is':
				return False
			name = words[-1]
			engine.say("Alright, I will remember that your name is " + name)
			engine.runAndWait()
			save_name(name)
		elif 'say' in client_query or 'what' in client_query:
			engine.say("You're " + name)
			engine.runAndWait()
		return True
	elif 'goodbye' in client_query or 'quit' in client_query or 'exit' in client_query:
		engine.say("Goodbye")
		engine.runAndWait()
		exit(0)


engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

client = wolframalpha.Client('G5EW4E-YH9UGGP6AH')

r = sr.Recognizer()

while True:
	with sr.Microphone() as source:
		audio_data = r.record(source, duration=5)
		try:
			query = r.recognize_google(audio_data)
		except:
			continue

		print(query)

		if is_client_query(query):
			continue

		try:
			res = client.query(query)
			engine.say(next(res.results).text)
			engine.runAndWait()
			print('--wolfram alpha')
		except:
			try:
				engine.say(wikipedia.summary(query, 1))
				engine.runAndWait()
				print('--wikipedia')
			except:
				engine.say("Sorry, I don't know how to help with that")
				engine.runAndWait()
