from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/ping')
def ping_host():
    # 1. Source: Snyk tracks this as untrusted user input from the web
    user_input = request.args.get('ip')
    
    # 2. Sink: This runs the untrusted input directly in your operating system shell
    os.system("ping -c 1 " + user_input)
    
    return "Ping executed"

if __name__ == '__main__':
    app.run()
