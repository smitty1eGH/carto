from flask import Flask,escape,request,render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def asdf(name=None):
    name = request.args.get("name", "World")
    return render_template('app.html')


@app.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

if __name__=='__main__':
    app.run()
