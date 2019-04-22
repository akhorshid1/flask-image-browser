import requests
import random
import os
import pandas as pd
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect, abort
from datetime import date
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Range1d, HoverTool, CrosshairTool
from bokeh.embed import components

app = Flask(__name__)

files = os.listdir('data/') # os.listdir does not sort files
files = sorted(files) 
del files[0]

likes = ['first image']
image_sequence = []

def choose_random():
    X = random.randint(0, len(files))
    image_name = files[X]
    return image_name 

def save_image_sequence(image_file):
    image_sequence.append(image_file)
    
def save_likes(image_sequence):
    likes.append(image_sequence)

def bokehplot(image_name):
    
    im = Image.open('data/' + image_name)
    im = im.convert("RGBA")
    imarray = np.array(im)
    imarray = imarray[::-1]
    plot = figure(x_range=(0,1), y_range=(0,1), plot_width=400, plot_height=400, title=likes[-1])
    plot.image_rgba(image=[imarray], x=0, y=0, dw=1, dh=1)
    
    return plot



def invalid():
    error = None
    with open("static/error.html") as err:
        error = err.read()
    return render_template(
        'index.html',
        bokeh_script="",
        bokeh_div=error)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', bokeh_script="", bokeh_div="")
    else:
#        image = request.form.get('image_text')
        image_file = choose_random()
        save_image_sequence(image_file)
        
        if request.form.get("liked_image"):
            save_likes(image_sequence[-2])
        
        fig = bokehplot(image_file)
        script, div = components(fig)
        return render_template(
            'index.html',
            bokeh_script=script,
            bokeh_div=div)

if __name__ == '__main__':
    app.run(port=33507)
