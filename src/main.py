from run import create_app
from service.methods import CRUD
from flask import request, jsonify
import json

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@127.0.0.1/postgres"


@app.route("/create", methods=['POST'])
def insert_data():
    object_ = CRUD()
    data = json.loads(request.data)
    object_.create(data)
    return jsonify({'status': 'ok'})


@app.route("/find_by_id/<id>")
def find_by_id(id: str):
    object_ = CRUD()
    result = object_.read_by_id(int(id))
    return json.dumps(result, ensure_ascii=False)


@app.route("/find")
def find_by_url():
    object_ = CRUD()
    url = request.args.get('url')
    password = request.args.get('password')
    if password == object_.get_password().get('password'):
        result = object_.read_by_url(str(url))
        return json.dumps(result, ensure_ascii=False)
    else:
        e = Exception
        print(e)


@app.route("/guide/<id>")
def delete_by_id(id: str):
    object_ = CRUD()
    result = object_.delete(int(id))
    return json.dumps({"status": 'ok'}, ensure_ascii=False)


@app.route("/update_by", methods=['PUT'])
def update_by_id():
    object_ = CRUD()
    data = json.loads(request.data)
    id = data.get('id')
    ob = data.get('obj')
    print(ob)
    result = object_.update(dict(ob))
    return json.dumps(result)


@app.route("/")
def hello_world():
    return json.dumps({"status": "alive"})


if __name__ == "__main__":
    app.run(debug=True)
