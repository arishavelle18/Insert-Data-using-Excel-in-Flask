from unicodedata import name
from flask import Flask,render_template,request
import pandas as pd 
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_DB"] = 'data'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'
mysql = MySQL(app)
@app.get("/")
def index():
    return render_template("index.html")

@app.post("/data")
def data(): 
    file = request.form['upload-file']
    data = pd.read_excel(file).to_dict()
    cur = mysql.connection.cursor()

    for i in data["name "].keys():
        res = cur.execute("SELECT * FROM user WHERE name = %s ",[data["name "][i]])
        if res == 0:
            cur.execute("INSERT INTO user(name,age) VALUES(%s,%s)",(data["name "][i],data["age "][i]))
            mysql.connection.commit()
    
   
    # close the fucking connection
    cur.close()


    return render_template("data.html",data = data)


if __name__ == "__main__":
    app.run(debug=True)