from flask import Flask, request
from resources import Entry, EntryManager

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p style='color:red'> Hello, World!</p>"


@app.route("/my_json/")
def get_json():
    return {'Hello': 'World'}



@app.route("/api/entries/")
def get_entries():
        em = EntryManager(FOLDER)
        em.load()
        entries = []
        for entry in em.entries:
            entries.append(entry.json())
        return entries

@app.route("/api/save_entries/", methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    data = request.get_json()
    for item in data:
        em = Entry.from_json(item)
        entry_manager.entries.append(em)
    entry_manager.save()
    return {'status': 'success'}

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

FOLDER = 'C:/'
#newdata

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
