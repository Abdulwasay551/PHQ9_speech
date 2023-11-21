from flask import Flask, render_template, jsonify, send_from_directory
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from logging.config import dictConfig
import threading
import time
import cv2
import os

app = Flask(__name__)

# Variable to store the status of audio playback
audio_playing = False
recording_flag = True
stop_event = threading.Event()
total_score = 0
score = 0

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


# Function to play audio in a separate thread
def play_audio(filename):
    global audio
    try:
        audio = AudioSegment.from_mp3(filename)
        play(audio)
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        return audio


@app.route('/')
def Homepage():
    return render_template('Homepage.html')


@app.route('/greeting', methods=['POST'])
def play_greeting():
    global audio_playing
    if not audio_playing:
        audio_playing = True
        audio_thread = threading.Thread(target=play_audio, args=('Greeting.mp3',))
        audio_thread.start()

    return jsonify({'status': 'success'})


# Function to record video
def record_video():
    global video, recording_flag, stop_event
    video = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('static/output.mp4', fourcc, 30.0, (1280, 720))

    while recording_flag:
        ret, frame = video.read()
        if ret:
            frame = cv2.resize(frame, (1280, 720))
            out.write(frame)
            cv2.imshow('Recording...', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

        # Check for the stop event
        if stop_event.is_set():
            break
        # Release everything when recording is done
    video.release()
    out.release()
    cv2.destroyAllWindows()


@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/start/start_audio', methods=['POST'])
def start_audio_question():
    global audio_playing, video_thread
    video_thread = threading.Thread(target=record_video)
    video_thread.start()
    if not audio_playing:
        audio_playing = True
        audio_thread = threading.Thread(target=play_audio, args=('Question 1.mp3',))
        audio_thread.start()

    return jsonify({'status': 'success'})


@app.route('/start/stop_audio', methods=['POST'])
def stop_audio():
    global audio_playing, total_score, score
    audio_playing = False
    time.sleep(1)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

        if any(word in text.lower() for word in ["not", "4", "four"]):
            score = 0
        elif any(word in text.lower() for word in ["several", "3", "three"]):
            score = 1
        elif any(word in text.lower() for word in ["half", "2", "two"]):
            score = 2
        elif any(word in text.lower() for word in ["every", "1", "one"]):
            score = 3
        else:
            score = "Sorry can you repeat it"
            app.logger.error('testing error log')
            print("error")
        if score == "Sorry can you repeat it":
            pass
        else:
            total_score = score

        return jsonify({'status': 'success', 'text': text, 'score': score})

    except sr.UnknownValueError:
        return jsonify({'status': 'error', 'message': 'Speech Recognition could not understand audio'})


@app.route('/question2')
def question2():
    return render_template('question2.html')


@app.route('/question3')
def question3():
    return render_template('question3.html')


@app.route('/question4')
def question4():
    return render_template('question4.html')


@app.route('/question5')
def question5():
    return render_template('question5.html')


@app.route('/question6')
def question6():
    return render_template('question6.html')


@app.route('/question7')
def question7():
    return render_template('question7.html')


@app.route('/question8')
def question8():
    return render_template('question8.html')


@app.route('/question9')
def question9():
    return render_template('question9.html')


def result(r_score):
    if r_score in range(0, 4):
        totals = "Minimal or None"
    elif r_score in range(5, 9):
        totals = "Mild"
    elif r_score in range(10, 14):
        totals = "Moderate"
    elif r_score in range(15, 19):
        totals = "Moderately severe"
    else:
        totals = "Severe"
    return totals


@app.route('/results/video')
def video():
    return render_template('video.html')


@app.route('/results/video/<path:filename>')
def get_video(filename):
    return send_from_directory('static', filename)


def comments(r_score):
    if r_score in range(0, 4):
        comment = "Monitor; may not require treatment"
    elif r_score in range(5, 14):
        comment = "Use clinical judgment (symptom duration, functional impairment) to determine necessity of treatment"
    else:
        comment = "Warrants active treatment with psychotherapy, medications, or combination"
    return comment


@app.route('/results')
def results():
    totals = result(total_score)
    comment = comments(total_score)
    return render_template('results.html', total_score=total_score, totals=totals, comment=comment)


@app.route('/question2/start_audio_2', methods=['POST'])
def start_audio_2():
    global audio_playing
    if not audio_playing:
        audio_playing = True
        audio_thread = threading.Thread(target=play_audio, args=('Question 2.mp3',))
        audio_thread.start()

    return jsonify({'status': 'success'})


@app.route('/question2/stop_audio_2', methods=['POST'])
def stop_audio_2():
    global audio_playing, total_score, score_2
    audio_playing = False
    time.sleep(1)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

        if any(word in text.lower() for word in ["not", "4", "four"]):
            score_2 = 0
        elif any(word in text.lower() for word in ["several", "3", "three"]):
            score_2 = 1
        elif any(word in text.lower() for word in ["half", "2", "two"]):
            score_2 = 2
        elif any(word in text.lower() for word in ["every", "1", "one"]):
            score_2 = 3
        else:
            score_2 = "Sorry can you repeat it"
            app.logger.error('testing error log')
            print("error")
        if score_2 == "Sorry can you repeat it":
            pass
        else:
            total_score += score_2

        return jsonify({'status': 'success', 'text': text, 'score': score_2})

    except sr.UnknownValueError:
        return jsonify({'status': 'error', 'message': 'Speech Recognition could not understand audio'})


@app.route('/question3/start_audio_3', methods=['POST'])
def start_audio_3():
    global audio_playing
    if not audio_playing:
        audio_playing = True
        audio_thread = threading.Thread(target=play_audio, args=('Question 3.mp3',))
        audio_thread.start()

    return jsonify({'status': 'success'})


@app.route('/question3/stop_audio_3', methods=['POST'])
def stop_audio_3():
    global audio_playing, total_score, score_3
    audio_playing = False
    time.sleep(1)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

        if any(word in text.lower() for word in ["not", "4", "four"]):
            score_3 = 0
        elif any(word in text.lower() for word in ["several", "3", "three"]):
            score_3 = 1
        elif any(word in text.lower() for word in ["half", "2", "two"]):
            score_3 = 2
        elif any(word in text.lower() for word in ["every", "1", "one"]):
            score_3 = 3
        else:
            score_3 = "Sorry can you repeat it"
            app.logger.error('testing error log')
            print("error")
        if score_3 == "Sorry can you repeat it":
            pass
        else:
            total_score += score_3

        return jsonify({'status': 'success', 'text': text, 'score': score_3})

    except sr.UnknownValueError:
        return jsonify({'status': 'error', 'message': 'Speech Recognition could not understand audio'})


@app.route('/question4/start_audio_4', methods=['POST'])
def start_audio_4():
    global audio_playing
    if not audio_playing:
        audio_playing = True
        audio_thread = threading.Thread(target=play_audio, args=('Question 4.mp3',))
        audio_thread.start()

    return jsonify({'status': 'success'})


@app.route('/question4/stop_audio_4', methods=['POST'])
def stop_audio_4():
    global audio_playing, total_score, score_4
    audio_playing = False
    time.sleep(1)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

        if any(word in text.lower() for word in ["not", "4", "four"]):
            score_4 = 0
        elif any(word in text.lower() for word in ["several", "3", "three"]):
            score_4 = 1
        elif any(word in text.lower() for word in ["half", "2", "two"]):
            score_4 = 2
        elif any(word in text.lower() for word in ["every", "1", "one"]):
            score_4 = 3
        else:
            score_4 = "Sorry can you repeat it"
            app.logger.error('testing error log')
            print("error")
        if score_4 == "Sorry can you repeat it":
            pass
        else:
            total_score += score_4

        return jsonify({'status': 'success', 'text': text, 'score': score_4})

    except sr.UnknownValueError:
        return jsonify({'status': 'error', 'message': 'Speech Recognition could not understand audio'})


@app.route('/question5/start_audio_5', methods=['POST'])
def start_audio_5():
    global audio_playing
    if not audio_playing:
        audio_playing = True
        audio_thread = threading.Thread(target=play_audio, args=('Question 5.mp3',))
        audio_thread.start()

    return jsonify({'status': 'success'})


@app.route('/question5/stop_audio_5', methods=['POST'])
def stop_audio_5():
    global audio_playing, total_score, score_5
    audio_playing = False
    time.sleep(1)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

        if any(word in text.lower() for word in ["not", "4", "four"]):
            score_5 = 0
        elif any(word in text.lower() for word in ["several", "3", "three"]):
            score_5 = 1
        elif any(word in text.lower() for word in ["half", "2", "two"]):
            score_5 = 2
        elif any(word in text.lower() for word in ["every", "1", "one"]):
            score_5 = 3
        else:
            score_5 = "Sorry can you repeat it"
            app.logger.error('testing error log')
            print("error")
        if score_5 == "Sorry can you repeat it":
            pass
        else:
            total_score += score_5

        return jsonify({'status': 'success', 'text': text, 'score': score_5})

    except sr.UnknownValueError:
        return jsonify({'status': 'error', 'message': 'Speech Recognition could not understand audio'})


@app.route('/question6/start_audio_6', methods=['POST'])
def start_audio_6():
    global audio_playing
    if not audio_playing:
        audio_playing = True
        audio_thread = threading.Thread(target=play_audio, args=('Question 6.mp3',))
        audio_thread.start()

    return jsonify({'status': 'success'})


@app.route('/question6/stop_audio_6', methods=['POST'])
def stop_audio_6():
    global audio_playing, total_score, score_6
    audio_playing = False
    time.sleep(1)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

        if any(word in text.lower() for word in ["not", "4", "four"]):
            score_6 = 0
        elif any(word in text.lower() for word in ["several", "3", "three"]):
            score_6 = 1
        elif any(word in text.lower() for word in ["half", "2", "two"]):
            score_6 = 2
        elif any(word in text.lower() for word in ["every", "1", "one"]):
            score_6 = 3
        else:
            score_6 = "Sorry can you repeat it"
            app.logger.error('testing error log')
            print("error")
        if score_6 == "Sorry can you repeat it":
            pass
        else:
            total_score += score_6

        return jsonify({'status': 'success', 'text': text, 'score': score_6})

    except sr.UnknownValueError:
        return jsonify({'status': 'error', 'message': 'Speech Recognition could not understand audio'})


@app.route('/question7/start_audio_7', methods=['POST'])
def start_audio_7():
    global audio_playing
    if not audio_playing:
        audio_playing = True
        audio_thread = threading.Thread(target=play_audio, args=('Question 7.mp3',))
        audio_thread.start()

    return jsonify({'status': 'success'})


@app.route('/question7/stop_audio_7', methods=['POST'])
def stop_audio_7():
    global audio_playing, total_score, score_7
    audio_playing = False
    time.sleep(1)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

        if any(word in text.lower() for word in ["not", "4", "four"]):
            score_7 = 0
        elif any(word in text.lower() for word in ["several", "3", "three"]):
            score_7 = 1
        elif any(word in text.lower() for word in ["half", "2", "two"]):
            score_7 = 2
        elif any(word in text.lower() for word in ["every", "1", "one"]):
            score_7 = 3
        else:
            score_7 = "Sorry can you repeat it"
            app.logger.error('testing error log')
            print("error")
        if score_7 == "Sorry can you repeat it":
            pass
        else:
            total_score += score_7

        return jsonify({'status': 'success', 'text': text, 'score': score_7})

    except sr.UnknownValueError:
        return jsonify({'status': 'error', 'message': 'Speech Recognition could not understand audio'})


@app.route('/question8/start_audio_8', methods=['POST'])
def start_audio_8():
    global audio_playing
    if not audio_playing:
        audio_playing = True
        audio_thread = threading.Thread(target=play_audio, args=('Question 8.mp3',))
        audio_thread.start()

    return jsonify({'status': 'success'})


@app.route('/question8/stop_audio_8', methods=['POST'])
def stop_audio_8():
    global audio_playing, total_score, score_8
    audio_playing = False
    time.sleep(1)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

        if any(word in text.lower() for word in ["not", "4", "four"]):
            score_8 = 0
        elif any(word in text.lower() for word in ["several", "3", "three"]):
            score_8 = 1
        elif any(word in text.lower() for word in ["half", "2", "two"]):
            score_8 = 2
        elif any(word in text.lower() for word in ["every", "1", "one"]):
            score_8 = 3
        else:
            score_8 = "Sorry can you repeat it"
            app.logger.error('testing error log')
            print("error")
        if score_8 == "Sorry can you repeat it":
            pass
        else:
            total_score += score_8

        return jsonify({'status': 'success', 'text': text, 'score': score_8})

    except sr.UnknownValueError:
        return jsonify({'status': 'error', 'message': 'Speech Recognition could not understand audio'})


@app.route('/question9/start_audio_9', methods=['POST'])
def start_audio_9():
    global audio_playing
    if not audio_playing:
        audio_playing = True
        audio_thread = threading.Thread(target=play_audio, args=('Question 9.mp3',))
        audio_thread.start()

    return jsonify({'status': 'success'})


@app.route('/question9/stop_audio_9', methods=['POST'])
def stop_audio_9():
    global audio_playing, total_score, score_9
    audio_playing = False
    time.sleep(1)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)

        if any(word in text.lower() for word in ["not", "4", "four"]):
            score_9 = 0
        elif any(word in text.lower() for word in ["several", "3", "three"]):
            score_9 = 1
        elif any(word in text.lower() for word in ["half", "2", "two"]):
            score_9 = 2
        elif any(word in text.lower() for word in ["every", "1", "one"]):
            score_9 = 3
        else:
            score_9 = "Sorry can you repeat it"
            app.logger.error('testing error log')
            print("error")
        if score_9 == "Sorry can you repeat it":
            pass
        else:
            total_score += score_9

        return jsonify({'status': 'success', 'text': text, 'score': score_9})

    except sr.UnknownValueError:
        return jsonify({'status': 'error', 'message': 'Speech Recognition could not understand audio'})


@app.route('/question9/stop_recording', methods=['GET'])
def stop_recording():
    try:
        global recording_flag, stop_event
        recording_flag = False  # Set the flag to stop the recording loop
        stop_event.set()  # Set the stop event
        time.sleep(1)  # Wait for a short duration to ensure the recording thread stops
        return jsonify({'status': 'success', 'text': "Video successfully recorded"})
    except:
        return jsonify({'status': 'error', 'message': 'Error stopping Webcam wa not working'})


if __name__ == '__main__':
    app.run(debug=True)
