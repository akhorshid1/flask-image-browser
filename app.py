import requests
import random
import os
import pandas as pd
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, show, output_notebook
from bokeh.embed import components

app = Flask(__name__)


################################## WOMEN #####################################
likes_women = ['woman']
image_sequence_women = []

files_women = os.listdir('data/women') # os.listdir does not sort files
files_women = sorted(files_women) 
del files_women[0]

######################### Setting up the .csv File ###########################
df_women = pd.read_csv('women.csv')
df_women = df_women[['File Name', 'Truncated Description', 'Certainty']]

# Return unique file name with a list of descriptions:
df1_women = df_women.groupby(['File Name'])['Truncated Description'].apply(list).reset_index() # reset_index() restores dataframe to conventional structure
df_certainty_women = df_women.groupby(['File Name'])['Certainty'].apply(list).reset_index()
df1_women = df1_women.join(df_certainty_women['Certainty'])   # adding the list of certainties
# Dropping duplicates from the list of descriptions of each image:
df1_women['Truncated Description'] = list(map(set, df1_women['Truncated Description']))
# Converting set (description) into list:
df1_women['Truncated Description'] = df1_women['Truncated Description'].apply(list)

################################### MEN ######################################
likes_men = ['man']
image_sequence_men = []

files_men = os.listdir('data/men') # os.listdir does not sort files
files_men = sorted(files_men) 
del files_men[0]

######################### Setting up the .csv File ###########################
df_men = pd.read_csv('men.csv')
df_men = df_men[['File Name', 'Truncated Description', 'Certainty']]

# Return unique file name with a list of descriptions:
df1_men = df_men.groupby(['File Name'])['Truncated Description'].apply(list).reset_index() # reset_index() restores dataframe to conventional structure
df_certainty_men = df_men.groupby(['File Name'])['Certainty'].apply(list).reset_index()
df1_men = df1_men.join(df_certainty_men['Certainty'])   # adding the list of certainties
# Dropping duplicates from the list of descriptions of each image:
df1_men['Truncated Description'] = list(map(set, df1_men['Truncated Description']))
# Converting set (description) into list:
df1_men['Truncated Description'] = df1_men['Truncated Description'].apply(list)
##############################################################################



def obtain_score(file_name, gender):
    if gender == 'women':         
        file_index = df1_women['File Name'][df1_women['File Name'] == file_name].index[0] # index value of the file
        file_values = df1_women['Truncated Description'][file_index]
        
    if gender == 'men':         
        file_index = df1_men['File Name'][df1_men['File Name'] == file_name].index[0] # index value of the file
        file_values = df1_men['Truncated Description'][file_index]
    
    return file_values

def choose_random(gender):
    if gender == 'women':
        # The most pythonic way to pop a random element from a list:
        image_name = files_women.pop(random.randrange(len(files_women)))
    if gender == 'men':
        # The most pythonic way to pop a random element from a list:
        image_name = files_men.pop(random.randrange(len(files_men)))   

    return image_name 

def save_image_sequence(image_file, gender):
    if gender == 'women':
        image_sequence_women.append(image_file)
    if gender == 'men':
        image_sequence_men.append(image_file)
    
def save_likes(image_sequence, gender):
    if gender == 'women':
        likes_women.append(image_sequence)
    if gender == 'men':
        likes_men.append(image_sequence)
        
    print(likes_women)
    print(likes_men)

def bokehplot(image_name, gender):
    
    if gender == 'women':
        im = Image.open('data/women/' + image_name)
    if gender == 'men':
        im = Image.open('data/men/' + image_name)
    
    im = im.convert("RGBA")
    imarray = np.array(im)
    imarray = imarray[::-1]
    title = str(obtain_score(image_name.rsplit( ".", 1 )[ 0 ], gender))   # Stripping .jpeg extension
    plot = figure(x_range=(0,1), y_range=(0,1), plot_width=400, plot_height=400, title=title)
    plot.image_rgba(image=[imarray], x=0, y=0, dw=1, dh=1)
    plot.title.text_font_size = '8pt'
    
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
    gender = ''
    if request.method == 'GET':
        return render_template('index.html', bokeh_script="", bokeh_div="", gender=gender)
    else:
        gender = request.form.get('gender','')
        
        # Pop a random element from a list:
        image_file = choose_random(gender)
        # save_image_sequence is used to recall the last 
        # image in the event that a user likes an image:
        save_image_sequence(image_file, gender)
        
        
        # Saving liked images:
        if request.form.get("liked_image"):
            if len(image_sequence_women)==1:
                pass
            if gender == 'women':
                save_likes(image_sequence_women[-2], gender)
            if len(image_sequence_men)==1:
                pass
            if gender == 'men':
                save_likes(image_sequence_men[-2], gender)               
            
        
        fig = bokehplot(image_file, gender)
        script, div = components(fig)
        return render_template(
            'index.html',
            bokeh_script=script,
            bokeh_div=div,
            gender=gender)

if __name__ == '__main__':
    app.run(port=33507)
