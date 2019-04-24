import speech_recognition as sr


def speech_to_text(time, buff):
    """

    :time:
    :buff:
    """


    rec = sr.Recognizer()
    with sr.AudioFile(buff) as source:
        audio = rec.record(source)

    # recognize speech using Sphinx
    try:
        phrase = rec.recognize_sphinx(audio)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    return time, phrase
