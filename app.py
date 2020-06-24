""" Shows how to use flask and matplotlib together.
Shows SVG, and png.
The SVG is easier to style with CSS, and hook JS events to in browser.
python3 -m venv venv
. ./venv/bin/activate
pip install flask matplotlib
python flask_matplotlib.py
"""
import io
import random
from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg


import base64
from io import BytesIO
from flask import Flask,render_template,url_for,request,redirect
from flask import Flask, session

from matplotlib.figure import Figure
import sys
sys.path.append(".")
from classes import Wikipedia

app = application = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


wiki = Wikipedia('https://en.wikipedia.org/wiki/Abba')


@app.route("/", methods=['GET', 'POST'])
def home():
    """ Returns html with the img tag for your plot.
    """
    styles = ['seaborn-ticks', 'ggplot', 'dark_background', 'bmh', 'seaborn-poster', 'seaborn-notebook',
             'fast', 'seaborn', 'classic', 'Solarize_Light2', 'seaborn-dark', 'seaborn-pastel', 'seaborn-muted',
             '_classic_test', 'seaborn-paper', 'seaborn-colorblind', 'seaborn-bright', 'seaborn-talk',
             'seaborn-dark-palette','tableau-colorblind10', 'seaborn-darkgrid', 'seaborn-whitegrid',
              'fivethirtyeight', 'grayscale', 'seaborn-white', 'seaborn-deep']
    
    cmaps=  [ 'viridis', 'plasma', 'inferno', 'magma', 'cividis',
              'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
             'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper', 'flag', 'prism', 'ocean',
             'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar',
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
             'twilight', 'twilight_shifted', 'hsv','Pastel1', 'Pastel2', 'Paired', 'Accent',
             'Dark2', 'Set1', 'Set2', 'Set3','tab10', 'tab20', 'tab20b', 'tab20c']
    
   
    if request.method == 'POST':
        session['get_url'] = request.form['my_url']
        session['get_style'] = request.form['styles']
        session['get_cmap'] = request.form['cmaps']
        
        # title
        if request.form.get('my_title') == '':
            session['get_title'] = "Default"
        else:
            session['get_title'] = request.form['my_title']
        
        # Color
        if request.form.get('my_color') == '':
            session['get_color'] = "#0000ff"
        else: 
            session['get_color'] = request.form.get('my_color')
        
        # Freqeuncy
        if request.form.get('my_freq') == '':
            session['get_freq'] = 5
        else:  
            session['get_freq'] = request.form.get('my_freq', type=int)
        
      
    return render_template('home.html', my_url   = session.get("get_url"),
                                        my_style = session.get("get_style"),
                                        my_cmap  = session.get("get_cmap"),
                                        my_title = session.get("get_title"),
                                        my_freq  = session.get("get_freq"),
                                        my_color = session.get("get_color"),
                                        styles   = styles,
                                        cmaps    = cmaps
                           )

   
   
@app.route("/wordcloud.png")
def wordcloud():
    
    if session.get('get_url') == None:
        wiki = Wikipedia('https://en.wikipedia.org/wiki/Abba')
        return wiki.wordcloud(cmap='viridis')
    else:
        wiki = Wikipedia(session.get("get_url"))
        return wiki.wordcloud(cmap=session.get("get_cmap"))
    
    
@app.route("/lineplot.png")
def lineplot():
    if session.get('get_url') == None:
        wiki = Wikipedia('https://en.wikipedia.org/wiki/Abba')
        return wiki.lineplot(style='seaborn', title="Default", freq=20, color="#0000ff")
    else:
        wiki = Wikipedia(session.get("get_url"))
        return wiki.lineplot(style=session.get("get_style"),
                              title=session.get("get_title"),
                              freq=session.get("get_freq"),
                              color=session.get("get_color")
                              )
        

@app.route("/barplot.png")
def barplot():
    if session.get('get_url') == None:
        wiki = Wikipedia('https://en.wikipedia.org/wiki/Abba')
        return wiki.barplot(style='seaborn')
    else:
        wiki = Wikipedia(session.get("get_url"))
        return wiki.barplot(style=session.get("get_style"),
                              title=session.get("get_title"),
                              freq=session.get("get_freq"),
                              color=session.get("get_color")
                              )

@app.route("/barplot_h.png")
def barplot_h():
    if session.get('get_url') == None:
        wiki = Wikipedia('https://en.wikipedia.org/wiki/Abba')
        return wiki.barplot_h(style='seaborn')
    else:
        wiki = Wikipedia(session.get("get_url"))
        return wiki.barplot_h(style=session.get("get_style"),
                              title=session.get("get_title"),
                              freq=session.get("get_freq"),
                              color=session.get("get_color")
                              )

@app.route("/pieplot.png")
def pieplot():
    if session.get('get_url') == None:
        wiki = Wikipedia('https://en.wikipedia.org/wiki/Abba')
        return wiki.pieplot(style='seaborn')
    else:
        wiki = Wikipedia(session.get("get_url"))
        return wiki.pieplot(style=session.get("get_style"),
                              title=session.get("get_title"),
                              freq=session.get("get_freq")                 
                              )

@app.route("/boxplot.png")
def boxplot():
    if session.get('get_url') == None:
        wiki = Wikipedia('https://en.wikipedia.org/wiki/Abba')
        return wiki.boxplot(freq=5)
    else:
        wiki = Wikipedia(session.get("get_url"))
        return wiki.boxplot(freq=session.get("get_freq"),
                            title=session.get("get_title"),                  
                            color=session.get("get_color")
                          )


if __name__ == "__main__":
    app.run(port =5000, debug=True)