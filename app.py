from flask import Flask ,render_template, url_for, request
import joblib
import pandas as pd
from pymongo import MongoClient

modelpath=  "./models/kmeans_model.lb"
modelpath2 = "./models/std_scaler.lb"
df = pd.read_csv("./models/filter_crops.csv")


scaler = joblib.load(modelpath2)
kmeans =  joblib.load(modelpath)

app = Flask(__name__)

connectionstring = "mongodb+srv://aayushjohari0403:FnNFgW9QjZ69IHgt@farmerdb.nczd5.mongodb.net/?retryWrites=true&w=majority&ssl=true&appName=FARMERDB"
# mongodb+srv://aayushjohari0403:<db_password>@farmerdb.nczd5.mongodb.net/?retryWrites=true&w=majority&appName=FARMERDB
client = MongoClient(connectionstring)
database = client['farmer']
collection = database['Farmerdata']



@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/features')
def features():
    return render_template('features.html') # http://127.0.0.1:5000/features


@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/predict',methods = ['GET','POST'])
def predict():
    if request.method =='POST':
        n = int(request.form['nitrogen'])
        p = int(request.form['phosphorus'])
        k = int(request.form['potassium'])
        t = float(request.form['temperature'])
        h = float(request.form['humidity'])
        ph = float(request.form['ph'])
        r = float(request.form['rainfall'])
        user_data = [[n , p , k , t, h, ph , r ]]

        trans_data = scaler.transform(user_data)
        cluster = kmeans.predict(trans_data)[0]
        suggestion_crop =list(df[df["cluster_no"]==cluster]['label'].unique())
        data = {"N":n , "P":p ,"K":k ,"tempersture":t , "humidity":h, "ph":ph , "rainfall": r}
        data_id= collection.insert_one(data).inserted_id
        print('Your data is inserted into the mongodib your record id is:',data_id)

        return f"suggested crops:  {suggestion_crop}"
        

        return user_data




if __name__ =="__main__":
    app.run(debug = True)
