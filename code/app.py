from flask import Flask, render_template

#keep this below imports else will Throw Error
app = Flask(__name__)

#keep this after app = Flask(__name__) else will Throw Error
import controllers.config

import models

#imports like config and route are helping us to replace the code
#Improves the code readability and makes it easy to modify
import controllers.routes


if __name__ == '__main__':
    app.run(debug=True)

