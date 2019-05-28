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


indoor  = set(['shower curtain', 'restaurant', 'window shade', 'shower curtain',
           'cellular telephone', 'barbershop', 'barbell', 'dumbbell',
           'television', 'prison', 'bath towel', 'remote control',
           'bannister', 'beer glass', 'medicine chest', 'library',
           'butternut squash', 'punching bag', 'bathtub', 'refrigerator',
           'wardrobe', 'bookshop', 'studio couch', 'monitor', 'bookcase',
           'theater curtain', 'washbasin', 'hand blower', 'shopping basket',
           'microwave', 'wine bottle', 'dishwasher', 'wooden spoon',
           'window screen', 'soap dispenser', 'beer bottle', 'television',
           'toilet seat', 'sliding door'])

outdoor = set(['mosque', 'picket fence', 'park bench', 'pier', 'sunscreen', 
           'seashore', 'cliff', 'seat belt', 'sunglass', 'sunglasses',
           'valley', 'alp', 'lakeside', 'promontory', 'coho',
           'cliff dwelling', 'bikini', 'valley', 'barracouta', 'gar',
           'mountain bike', 'sleeping bag', 'crash helmet', 'sturgeon',
           'sandbar', 'snorkel', 'motor scooter', 'snowmobile', 'racket',
           'umbrella', 'lumbermill', 'basketball', 'backpack', 'convertible',
           'street sign', 'fountain', 'palace', 'car wheel','volcano',
           'golfcart', 'rapeseed', 'suspension bridge', 'dome',
           'car mirror', 'limousine', 'palace'])

animals = set(['American Staffordshire terrier', 'papillon', 'Mexican hairless',
           'golden retriever', 'French bulldog', 'German shepherd', 
           'Italian greyhound', 'Arabian camel', 'Siberian husky',
           'Bernese mountain dog', 'Rhodesian ridgeback', 'Shetland sheepdog',
           'Tibetan mastiff', 'Old English sheepdog', 'Scottish deerhound',
           'Scottish deerhound', 'Afghan hound', 'English setter',
           'Irish terrier', 'Pomeranian', 'Norwegian elkhound', 'Irish setter',
           'English springer', 'Irish wolfhound', 'German short-haired pointer',
           'dalmatian', 'French bulldog', 'Labrador retriever', 'Doberman', 
           'Staffordshire bullterrier', 'Pekinese', 'Shih-Tzu', 'Rottweiler',
           'Saint Bernard', 'toy poodle', 'miniature poodle', 'Great Dane',
           'vizsla',
           'Persian cat', 'Egyptian cat' 
           ])

sports = set(['ballplayer', 'barbell', 'dumbbell', 'snorkel', 'ski', 
              'snowmobile', 'rugby ball', 'soccer ball', 'canoe', 'volleyball',
              'football helmet', 'ski mask', 'basketball'])

fashion = set(['swimming trunks', 'sweatshirt', 'jean', 'Windsor tie', 'pajama'
           'bikini', 'sombrero', 'cardigan', 'miniskirt', 'jersey', 'suit', 
           'mortarboard', 'shower cap', 'bikini', 'bonnet', 'stole', 'fur coat'
           'academic gown', 'brassiere', 'trench coat', 'sarong'])

misc = set(['cellular telephone', 'television', 'beer glass', 'beer bottle'])

sociability = set([])


indoor_individual = []
outdoor_individual = []
sociability_individual = []
fashion_individual = []
animals_individual = []
sports_individual = []


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

likes = 0
indoor_count = []
outdoor_count = []
animals_count = []
sports_count = []

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
        
    x = True
    y = True
    z = True
    k = True
        
    for i in range(0, len(objects)):

        
        if (objects[i] in indoor) == True:
            indoor_individual.append(objects[i])
            if x==True:
                indoor_count.append(1)
                x = False

                     
        if (objects[i] in animals) == True:
            animals_individual.append(objects[i])
            if y==True:
                animals_count.append(1)
                y = False
                
        if (objects[i] in outdoor) == True:
            outdoor_individual.append(objects[i])
            if z==True:
                outdoor_count.append(1)
                z = False
            
        if (objects[i] in sports) == True:
            sports_individual.append(objects[i])
            if k==True:
                sports_count.append(1)
                k = False
    
def bokehplot():
    
################################### MEN ######################################
        
    df1 = df_men.groupby(['Truncated Description']).size().reset_index()
    df1 = df1.sort_values([0], ascending = False).reset_index()
    
    df1.rename(columns={0:'count',
                        'Truncated Description':'truncated_description'},
                        inplace=True)   # Rename headers
    df1 = df1[0:50]
    
    
    description_array = df1['truncated_description'].tolist()

    
    p1 = figure(x_range=description_array,
               width=600, height=500, title="Men",
               tools="",background_fill_color='#440154')
    
    
    hover = HoverTool(tooltips = [
        ('Item', '@truncated_description'),
        ('Count', '@count')])
    
    
    p1.add_tools(hover)
    
    p1.grid.visible = False
    
    p1.vbar(top = 'count', x='truncated_description', width=0.8,
           source=df1, hover_color="pink", hover_alpha=0.8)
    
    p1.y_range.start = 0
    p1.title.align = 'center'
    p1.title.text_font_size = "1.25em"
    p1.xaxis.axis_label = "Classification"
    p1.yaxis.axis_label = "Count"
    p1.xaxis.major_label_orientation = 1
    p1.xgrid.grid_line_color = None
    
    p1.toolbar.logo = None
    p1.toolbar_location = None

################################## WOMEN #####################################
    
    df2 = df_women.groupby(['Truncated Description']).size().reset_index()
    df2 = df2.sort_values([0], ascending = False).reset_index()
    
    df2.rename(columns={0:'count',
                        'Truncated Description':'truncated_description'},
                        inplace=True)   # Rename headers
    df2 = df2[0:50]
    
    
    description_array = df2['truncated_description'].tolist()

    
    p2 = figure(x_range=description_array,
               width=600, height=500, title="Women",
               tools="",background_fill_color='#440154')
    
    
    hover = HoverTool(tooltips = [
        ('Item', '@truncated_description'),
        ('Count', '@count')])
    
    
    p2.add_tools(hover)
    
    p2.grid.visible = False
    
    p2.vbar(top = 'count', x='truncated_description', width=0.8,
           source=df2, hover_color="pink", hover_alpha=0.8)
    
    p2.y_range.start = 0
    p2.title.align = 'center'
    p2.title.text_font_size = "1.25em"
    p2.xaxis.axis_label = "Classification"
    p2.yaxis.axis_label = "Count"
    p2.xaxis.major_label_orientation = 1
    p2.xgrid.grid_line_color = None
    
    p2.toolbar.logo = None
    p2.toolbar_location = None
    
    layout = row(p1, p2)
    return layout

def bokehplot1(image_name, gender):
    
    if gender == 'women':
        im = Image.open('data/women/' + image_name)
    if gender == 'men':
        im = Image.open('data/men/' + image_name)
    
    im = im.convert("RGBA")
    imarray = np.array(im)
    imarray = imarray[::-1]
    title = str(obtain_score(image_name.rsplit( ".", 1 )[ 0 ], gender)[0:3])   
    # Stripping .jpeg extension
    p1 = figure(x_range=(0,1), y_range=(0,1), plot_width=400,
                  plot_height=400, title=title)
    p1.title.text_font_size = '12pt'
    p1.title.text_color = "#ffffff"
    p1.title.align = 'center'
    p1.image_rgba(image=[imarray], x=0, y=0, dw=1, dh=1)
    p1.background_fill_color = "#234567"
    p1.border_fill_color = "#234567"   #234567
#    plot.min_border = 80
   
    p1.toolbar.logo = None
    p1.toolbar_location = None
    p1.axis.visible = False
    
    A = len(indoor_count)
    B = len(outdoor_count)
    C = len(animals_count)
    D = len(sports_count)
    
    A_count = {x:indoor_individual.count(x) for x in indoor_individual}
    B_count = {x:outdoor_individual.count(x) for x in outdoor_individual}
    C_count = {x:animals_individual.count(x) for x in animals_individual}
    D_count = {x:sports_individual.count(x) for x in sports_individual}

    
    A_list = list(A_count.items())
    B_list = list(B_count.items())
    C_list = list(C_count.items())
    D_list = list(D_count.items())

    
    A_top = sorted(A_list, key=lambda x: x[1], reverse=True)[0:3]
    B_top = sorted(B_list, key=lambda x: x[1], reverse=True)[0:3]
    C_top = sorted(C_list, key=lambda x: x[1], reverse=True)[0:3]
    D_top = sorted(D_list, key=lambda x: x[1], reverse=True)[0:3]
    
    

    data = [['Indoor', A, A_top],['Outdoor', B, B_top],
            ['Pets', C, C_top],['Sports', D, D_top]]
    stats = pd.DataFrame(data, columns = ['categories', 'count', 'top']) 
    categories = ['Indoor', 'Outdoor', 'Pets', 'Sports']
    
    
    
    p2 = figure(x_range=categories, width=400, height=400, tools="",
                background_fill_color='#440154')
    
    hover = HoverTool(tooltips = [
        ('Item', '@categories'),
        ('Count', '@count'),
        ('Top', '@top')])
    
    p2.add_tools(hover)
    
    p2.grid.visible = False
    
    p2.vbar(top = 'count', x='categories', width=0.8,
            source = stats,
            hover_color="pink", hover_alpha=0.8)
    
    p2.y_range.start = 0
#    p2.xaxis.axis_label = "Classification"
    p2.yaxis.axis_label = "Count"    
    p2.xaxis.major_label_orientation = 1
    p2.xgrid.grid_line_color = None
    p2.background_fill_color = "#440154"
    p2.border_fill_color = "#234567"
    p2.title.text_color = "#ffffff"
    p2.title.text_font_size = "1.25em"
    p2.axis.major_label_text_color = "#ffffff"
    p2.axis.major_label_text_font_size = "1em"
    p2.axis.axis_line_color = "#ffffff"
    p2.axis.major_tick_line_color = "#ffffff"
    p2.axis.minor_tick_line_color = "#ffffff"
    p2.yaxis.axis_label_text_font_size = "1em"
    p2.yaxis.axis_label_text_font_style = "normal"
    p2.xaxis.axis_label_text_font_size = "1em"
    p2.xaxis.axis_label_text_font_style = "normal"
    p2.xaxis.axis_label_standoff = 12
    p2.yaxis.axis_label_standoff = 12
    p2.xaxis.axis_label_text_color = "#ffffff"
    p2.yaxis.axis_label_text_color = "#ffffff"
    
    p2.toolbar.logo = None
    p2.toolbar_location = None
    
    layout = row(p1, p2)

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

@app.route('/about')
def about():
    fig = bokehplot()
    script, div = components(fig)
    return render_template('about.html',
                           bokeh_script=script,
                           bokeh_div=div)

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
         
        fig = bokehplot1(image_file, gender)
        script, div = components(fig)
            
        return render_template(
            'index.html',
            bokeh_script=script,
            bokeh_div=div,
            gender=gender)
        


if __name__ == '__main__':
    app.run(port=33507)
