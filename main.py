from flask import Flask
import logging

app = Flask(__name__)

@app.route("/")
def hello_world():
 prefix_google = """
 <!-- Google tag (gtag.js) -->
<script async 
src="https://www.googletagmanager.com/gtag/js?id=G-RW8X8N6FVS"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', ' G-RW8X8N6FVS');
</script>
 """
 return prefix_google + "Hello World 🚀"

logging.basicConfig(level=logging.DEBUG)

@app.route('/logger')
def logger():
    app.logger.info("Ceci est un log côté serveur (backend)!")
    return "<script>console.log('Ceci est un log côté client (frontend)!');</script>"

@app.route('/textbox', methods=['GET', 'POST'])
def textbox():
    message = ""
    if request.method == 'POST':
        message = request.form.get('message')
        app.logger.info(f"Message from textbox: {message}")

    return '''
        <form method="post">
            <input type="text" name="message">
            <input type="submit" value="Log Message">
        </form>
        '''


def root():
    return "Hello from Space! 🚀"

if __name__ == "__main__":
    # Changement du port d'écoute
    app.run(host='0.0.0.0', port=8080)