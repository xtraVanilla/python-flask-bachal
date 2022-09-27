from flask import Flask
from blueprints import librarian, user

app = Flask(__name__)
app.register_blueprint(librarian, url_prefix="/api/librian")
app.register_blueprint(user, urserl_prefix="/api/user")

if __name__ == "__main__":
    app.run(debug=True)
