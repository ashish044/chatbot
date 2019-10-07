 # coding: utf-8 

'''-----------------------PROCESSING TEXT DATA-------------------------'''
def text_processing(text=""):
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    ps = PorterStemmer()  
    text = text.lower()
    #list123=[]
    stopword_token = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word not in stopwords.words('english')]
    text = ' '.join(stopword_token)
    stemmed_token = [ps.stem(word) for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    text = ' '.join(stemmed_token)
    #logger.info('returning processed query as list')
    return text
'''-----------------------PROCESSING TEXT DATA BY ONLY TOKENISING-------------------------'''
def just_tokenise(text=""):
    import nltk
    from nltk.corpus import stopwords
    #from nltk.stem.porter import PorterStemmer
    #ps = PorterStemmer()  
    text = text.lower()
    #list123=[]
    stopword_token = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word not in stopwords.words('english')]
    text = ' '.join(stopword_token)
    return text
'''-----------------------PROCESSING TEXT DATA BY ONLY STEMMING-------------------------'''
def just_stem(text=""):
    import nltk
    #from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    ps = PorterStemmer()  
    text = text.lower()
    stemmed_token = [ps.stem(word) for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    text = ' '.join(stemmed_token)
    #logger.info('returning processed query as list')
    return text
