from flask import Flask, render_template, request, redirect, session,jsonify
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from sqlalchemy import text
import pickle
import pandas as pd
import os
from ChatBot_Response import chatbot_response
from keras.utils import load_img,img_to_array
from keras.models import load_model
from keras.preprocessing import image
import warnings
import sqlite3