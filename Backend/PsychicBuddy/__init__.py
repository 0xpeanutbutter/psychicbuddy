from .utils.summarization import Tokenizer , Summarizer , sModel , iModel
from .utils.summarization import getCategory

from .utils.files import audioToText , videoToText , splitPassage

from .utils.yolo import Yolo_v3

from flask import Flask

UPLOAD_FOLDER = './Media'

app = Flask("PsychicBuddy")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER