
from flask import Flask , request , json, render_template
from flask_cors import CORS
import os
os.chdir("/mnt/c/Users/ashis/Documents/Python Scripts/")
import shelve_pfizer as sh
import genericQueriesCode as gqc
from autocorrect import spell
app = Flask(__name__)
CORS(app)
@app.route("/")
def home():    
    return render_template("hello.html") 

#@app.route('/msg' , methods=['POST'] )
@app.route('/msg', methods=['GET','POST'] )
def getBotResponse():
    filepath = "/mnt/c/Users/ashis/Documents/Python Scripts/"
    
    query = request.form['msg']
    print query
    
    #input_query = request.get_json()
    #query = input_query.get('query')

    #fQuery = input_query.get('firstQuery')
    #fQuery = input_query.get('secondQuery')
    #if str(fQuery) == "True":
    #    sh.shelve_reset()
    
    if query.upper() == 'RESETBOT':
        sh.shelve_reset() 
        print "Shelve Cleared!!"
        returnString1 = {}
        returnString1['message'] = ["Chat Restarted!!!"]
        response = app.response_class(
                response = json.dumps(returnString1),
                status = 200,
                mimetype = 'application/json'
                )
        return response
    
    tempList = []
    query = query.lower()
    if "bugfix" in query:
        query = query.replace("bugfix","bug fix")
    if ("auxilary") in query:
        query = query.replace("auxilary","auxiliary")
    if ("auxillary") in query:
        query = query.replace("auxillary","auxiliary")
    if "data base" in query:
        query = query.replace("data base","database")
    if "database" in query:
        query = query + " DB"
    if "backend" in query:
        query = query.replace("backend","back end")	
    check_list = ["pdoc","btqa","buqa","citrix"]
    for i in (check_list):
        if i in query.split():
            tempList.append(i)
            query = query.replace(i,'')
            
    query = str(' '.join(map(spell,query.split())))
    query = query +' ' +' '.join(tempList)
    
    print "spellcorrect:",query
    generic_result,confidence_Score,row_number,flag = gqc.train_data_generic(filepath  ,'_questions', query)
    generic_json = {}
    generic_json['message'] = [generic_result]
    print generic_result
    if confidence_Score > 0.9:
        result = generic_json
        response = app.response_class(
              response = json.dumps(result),
              status = 200,
              mimetype = 'application/json'
              )
        return response
    result_dict = {}
    result_dict['message'] = "Sorry I Am Not able to understand you..."
    #result_dict['Row number in Excel'] = row_number
    response = app.response_class(
        response=json.dumps(result_dict),
        status=200,
        mimetype='application/json'
    )
    return response

#port = port no , here we have 5004 port no, we can change it as per our port availability.   
if __name__ == "__main__":
        app.run(host ='0.0.0.0')
