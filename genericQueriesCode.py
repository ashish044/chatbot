# coding: utf-8 
import os,pandas as pd,numpy as np,cPickle as pickle,operator
from sklearn.feature_extraction.text import TfidfVectorizer
import textprocessor

'''-----------------------READ GENERIC QUESTIONS-------------------------'''  
##read generic questions
def read_questions_generic(filePath_Property,sheetname):
    if not os.path.exists('generic_questions'+sheetname+'.pickle'):
        filePath = filePath_Property + "MFGS.xlsx"
        dataFrame = pd.read_excel(filePath, sheetname=sheetname,names=['sr.no','question','answer'])
        dataFrame = dataFrame.replace(np.nan, ' ')
        for i in dataFrame.columns.values:
            dataFrame[i] = dataFrame[i]
        
        with open('generic_questions_'+sheetname+'.pickle','wb')as qof:
            pickle.dump(dataFrame,qof)
        qof.close()     
    else: 
        with open('generic_questions_'+sheetname+'.pickle','rb')as qof:
            dataFrame = pickle.load(qof)
        qof.close()
    return dataFrame
    
    
#df_generic = read_questions_generic(filePath_Property)  



'''-----------------------PREPARE GENERIC TRAINING DATA-------------------------'''    

def train_data_generic(filePath_Property, sheetname,processed_query="" ):
    ##similar training as in the product catalogue queries except the training is done on generic questions
    processed_query = textprocessor.text_processing(processed_query)
    dataFrame = read_questions_generic(filePath_Property,sheetname)
    
    id_dataset = dataFrame['question']
    answer_data = dataFrame['answer']
    final_output = []
    values_output = []
    row_number=0
    multiple_match = []
    flag = ""
    flagCount = 0
    
    if sheetname != '_questions':
        if os.path.exists('flagcount.pickle'):
            flagCount = pickle.load(open('flagcount.pickle','rb'))
        else:
            flagCount = 0 ##starting the pickles!
            pickle.dump(flagCount, open('flagcount.pickle', "wb"))
        print "BEFOREFLAG:",flagCount
    
    questions_list = process_questions_generic(filePath_Property,sheetname)##processing the questions- stem and cleaning
    
    tf = TfidfVectorizer(min_df=0, ngram_range=(1, 1), strip_accents='unicode', norm='l2')
    
    tfidf_matrix =  tf.fit_transform(np.array([''.join(el) for el in questions_list]))  
   
    #print "processed query",processed_query
    X_query = tf.transform([processed_query])
    XX_similarity = np.dot(tfidf_matrix.todense(), X_query.transpose().todense())
    XX_sim_scores = np.array(XX_similarity).flatten().tolist()
    #print "scores tuple:",(X_query,XX_sim_scores,XX_similarity)
    dict_sim = dict(enumerate(XX_sim_scores))
    #print "dictsim:",dict_sim
    
    temp ={k:v for (k,v) in dict_sim.items() if v > 0.6}
    
    if len(temp) > 1 :
        flag = "multiple"
        conf_match={k:v for (k,v) in temp.items() if v >= 0.95}
        if len(conf_match) == 1:
            print "button flag"
            flag = "btn_input"
         
        
        
        #return stageName,confScore,row_number,flag
    sorted_dict_sim = sorted(dict_sim.items(), key = operator.itemgetter(1), reverse=True)
    #print "sorted dict:",sorted_dict_sim
    row_number = sorted_dict_sim[0]
    
    values_output = []
    print sorted_dict_sim[0][1]
    if sorted_dict_sim[0][1] == 0:
        flag = "out_of_list"
        print("not a generic query!!") 
        jsondata_values = [1, 1, "Sorry, I didn’t get that. I am new and still learning.", round(0, 2)]  
        values_output.append(jsondata_values)
    else:
        n = 0
        #value_check = []
        for el in sorted_dict_sim:
            n = n + 1
            if el[1] > 0 and n < len(sorted_dict_sim):# or (el[1] > 0.1 and n == len(sorted_dict_sim) ) :
                jsondata_values = [n, id_dataset[el[0]], (answer_data[el[0]]), round(el[1], 2)]
                if flag =="multiple":
                    if jsondata_values[3]>0.60:
                        multiple_match.append(jsondata_values[1])
                if flag == "btn_input":
                    print "score :",(jsondata_values[3])
                    if jsondata_values[3] > 0.95:
                        multiple_match.append(jsondata_values[2])
                    
                #value_check.append(jsondata_values)
                #print jsondata_values
                #print len(sorted_dict_sim)
                values_output.append(jsondata_values)
                       
        
                
    if flag == "multiple":
        final_output = multiple_match
        flagCount += 1 
    elif flag == "btn_input":
        final_output = multiple_match
        flagCount += 1 
    else :
        final_output = values_output[0][2]
    if '?' in final_output:
        final_output = final_output.replace('?','')
    
    if sheetname != '_questions':
        pickle.dump(flagCount, open('flagcount.pickle', "wb"))
    
    #print final_output,values_output[0][3],row_number
    if sheetname != '_questions':
        if (flagCount == 2 and (flag == "multiple" or flag == "btn_input")):
            final_output = values_output[0][2]
            flagCount = 0
            flag = ""
            pickle.dump(flagCount, open('flagcount.pickle', "wb"))
        print "AFTERFLAG:",flagCount
    
    return final_output,values_output[0][3],row_number,flag


'''-----------------------PROCESSING THE GENERIC QUESTIONS-------------------------'''     
    
def process_questions_generic(filePath_Property,sheetname):
    if not os.path.exists('processed_questions_generic_'+sheetname+'.pickle'):
        if os.path.exists('generic_questions_'+sheetname+'.pickle'):
            with open('generic_questions_'+sheetname+'.pickle','rb')as qof:
                dataFrame = pickle.load(qof)
            qof.close()
        else:
            dataFrame = read_questions_generic(filePath_Property)
        
        questions_list = list(dataFrame['question'])
        if len(questions_list) > 0:
            for i in range(len(questions_list)):
                new_list = []
                old_list=[]
                for j in questions_list[i].split():
                    if j.startswith('$'):
                        new_list.append(j)
                    elif not j.startswith('$'):
                        old_list.append(j)
                old_list = ' '.join(old_list)
                new_list = ' '.join(new_list)
                questions_list[i] = textprocessor.text_processing(old_list)
                questions_list[i] = questions_list[i].split()
                questions_list[i].append(new_list)
                questions_list[i] = ' '.join(questions_list[i])
        else:
            raise ValueError    
        with open('processed_questions_generic_'+sheetname+'.pickle','wb')as qof:
            pickle.dump(questions_list,qof)
        qof.close() 
    else:        
        with open('processed_questions_generic_'+sheetname+'.pickle','rb')as qof:
            questions_list = pickle.load(qof)
        qof.close()
        
    return questions_list

#     
  
