import datetime
import random
import locale
from flask import request


def format_url(uri):
    """returns the full url"""
    return f'{request.root_url}{uri}'


def adjust_market_value(ask_price):
    """
    Increase player's market value by a random factor in range (10, 100)
    :param ask_price: current ask_price
    :return: updated ask_price
    """
    percent_increase = random.randint(10, 100)
    increment = (percent_increase / 100) * ask_price
    return ask_price + increment


def currency_formatter(num):
    """
    Format currency as USD
    :param num: int
    :return: $ amount
    """
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(num, grouping=True)


def player_age_generator():
    """Generate random age in range (18, 40)"""
    return random.randint(18, 40)


def format_error(e):
    """
    Format API error response
    :param e: exception object
    :return: JSON
    """
    if "password" in e.payload:
        del e.payload["password"]
    data = {
        "success": False,
        "timestamp": datetime.datetime.utcnow(),
        "request_uri": request.url,
        "request_payload": e.payload,
        "error": {
            "name": e.name,
            "response code": e.status_code,
            "description": e.message,
        }
    }
    return data, e.status_code


def format_generic_error(e):
    """
    Format API error response
    :param e: exception object
    :return: JSON
    """
    data = {
        "success": False,
        "timestamp": datetime.datetime.utcnow(),
        "request_uri": request.url,
        "error": {
            "description": str(e),
            "name": e.__class__.__name__
        }
    }
    return data, 500


def format_response(data, code):
    """
    Format success response
    :param data: json result
    :param code: response code
    :return: JSON
    """
    data = {
        "success": True,
        "timestamp": datetime.datetime.utcnow(),
        "request_uri": request.url,
        "data": data,
        "status_code": code,
    }

    return data
