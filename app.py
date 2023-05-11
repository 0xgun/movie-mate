from flask import Flask,render_template,request,session, url_for, redirect

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pymysql
from werkzeug.utils import secure_filename

import os
import pathlib
       

def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="movies", charset='latin1')
    return connection

def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")
        

con = dbConnection()
cursor = con.cursor()

app=Flask(__name__)

global unames
unames=""


UPLOAD_FOLDER = 'static/uploaded_files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','wav','mp3'}
app.secret_key = 'any random string'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main')
def main():
    con = dbConnection()
    cursor = con.cursor()
    print("---------------------------")
    cursor.execute("SELECT * FROM moviesdata")
    result = cursor.fetchall()
    print(result)
    
    return render_template("main.html",result=result)


@app.route('/home')
def home():
    return render_template('home.html')


from transformers import AutoTokenizer
def map_to_input(sen:str, seq_len:int):
    tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')
    tokens = tokenizer.encode_plus(sen, max_length=seq_len, 
                               truncation=True, padding="max_length",
                               add_special_tokens=True, return_token_type_ids=False,
                               return_attention_mask=True, return_tensors="tf"
                              )
    
    return tokens


from tensorflow.keras.models import load_model
import numpy as np
import string
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def clean_text(text):
    
    ## Remove puncuation
    text = text.translate(string.punctuation)
    
    ## Convert words to lower case and split them
    text = text.lower().split()
    
    ## Remove stop words
    stops = set(stopwords.words("english"))
    text = [w for w in text if not w in stops and len(w) >= 3]
    
    text = " ".join(text)
    ## Clean the text
    text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r",", " ", text)
    text = re.sub(r"\.", " ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\/", " ", text)
    text = re.sub(r"\^", " ^ ", text)
    text = re.sub(r"\+", " + ", text)
    text = re.sub(r"\-", " - ", text)
    text = re.sub(r"\=", " = ", text)
    text = re.sub(r"'", " ", text)
    text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r" e g ", " eg ", text)
    text = re.sub(r" b g ", " bg ", text)
    text = re.sub(r" u s ", " american ", text)
    text = re.sub(r"\0s", "0", text)
    text = re.sub(r" 9 11 ", "911", text)
    text = re.sub(r"e - mail", "email", text)
    text = re.sub(r"j k", "jk", text)
    text = re.sub(r"\s{2,}", " ", text)
    ## Stemming
    text = text.split()
    stemmer = SnowballStemmer('english')
    stemmed_words = [stemmer.stem(word) for word in text]
    text = " ".join(stemmed_words)
    return text

print("[Info] Model Loading....")
testmodel = load_model("NN_movie_sentiment.hp5")
print("[Info] Model loaded!!1!")


@app.route('/prediction',methods=['POST','GET'])
def prediction():
    global unames
    if request.method == "POST":
        global unames
        details = request.form.get
        usrcomment = details('usrcoment')
        usrmoviename = details('moviename')
        usrname = unames

        print(usrcomment,usrmoviename)

        op = "prdicted_result"


        classes = {
            0: "Negative",
            1: "Somewhat Negative",
            2: "Neutral",
            3: "Somewhat Positive",
            4: "Positive"
        }

        X_test = [clean_text(usrcomment)]
        vocab_size = 20000
        tokenizer = Tokenizer(num_words = vocab_size)
        tokenizer.fit_on_texts(X_test)
        sequences = tokenizer.texts_to_sequences(X_test)
        X_test = pad_sequences(sequences, maxlen=50)

        Y_test = testmodel.predict(X_test)
        Y_test = [np.argmax(val) for val in Y_test]

        print("Y_test")
        print(Y_test)
        print()

        sentiscore = ""
        if Y_test[0]==0:
            sentiscore += "1"
        if Y_test[0]==1:
            sentiscore += "2"
        if Y_test[0]==2:
            sentiscore += "3"
        if Y_test[0]==3:
            sentiscore += "4"
        if Y_test[0]==4:
            sentiscore += "5"

        con = dbConnection()
        cursor = con.cursor()
        sql = 'INSERT INTO review_table (unames, moviename, reviewdata, sentimentop) values(%s,%s,%s,%s)'
        val = (usrname, usrmoviename, usrcomment,sentiscore)
        cursor.execute(sql,val)
        con.commit()

        return redirect(url_for("main")) 
    return redirect(url_for("main")) 


def SessionHandle1():
    if request.method == "POST":
        details = request.form
        name = details['name']
        session['name'] = name
        strofuser = name
        print (strofuser.encode('utf8', 'ignore'))
        return strofuser    


@app.route('/register')
def register():
    return render_template('register.html') 

@app.route('/userregistration',methods=['POST','GET'])
def userregistration():
    if request.method == "POST":
        details = request.form
        username = details['username']
        email = details['email']
        mobno = details['mobno']
        address = details['address']
        password = details['password']
        
        uploaded_file =request.files['filename']
        filename_secure = secure_filename(uploaded_file.filename)
        print(filename_secure)
        pathlib.Path(app.config['UPLOAD_FOLDER'], username).mkdir(exist_ok=True)
        print("print saved")
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], username, filename_secure))
        filename1 =os.path.join(app.config['UPLOAD_FOLDER'], username+"/", filename_secure)
     
        sql2  = "INSERT INTO register(username,email,mobileno,address,password,filepath) VALUES (%s, %s, %s, %s, %s ,%s)"
        val2 = (str(username), str(email), str(mobno), str(address), str(password), str(filename1))
        cursor.execute(sql2,val2) 
        con.commit()
        
    return render_template('login.html') 


@app.route('/login', methods=["GET","POST"])
def login():
    msg = ''
    global unames
    if request.method == "POST":
            global unames
            username = request.form.get("username")
            password = request.form.get("password")
            
            con = dbConnection()
            cursor = con.cursor()
            cursor.execute('SELECT * FROM register WHERE username = %s AND password = %s', (username, password))
            result = cursor.fetchone()
            print ("result",result)
            if result:
                session['name'] = result[1]
                unames += username
                return redirect(url_for("main")) 
            else:
                msg = 'Incorrect username/password!'
                return msg
    return render_template('login.html')

@app.route('/logout')
def logout():
    global unames
    session.pop('name',None)
    unames = ""
    return render_template('index.html') 

@app.route('/movie/<id>')
def movie(id):
    print(id)
    con = dbConnection()
    cursor = con.cursor()
    cursor.execute('SELECT * FROM moviesdata WHERE id = %s',(id))
    result = cursor.fetchone()
    
    results = list(result)
    print(results)
    
    sql = "SELECT * from review_table where moviename=%s"
    val = (results[3])
    cursor.execute(sql,val)
    res = cursor.fetchall()
    result2 = list(res)

    unames = [i[1] for i in result2]
    moviename = [i[2] for i in result2]
    reviewdata = [i[3] for i in result2]
    sentimentop = [i[4] for i in result2]

    flst = zip(unames,reviewdata,sentimentop)


    return render_template('movie-details.html',result=result,flst=flst)

@app.route('/analysis.html')
def analysis():
   return render_template('analysis.html')
@app.route('/modification.html')
def Modification():
    return render_template('modification.html')

if __name__=="__main__":
    app.run("0.0.0.0")
    # app.run(debug=True)