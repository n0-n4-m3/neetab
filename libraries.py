from pymongo import MongoClient
from bson.objectid import ObjectId

from flask import Flask, render_template, request, redirect, session
from jinja2 import Template, Environment, FileSystemLoader

from functions import *

import sys
import bcrypt

"""Операции с приложением Flask"""
app = Flask(__name__)
app.secret_key = "test"

"""Подключение ДБ"""
client = MongoClient("localhost", 27017)
db = client.Cat_and_fish