from flask import Flask
from flask import Flask, render_template, request
from my_scraper import scrape_courses

app = Flask(__name__)

@app.route("/",methods=['GET'] )
def hello_world():
    #return "<p>Hello, World!</p>"
    return render_template("index.html")

@app.route('/scrape_data', methods=['GET','POST'])
def scrape_data():
    categoryName = request.form["categoryName"]
    pageNumbers = request.form["pageNumbers"]

    if pageNumbers.isnumeric() == False:
        return "<p> Number of Page should be numeric </p>"

    df = scrape_courses(categoryName,int(pageNumbers))
    print(df)
    return render_template('df.html',tables=[df.to_html(classes='data')],
            titles = df.columns.values)
    #return "<p> Completed </p>"