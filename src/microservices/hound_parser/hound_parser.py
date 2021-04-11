# @Author: Daniil Maslov (ComicSphinx)

from flask import Flask, jsonify
from flask_restful import Api, Resource
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
api = Api(app)

class parser(Resource):

    @app.route("/get/<portfolio_id>",methods=['GET'])
    def get(portfolio_id):
        link = "link/" + portfolio_id
        page = requests.get(link)
        data = bs(page.text, 'html.parser')
        
        cost = data.find('span', class_= 'dashboard-currency dashboard-card-big-nums rub')
        income = data.find('div', class_= 'flex dashboard-item xl3 lg3 md6 sm6 xs12 align-content-start')
        income = income.find('span', class_= 'dashboard-currency dashboard-card-big-nums rub')
        
        cost = cost.text
        income = income.text
        data = {'cost': cost, 'income': income}
        return jsonify(data), 200

api.add_resource(parser, "/get/")
if __name__ == '__main__':
    app.run(debug=True)