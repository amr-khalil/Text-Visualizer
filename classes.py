# import  necessary libraries
import base64
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from wordcloud import WordCloud, ImageColorGenerator
from bidi.algorithm import get_display
import arabic_reshaper
from flask import Flask, Response, request
import io

class Wikipedia:
    
    def __init__(self, url):
        
        self.url = url
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.text, 'html.parser')

        # Get all paragraphs
        paragraphs = self.soup.find_all('p')
        self.article_text = ""
        for para in paragraphs:
            self.article_text += para.text
            
        # Get the title
        self.articletitle = self.soup.find('title').get_text()
        self.articletitle = get_display(arabic_reshaper.reshape(self.articletitle)) # For arabic font
            
    def wordCounter(self):
        # split() to slice the string and len() to count the items of the list
        wordcount = len(self.article_text.split(" "))
        return str(wordcount)+" Words"
    
   
    
    def links(self):
        links = self.soup.find_all('a')
        
        self.linksText = []
        # extract the links
        for link in links: 
            if str(link.get('href')).startswith("http"):
                self.linksText.append(link.get('href'))
                
        return "\n".join(self.linksText)
    
    
    def process_text(self):
        
        with open('data/stops_en.txt', 'r', encoding="utf-8") as myfile:
            stopwords_en = myfile.read().split("\n")
        
        with open('data/stops_de.txt', 'r', encoding="utf-8") as myfile:
            stopwords_de = myfile.read().split("\n")
        
        with open('data/stops_ar.txt', 'r', encoding="utf-8") as myfile:
            stopwords_ar = myfile.read().split("\n")
        
        # remove \n \t
        text = self.article_text.replace("\n", " ").replace("\t", " ")

        # lowercase words
        text = text.lower()

        # split the text to a list of words
        wordlist = text.split(" ")

        # remove stopwords
        stops = [word for word in wordlist if (word not in stopwords_en) and (word not in stopwords_de)and (word not in stopwords_ar)]

        # to remove the punctuation we will loop on every charachter and check it with isalnum()
        # isalnum() retrun Alphabetic charachters and numbers
        puncts = "".join([char for char in " ".join(stops) if char.isalnum() or char == " "]).strip()

        # remove words less than 4 charachters
        tokenized = [word for word in puncts.split() if len(word) > 3]
        processed = " ".join(tokenized)
        
        data = get_display(arabic_reshaper.reshape(processed)) # For arabic font
        
        return data
    
    
    def BagOfWords(self, freq=10):

        tokenized = self.process_text().split()
        
        # create a dictionary with key = word and value = frequency of a word 
        dic = {} 
        for word in tokenized:
            if word in dic:
                dic[word] += 1
            else:
                dic[word] = 1

        sorted_dic = {}

        for key, value in sorted(dic.items(), key=lambda x:x[1], reverse=True):
            sorted_dic.update({key:value})

        counter = {word:sorted_dic[word] for word in sorted_dic.keys() if sorted_dic[word] >= freq }
        return counter

    
    def wordcloud(self, cmap='viridis'):
       
        text = self.process_text()
        
        # Create and generate a word cloud image:
        wordcloud = WordCloud(font_path='static/fonts/arial.ttf',
                              width = 800, height = 800,
                              background_color="white",
                              colormap= cmap, include_numbers=True).generate(text)
          
        fig, ax = plt.subplots()
        fig.set_size_inches(10.5, 10.5)
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        ax.set_title("Word Cloud - "+self.articletitle, fontsize= 15)
        
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")
        
    def boxplot(self,freq=1, style='seaborn', color= '#333399',
                     title='Horizontal Bar Chart - Word Frequency'):
       
        bow = self.BagOfWords(freq)
        word,count = zip(*bow.items())  
        plt.style.use(style)
        
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)
        plt.subplots_adjust(bottom=0.3)
        ax.set_ylabel('Words Count')
        ax.set_title(title)
        #labels = ax.get_xticklabels()
        #plt.setp(labels, rotation=90, horizontalalignment='right')

        box = ax.boxplot(count, patch_artist=True, vert=False,widths = 0.6)
        colors = [color]
        for p, c in zip(box['boxes'], colors):
            p.set_facecolor(c)
        
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")
        
        
    def lineplot(self,freq=1, style='seaborn', color= '#333399',
                     title='Horizontal Bar Chart - Word Frequency'):
       
        bow = self.BagOfWords(freq)
        word,count = zip(*bow.items())  
        plt.style.use(style)
        
        fig, ax = plt.subplots()
        fig.set_size_inches(15, 7.5)
        plt.subplots_adjust(bottom=0.3)
        ax.set_ylabel('Words Count')
        ax.set_title(title)
        fig.suptitle('This is the figure title', fontsize=10)
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=90, horizontalalignment='right')
        word = [w.capitalize() for w in word]
        ax.plot(word, count, color=color)
        #ax.hist(count, color=color, bins = 300, density=True)
  
        
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")
        


    def barplot(self, freq=20, style='seaborn', color= '#333399',
                 title='Horizontal Bar Chart - Word Frequency'):
       
        bow = self.BagOfWords(freq)
        word,count = zip(*bow.items())
        plt.style.use(style)
        
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)

        plt.subplots_adjust(bottom=0.3)
        ax.set_ylabel('Words Count')
        ax.set_title(title)
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=90, horizontalalignment='right')
        ax.bar(word, count, align='center', color=color)
        
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")
        
    def barplot_h(self, freq=20, style='seaborn', color= '#333399',
                 title='Horizontal Bar Chart - Word Frequency'):
       
        bow = self.BagOfWords(freq)
        word,count = zip(*bow.items())
        plt.style.use(style)
        
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)

        plt.subplots_adjust(bottom=0.3)
        ax.set_xlabel('Words Count')
        ax.set_title(title)
        labels = ax.get_yticklabels()
        ax.barh(word, count, align='center', color=color)
        ax.invert_yaxis()  # labels read top-to-bottom
        
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")
        
    def pieplot(self,freq=20, style='seaborn',
                     title='Pie Chart - Word Frequency'):
        
        bow = self.BagOfWords(freq)
        word,count = zip(*bow.items())
        plt.style.use(style)
        
        explode = np.zeros(len(word))
        explode[0:3] = [0.1,0.05,0.025]

        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)
        ax.pie(count, labels=word, radius=1, autopct='%1.1f%%',
                textprops={'fontsize': 12},
                 startangle=90, shadow=True, explode=explode)
        ax.set_title(title)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.        
        plt.subplots_adjust(left=0.2, bottom=0.2)
        #ax.legend()
        
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")
        
    def table(self, freq=10, title="Table"):

        bow = self.BagOfWords(freq)
        
        data = np.array(list(bow.items()))
        fig, ax =plt.subplots()
        
        collabel=("Word", "Frequency - Word Frequency")
        #ax.axis('tight')
        ax.axis('off')
        ax.table(cellText=data,colLabels=collabel, loc='center', cellLoc='left') #,loc='center',cellLoc='left',  colWidths = [2, 1]
        ax.set_title(title)
        
        
        output = io.BytesIO()
        FigureCanvasAgg(fig).print_png(output)
        return Response(output.getvalue(), mimetype="image/png")

        
