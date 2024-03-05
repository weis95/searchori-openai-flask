import requests
from deep_translator import GoogleTranslator
from analysis.sentiment import getSentimentNLTK

def translation_worker(news, lang):
    if len(news) == 0:
        return 'No news to translate'
    
    print(lang + ' :News to translate', len(news))
    for data in news:
        if data['title'] != 'error':
            data['title'] = GoogleTranslator(source=lang, target='en').translate(data['title'])

        if data['subheading'] != 'error':
            data['subheading'] = GoogleTranslator(source=lang, target='en').translate(data['subheading'])

        if len(data['story']) != 0:
            for i, story in enumerate(data['story']):
                if(data['story'][i] != 'error'):
                    data['story'][i] = GoogleTranslator(source=lang, target='en').translate(data['story'][i])
            
            if data['title'] != 'error' and data['story'][0] != 'error':
               
                story = ''.join(map(str, data['story']))
                story[:30]
               
                sentiment = getSentimentNLTK(data['title'] + story)
                data['sentiment'] = sentiment
        
        if len(data['comments']) != 0:
            for index, comment in enumerate(data['comments']):
                for i, idx in enumerate(data['comments'][index]):
                    data['comments'][index][i] = GoogleTranslator(source=lang, target='en').translate(data['comments'][index][i])
       
        data['translated'] = True
    
    print('Done translating: ', lang)
    resp = requests.patch('https://searchori.net/articles/update', json = news)
    print(resp.text)

