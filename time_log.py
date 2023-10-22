from flask import Flask, render_template, jsonify
import time
from collections import Counter
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time
    return wrapper

@timer
def count_words_dict(filename):
    with open(filename, 'r') as file:
        text = file.read().split()
        word_count = {}
        for word in text:
            word = word.lower()
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    return word_count

@timer
def count_words_counter(filename):
    with open(filename, 'r') as file:
        text = file.read().split()
        return Counter(text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_experiment')
def run_experiment():
    dict_times = []
    counter_times = []

    for _ in range(100):
        _, time_taken = count_words_dict('t8.shakespeare.txt')
        dict_times.append(time_taken)

        _, time_taken = count_words_counter('t8.shakespeare.txt')
        counter_times.append(time_taken)

    fig, ax = plt.subplots()
    ax.hist(dict_times, alpha=0.5, label='Dictionary Method')
    ax.hist(counter_times, alpha=0.5, label='CounterMethod')
    ax.legend(loc='upper right')
    ax.set_title('Distribution of Execution Times')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Frequency')

    # Sauvegarder l'image dans un flux de données en mémoire
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_b64 = base64.b64encode(buf.read()).decode('utf-8')

    # Retourner l'image encodée en base64 pour l'affichage dans le navigateur
    return jsonify({'image_b64': image_b64})

@app.route('/question/<int:q_number>')
def question(q_number):
    if q_number == 4:
        word_count_dict, time_taken_dict = count_words_dict('t8.shakespeare.txt')
        word_count_counter, time_taken_counter = count_words_counter('t8.shakespeare.txt')

        # Renvoyer le temps d'exécution et un échantillon des comptages pour des raisons de lisibilité
        return jsonify({
            'time_taken_dict': time_taken_dict,
            'time_taken_counter': time_taken_counter,
            'sample_dict': dict(list(word_count_dict.items())[:10]),
            'sample_counter': dict(list(word_count_counter.items())[:10])
        })

    # Ici, vous pouvez ajouter d'autres conditions pour les autres questions si nécessaire

    return jsonify({'message': 'Question not implemented'})

if __name__ == "__main__":
    app.run(debug=True)
