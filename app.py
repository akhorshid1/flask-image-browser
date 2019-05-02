import requests
import random
import os
import pandas as pd
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, show, output_notebook
from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.layouts import row, column

app = Flask(__name__)


indoor  = ['shower curtain', 'restaurant', 'window shade', 'shower curtain',
           'cellular telephone', 'barbershop', 'barbell', 'dumbbell',
           'television', 'prison', 'coho', 'bath towel', 'remote control',
           'bannister', 'beer glass', 'medicine chest', 'library',
           'butternut squash', 'punching bag', 'bathtub', 'refrigerator',
           'wardrobe', 'bookshop', 'studio couch', 'monitor']

outdoor = ['mosque', 'picket fence', 'park bench', 'pier', 'sunscreen', 
           'seashore', 'cliff', 'seat belt', 'sunglass', 'sunglasses',
           'seashore', 'valley', 'alp', 'lakeside', 'promontory', 
           'cliff dwelling', 'bikini', 'valley', 'barracouta', 'gar',
           'mountain bike', 'sleeping bag', 'crash helmet', 'sturgeon',
           'sandbar', 'snorkel', 'motor scooter', 'ski', 'snowmobile', 'racket',
           'umbrella', 'lumbermill', 'basketball', 'backpack', 'convertible',
           'street sign', 'fountain', 'palace', 'car wheel','volcano']

animals = ['American Staffordshire terrier', 'papillon', 'Mexican hairless',
           'golden retriever', 'French bulldog', 'German shepherd', 
           'Italian greyhound', 'Arabian camel', 'Siberian husky',
           'Bernese mountain dog', 'Rhodesian ridgeback', 'Shetland sheepdog',
           'Tibetan mastiff', 'Old English sheepdog', 'Scottish deerhound',
           'Scottish deerhound', 'Afghan hound', 'English setter',
           'Irish terrier', 'Pomeranian', 'Norwegian elkhound', 'Irish setter',
           'English springer', 'Irish wolfhound', 'German short-haired pointer',
           'dalmatian', 'French bulldog', 'Labrador retriever', 
           'Staffordshire bullterrier',
           'Persian cat', 'Egyptian cat', 
           'chimpanzee', 'tench', 'gar', 'African grey']

sociability = []

sports = ['ballplayer', 'barbell', 'dumbbell', 'snorkel', 'ski', 'snowmobile' ]

fashion = ['swimming trunks', 'sweatshirt', 'jean', 'Windsor tie', 'pajama'
           'bikini', 'sombrero', 'cardigan', 'miniskirt', 'jersey', 'suit', 
           'mortarboard', 'shower cap', 'bikini', 'bonnet', 'stole', 'fur coat'
           'academic gown', 'brassiere', 'trench coat']

misc = ['cellular telephone', 'television', 'beer glass', 'beer bottle']

indoor_individual = []
outdoor_individual = []
sociability_individual = []
fashion_individual = []
animals_individual = []

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


##############################################################################



def obtain_score(file_name, gender):
    index_value = []
    objects = []
    score_image = 0
    if gender == 'women':         
        file_index = df1_women['File Name'][df1_women['File Name'] == file_name].index[0] # index value of the file
        file_values = df1_women['Truncated Description'][file_index]
        score = df1_women['Certainty'][file_index]
        for i in range(0, len(file_values)):
            if score[i] > 0.2:
                index_value.append(i)
                objects.append(file_values[i])
                score_image = score_image + score[i]
        
    if gender == 'men':         
        file_index = df1_men['File Name'][df1_men['File Name'] == file_name].index[0] # index value of the file
        file_values = df1_men['Truncated Description'][file_index]
        score = df1_men['Certainty'][file_index]
        for i in range(0, len(file_values)):
            if score[i] > 0.2:
                index_value.append(i)
                objects.append(file_values[i])
                score_image = score_image + score[i]
                
    objects = list(set(objects))
    
    return objects

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
#        df1_men = [df1_men[df1_men['File Name']!= image_name.rsplit( ".", 1 )[ 0 ] ] ]
        
    
def save_likes(image_sequence, gender, objects):
    if gender == 'women':
        likes_women.append(image_sequence)
    if gender == 'men':
        likes_men.append(image_sequence)
        
    for i in range(0, len(objects)):
        
        if (objects[i] in indoor) == True:
            indoor_individual.append(objects[i])
        if (objects[i] in animals) == True:
            animals_individual.append(objects[i])
        if (objects[i] in outdoor) == True:
            outdoor_individual.append(objects[i])
        if (objects[i] in fashion) == True:
            fashion_individual.append(objects[i])
                    
    print(indoor_individual)
    print(outdoor_individual)
    print(animals_individual)
#    print(likes_women)
#    print(likes_men)

def bokehplot(image_name, gender):
    
    if gender == 'women':
        im = Image.open('data/women/' + image_name)
    if gender == 'men':
        im = Image.open('data/men/' + image_name)
    
    im = im.convert("RGBA")
    imarray = np.array(im)
    imarray = imarray[::-1]
    title = str(obtain_score(image_name.rsplit( ".", 1 )[ 0 ], gender))   
    # Stripping .jpeg extension
    plot = figure(x_range=(0,1), y_range=(0,1), plot_width=400,
                  plot_height=400, title=title)
    plot.title.text_font_size = '12pt'
    plot.title.text_color = "#ffffff"
    plot.title.align = 'center'
    plot.image_rgba(image=[imarray], x=0, y=0, dw=1, dh=1)
    plot.background_fill_color = "#234567"
    plot.border_fill_color = "#234567"
#    plot.min_border = 80
   
    plot.toolbar.logo = None
    plot.toolbar_location = None
    plot.axis.visible = False
    

#    df = pd.read_csv('men.csv')
#    df1 = df.groupby(['Truncated Description']).size().reset_index()
#    df1 = df1.sort_values([0], ascending = False).reset_index()
#    df1.rename(columns={0:'count', 'Truncated Description':'truncated_description'}, inplace=True)   # Rename headers
#    df1 = df1[0:50]
    
    
    
    
#    description_array = df1['truncated_description'].tolist()
#    p = figure(x_range=description_array, width=600, height=500, title="Top 50 Classifications", tools="",background_fill_color='#440154')
#    
#    hover = HoverTool(tooltips = [
#        ('Item', '@truncated_description'),
#        ('Count', '@count')])
#    
#    
#    p.add_tools(hover)
#    
#    p.grid.visible = False
#    
#    p.vbar(top = 'count', x='truncated_description', width=0.8, source=df1, hover_color="pink", hover_alpha=0.8)
#    
#    p.y_range.start = 0
#    p.xaxis.axis_label = "Classification"
#    p.yaxis.axis_label = "Count"
#    p.xaxis.major_label_orientation = 1
#    p.xgrid.grid_line_color = None
#    
#    p.toolbar.logo = None
#    p.toolbar_location = None
    
    categories = ['Indoor', 'Outdoor', 'Pets']
    
    A = len(outdoor_individual)
    B = len(indoor_individual)
    
    count = [A,B,3]
    
    
    p = figure(x_range=categories, width=400, height=400, title="Statistics", tools="",background_fill_color='#440154')
    
    p.grid.visible = False
    
    p.vbar(top = count, x=categories, width=0.8, hover_color="pink", hover_alpha=0.8)
    
    p.y_range.start = 0
    p.xaxis.axis_label = "Classification"
    p.yaxis.axis_label = "Count"    
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.background_fill_color = "#440154"
    p.border_fill_color = "#234567"
    p.title.text_color = "#ffffff"
    p.title.text_font_size = "1.25em"
    p.axis.major_label_text_color = "#ffffff"
    p.axis.major_label_text_font_size = "0.75em"
    p.axis.axis_line_color = "#ffffff"
    p.axis.major_tick_line_color = "#ffffff"
    p.axis.minor_tick_line_color = "#ffffff"
    p.yaxis.axis_label_text_font_size = "1em"
    p.yaxis.axis_label_text_font_style = "normal"
    p.xaxis.axis_label_text_font_size = "1em"
    p.xaxis.axis_label_text_font_style = "normal"
    p.xaxis.axis_label_standoff = 12
    p.yaxis.axis_label_standoff = 12
    p.xaxis.axis_label_text_color = "#ffffff"
    p.yaxis.axis_label_text_color = "#ffffff"
    
    p.toolbar.logo = None
    p.toolbar_location = None
    
    layout = column(plot, p)

    return layout

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
                objects = obtain_score(image_sequence_women[-2].rsplit( ".", 1 )[ 0 ], gender)
                save_likes(image_sequence_women[-2], gender, objects)
                
            if len(image_sequence_men)==1:
                pass
            if gender == 'men':
                objects = obtain_score(image_sequence_men[-2].rsplit( ".", 1 )[ 0 ], gender)
                save_likes(image_sequence_men[-2], gender, objects)
            
        
        fig = bokehplot(image_file, gender)
        script, div = components(fig)
        return render_template(
            'index.html',
            bokeh_script=script,
            bokeh_div=div,
            gender=gender)

if __name__ == '__main__':
    app.run(port=33507)
