import json
import os
import random
import nltk
from nltk.tokenize import word_tokenize
import pyttsx3
import webbrowser

response = "https://www.youtube.com"
if response.startswith("http"):
    webbrowser.open(response)
else:
    print(response)