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
           'television', 'prison', 'coho', 'bath towel', 'remote control',
           'bannister', 'beer glass', 'medicine chest', 'library',
           'butternut squash', 'punching bag', 'bathtub', 'refrigerator',
           'wardrobe', 'bookshop', 'studio couch', 'monitor', 'bookcase',
           'theater curtain', 'washbasin', 'hand blower', 'shopping basket',
           'microwave', 'wine bottle', 'dishwasher', 'wooden spoon',
           'window screen'])

outdoor = set(['mosque', 'picket fence', 'park bench', 'pier', 'sunscreen', 
           'seashore', 'cliff', 'seat belt', 'sunglass', 'sunglasses',
           'seashore', 'valley', 'alp', 'lakeside', 'promontory', 
           'cliff dwelling', 'bikini', 'valley', 'barracouta', 'gar',
           'mountain bike', 'sleeping bag', 'crash helmet', 'sturgeon',
           'sandbar', 'snorkel', 'motor scooter', 'ski', 'snowmobile', 'racket',
           'umbrella', 'lumbermill', 'basketball', 'backpack', 'convertible',
           'street sign', 'fountain', 'palace', 'car wheel','volcano',
           'golfcart', 'rapeseed', 'suspension bridge', 'dome'])

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
           'Saint Bernard',
           'Persian cat', 'Egyptian cat', 
           'chimpanzee', 'tench', 'gar', 'African grey'])

sociability = []

sports = ['ballplayer', 'barbell', 'dumbbell', 'snorkel', 'ski', 'snowmobile' ]

fashion = ['swimming trunks', 'sweatshirt', 'jean', 'Windsor tie', 'pajama'
           'bikini', 'sombrero', 'cardigan', 'miniskirt', 'jersey', 'suit', 
           'mortarboard', 'shower cap', 'bikini', 'bonnet', 'stole', 'fur coat'
           'academic gown', 'brassiere', 'trench coat', 'sarong']

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

likes = 0

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
    
                    
#    print(indoor_individual)
#    print(outdoor_individual)
#    print(animals_individual)
#    print(likes_women)
#    print(likes_men)

def bokehplot(image_name, gender):
    
    if gender == 'women':
        im = Image.open('data/women/' + image_name)
        dataframe = df1_women
    if gender == 'men':
        im = Image.open('data/men/' + image_name)
        dataframe = df1_men
    
    score = []

    # Dropping duplicates from the list of descriptions of each image:
    dataframe['Truncated Description'] = list(map(set,dataframe['Truncated Description']))
    # Converting set (description) into list:
    dataframe['Truncated Description'] = dataframe['Truncated Description'].apply(list)
    
    
    file_index = dataframe['File Name'][dataframe['File Name'] == image_name.rsplit( ".", 1 )[ 0 ]].index[0] # index value of the file
    file_values = dataframe['Truncated Description'][file_index]
    

    
    for i in range(0, len(dataframe['File Name'])):
        score.append(0) # initial score = 0 (i.e. no matches)
        
        if (dataframe['File Name'][i] == image_name.rsplit( ".", 1 )[ 0 ]):
            pass 
        else:
            
            for j in range(0, len(dataframe['Truncated Description'][i])):

                for k in range(0, len(file_values)):
                    
                    if (file_values[k] == dataframe['Truncated Description'][i][j]):
#                            score[i] = score[i] + 1
                        score[i] = score[i] + dataframe['Certainty'][i][j] + 1
                    else:
                        pass
    
    header_score ='Score (' + str(image_name)+ ')'
    df_score = pd.DataFrame({header_score: score})
    dataframe = dataframe.join(df_score)
    dataframe = dataframe.sort_values(by=[header_score], ascending = False).reset_index()
    
    # Reordering columns (using double [[]]):
    dataframe = dataframe[['index', 'File Name', 'Truncated Description', header_score, 'Certainty']]
    
    print(dataframe.head())
    
    im1 = im.convert("RGBA")
#    imarray = np.array( Image.open('data/men/' + dataframe['File Name'][0] + '.jpg') )
    imarray1 = np.array( im1 )
    imarray1 = imarray1[::-1]
    title = 'sample image'  
    # Stripping .jpeg extension
    p1 = figure(x_range=(0,1), y_range=(0,1), plot_width=400,
                  plot_height=400, title=title)
    p1.title.text_font_size = '12pt'
    p1.title.text_color = "#000000"
    p1.title.align = 'center'
    p1.image_rgba(image=[imarray1], x=0, y=0, dw=1, dh=1)
    p1.background_fill_color = "#D3D3D3"
    p1.border_fill_color = "#D3D3D3"
#    plot.min_border = 80
   
    p1.toolbar.logo = None
    p1.toolbar_location = None
    p1.axis.visible = False
    
    im2 = Image.open('data/men/' + dataframe['File Name'][1] + '.jpg')
    im2 = im2.convert("RGBA")
    imarray2 = np.array( im2 )
    imarray2 = imarray2[::-1]
    title = 'suggested image'  
    # Stripping .jpeg extension
    p2 = figure(x_range=(0,1), y_range=(0,1), plot_width=400,
                  plot_height=400, title=title)
    p2.title.text_font_size = '12pt'
    p2.title.text_color = "#000000"
    p2.title.align = 'center'
    p2.image_rgba(image=[imarray2], x=0, y=0, dw=1, dh=1)
    p2.background_fill_color = "#D3D3D3"
    p2.border_fill_color = "#D3D3D3"
#    plot.min_border = 80
   
    p2.toolbar.logo = None
    p2.toolbar_location = None
    p2.axis.visible = False
    
    im3 = Image.open('data/men/' + dataframe['File Name'][2] + '.jpg')
    im3 = im3.convert("RGBA")
    imarray3 = np.array( im3 )
    imarray3 = imarray3[::-1]
    title = 'suggested image'  
    # Stripping .jpeg extension
    p3 = figure(x_range=(0,1), y_range=(0,1), plot_width=400,
                  plot_height=400, title=title)
    p3.title.text_font_size = '12pt'
    p3.title.text_color = "#000000"
    p3.title.align = 'center'
    p3.image_rgba(image=[imarray3], x=0, y=0, dw=1, dh=1)
    p3.background_fill_color = "#D3D3D3"
    p3.border_fill_color = "#D3D3D3"
#    plot.min_border = 80
   
    p3.toolbar.logo = None
    p3.toolbar_location = None
    p3.axis.visible = False
    
    im4 = Image.open('data/men/' + dataframe['File Name'][3] + '.jpg')
    im4 = im4.convert("RGBA")
    imarray4 = np.array( im4 )
    imarray4 = imarray4[::-1]
    title = 'suggested image'  
    # Stripping .jpeg extension
    p4 = figure(x_range=(0,1), y_range=(0,1), plot_width=400,
                  plot_height=400, title=title)
    p4.title.text_font_size = '12pt'
    p4.title.text_color = "#000000"
    p4.title.align = 'center'
    p4.image_rgba(image=[imarray4], x=0, y=0, dw=1, dh=1)
    p4.background_fill_color = "#D3D3D3"
    p4.border_fill_color = "#D3D3D3"
#    plot.min_border = 80
   
    p4.toolbar.logo = None
    p4.toolbar_location = None
    p4.axis.visible = False
    
    layout = column(p1, p2, p3, p4)
    return layout

def bokehplot1(image_name, gender):
    
    if gender == 'women':
        im = Image.open('data/women/' + image_name)
    if gender == 'men':
        im = Image.open('data/men/' + image_name)
    
    im = im.convert("RGBA")
    imarray = np.array(im)
    imarray = imarray[::-1]
    title = str(obtain_score(image_name.rsplit( ".", 1 )[ 0 ], gender))   
    # Stripping .jpeg extension
    p1 = figure(x_range=(0,1), y_range=(0,1), plot_width=400,
                  plot_height=400, title=title)
    p1.title.text_font_size = '12pt'
    p1.title.text_color = "#000000"
    p1.title.align = 'center'
    p1.image_rgba(image=[imarray], x=0, y=0, dw=1, dh=1)
    p1.background_fill_color = "#D3D3D3"
    p1.border_fill_color = "#D3D3D3"   #234567
#    plot.min_border = 80
   
    p1.toolbar.logo = None
    p1.toolbar_location = None
    p1.axis.visible = False
    
    A = len(indoor_individual)
    B = len(outdoor_individual)
    C = len(animals_individual)
    D = len(fashion_individual)
    
    A_count = {x:indoor_individual.count(x) for x in indoor_individual}
    B_count = {x:outdoor_individual.count(x) for x in outdoor_individual}
    C_count = {x:animals_individual.count(x) for x in animals_individual}
    D_count = {x:fashion_individual.count(x) for x in fashion_individual}

    
    A_list = list(A_count.items())
    B_list = list(B_count.items())
    C_list = list(C_count.items())
    D_list = list(D_count.items())

    
    A_top = sorted(A_list, key=lambda x: x[1], reverse=True)[0:3]
    B_top = sorted(B_list, key=lambda x: x[1], reverse=True)[0:3]
    C_top = sorted(C_list, key=lambda x: x[1], reverse=True)[0:3]
    D_top = sorted(D_list, key=lambda x: x[1], reverse=True)[0:3]
    
    

    data = [['Indoor', A, A_top],['Outdoor', B, B_top],
            ['Pets', C, C_top],['Fashion', D, D_top]]
    stats = pd.DataFrame(data, columns = ['categories', 'count', 'top']) 
    categories = ['Indoor', 'Outdoor', 'Pets', 'Fashion']
    
    
    
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
#    p2.yaxis.axis_label = "Count"    
    p2.xaxis.major_label_orientation = 1
    p2.xgrid.grid_line_color = None
    p2.background_fill_color = "#ffffff"
    p2.border_fill_color = "#D3D3D3"
    p2.title.text_color = "#000000"
    p2.title.text_font_size = "1.25em"
    p2.axis.major_label_text_color = "#000000"
    p2.axis.major_label_text_font_size = "0.75em"
    p2.axis.axis_line_color = "#000000"
    p2.axis.major_tick_line_color = "#000000"
    p2.axis.minor_tick_line_color = "#000000"
    p2.yaxis.axis_label_text_font_size = "1em"
    p2.yaxis.axis_label_text_font_style = "normal"
    p2.xaxis.axis_label_text_font_size = "1em"
    p2.xaxis.axis_label_text_font_style = "normal"
    p2.xaxis.axis_label_standoff = 12
    p2.yaxis.axis_label_standoff = 12
    p2.xaxis.axis_label_text_color = "#000000"
    p2.yaxis.axis_label_text_color = "#000000"
    
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

#@app.route('/about')
#def about():
#    return redirect('/index')

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
            
        if request.form.get("suggestions"):
            fig = bokehplot(image_sequence_men[-2], gender)
            script, div = components(fig)
          
        else: 
            fig = bokehplot1(image_file, gender)
            script, div = components(fig)
            
        return render_template(
            'index.html',
            bokeh_script=script,
            bokeh_div=div,
            gender=gender)
        


if __name__ == '__main__':
    app.run(port=33507)
