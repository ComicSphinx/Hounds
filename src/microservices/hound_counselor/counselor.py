# @Author: Daniil Maslov (ComicSphinx)

from flask import Flask, jsonify
from flask_restful import Api, Resource
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
api = Api(app)

class counselor(Resource):
    @app.route("/")
    def stock_analysis():
        print("Stock analysis requested")
        
        resume = ""
        
        tiker = ""
        
        # trend
        trend_start = ""
        trend_end = ""
        
        # price
        price_for_one = 0
        price_for_lot = 0
        lot_size = 0

        # fundamental analysis
        price_start_of_period = 0
        price_end_of_period = 0
        price_different_between_periods = 0
        trend = ""
        p_e = 0
        mrq = 0
        listing_level = 0
        dividends = 0
        # net profit
        price_at_the_beginnig_of_period = 0
        price_at_the_end_of_period = 0
        profit_resume = ""

        # TECHNICAL ANALYSIS
        # month forecast
        moving_average = 0
        technical_indicators = 0
        month_forecast = ""
        # consensus forecast
        to_buy = 0
        neutral = 0
        to_sell = 0
        consensus_forecast = ""
        # ANALYTICS
        # maximum
        maximum_analytics_goal_price = 0
        analytics_income = 0
        # minimum
        minimum_analytics_goal_price = 0
        analytics_loss = 0
        # price_place_on_chart
        price_place_on_chart = 0