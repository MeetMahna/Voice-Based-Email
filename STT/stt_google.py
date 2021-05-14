import speech_recognition as s
sr = s.Recognizer()
print("*recording*")
with s.Microphone() as m:
    audio = sr.listen(m)
    query=sr.recognize_houndify(audio)
    print(query)
    