from flask import Flask, redirect
from app import create_app
import logging

app = create_app()

# Setup basic logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    app.logger.debug("Redirecting to /main")
    return redirect('/main')

if __name__ == '__main__':
    app.run(debug=True)
