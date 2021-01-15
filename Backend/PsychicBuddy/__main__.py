from . import Tokenizer , Summarizer , sModel , iModel , getCategory

from . import audioToText , videoToText , splitPassage

from . import app

from flask import jsonify
from flask import request

@app.route("/text")
def textClassification() :
    data = request.json

    try :
        text = data['text']

        return jsonify(
            {
                'summary' : Summarizer(text)[0]['summary_text'] , 
                'category' : getCategory(text)
            }
        )
    except :
        return jsonify({})

@app.route('/video') 
def videoClassification() :
    file_ = request.file['file']

    filepath = './'+app.config['UPLOAD_FOLDER']+'/'+file_.filename
    file_.save(filepath)
    text = audioToText(filepath)

    parts = splitPassage(text)
    
    results = []

    for part in parts :
        results.append({
                'summary' : Summarizer(part)[0]['summary_text'] , 
                'category' : getCategory(part)
            })    
    return jsonify({
        'Results' : results
    })

@app.route('/audio')
def audioClassification() :
    file_ = request.file['file']

    filepath = './'+app.config['UPLOAD_FOLDER']+'/'+file_.filename
    file_.save(filepath)
    text = videoToText(filepath)

    parts = splitPassage(text)
    
    results = []

    for part in parts :
        results.append({
                'summary' : Summarizer(part)[0]['summary_text'] , 
                'category' : getCategory(part)
            })    
    return jsonify({
        'Results' : results
    })

if __name__ == '__main__' : 
    app.run(debug=True)