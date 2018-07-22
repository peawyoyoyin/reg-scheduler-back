from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)

app.add_url_rule('/api', view_func=GraphQLView.as_view('graphql', schema=schema.schema, graphiql=True))

@app.route('/')
def hello():
    return 'you might want to go to /api instead'

if __name__ == '__main__':
    app.run()
