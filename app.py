from flask import Flask, render_template

#keep this below imports else will Throw Error
app = Flask(__name__)

#keep this after app = Flask(__name__) else will Throw Error
import config

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)