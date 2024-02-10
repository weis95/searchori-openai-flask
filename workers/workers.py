import requests
from deep_translator import GoogleTranslator
from analysis.sentiment import getSentimentNLTK

def translation_worker(news, lang):
    for data in news:
        data['title'] = GoogleTranslator(source=lang, target='en').translate(data['title'])
        data['subheading'] = GoogleTranslator(source=lang, target='en').translate(data['subheading'])
        if data['story'][0] != 'error':
            for i, story in enumerate(data['story']):
                data['story'][i] = GoogleTranslator(source=lang, target='en').translate(data['story'][i])
            
            sentiment = getSentimentNLTK(data['title'] + ' '.join(data['story'][0]))
            data['sentiment'] = sentiment
        
        if len(data['comments']) > 0:
            for index, comment in enumerate(data['comments']):
                for i, idx in enumerate(data['comments'][index]):
                    data['comments'][index][i] = GoogleTranslator(source=lang, target='en').translate(data['comments'][index][i])
    
    requests.post('http://localhost:8000/articles', json = {'data': news})
