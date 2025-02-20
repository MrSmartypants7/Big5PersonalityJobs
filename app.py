#####################################################
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import webbrowser
from numpy import *
from sklearn.linear_model import LogisticRegression
import urllib.parse

#####################################################

app = Flask(__name__)

#####################################################
# Loading Dataset Globally
data = pd.read_csv("dataset.csv")
array = data.values

for i in range(len(array)):
    if array[i][0] == "Male":
        array[i][0] = 1
    else:
        array[i][0] = 0

df = pd.DataFrame(array)

maindf = df[[0, 1, 2, 3, 4, 5, 6]]
mainarray = maindf.values

temp = df[7]
train_y = temp.values
train_y = temp.values

for i in range(len(train_y)):
    train_y[i] = str(train_y[i])

mul_lr = LogisticRegression(
    multi_class="multinomial", solver="newton-cg", max_iter=1000
)
mul_lr.fit(mainarray, train_y)
#####################################################

# Function to determine job recommendations based on personality traits


def get_job_recommendation(openness, conscientiousness, extraversion, agreeableness, neuroticism):
    if openness >= 6:
        job_field = "UX Designer OR Writer OR Research Scientist OR Graphic Designer"
    elif openness <= 3:
        job_field = "Accountant OR Civil Engineer OR Bank Teller OR Logistics Manager"
    elif conscientiousness >= 6:
        job_field = "Project Manager OR Data Analyst OR Financial Planner OR IT Consultant"
    elif conscientiousness <= 3:
        job_field = "Artist OR Freelance Writer OR Photographer OR Musician"
    elif extraversion >= 6:
        job_field = "Sales Manager OR HR Specialist OR Public Relations OR Event Planner"
    elif extraversion <= 3:
        job_field = "Software Developer OR Data Scientist OR Researcher OR Librarian"
    elif agreeableness >= 6:
        job_field = "Therapist OR Teacher OR Social Worker OR Healthcare Professional"
    elif agreeableness <= 3:
        job_field = "Lawyer OR Business Consultant OR Auditor OR Investment Banker"
    elif neuroticism >= 6:
        job_field = "Librarian OR Archivist OR Data Entry Specialist OR Quality Control Analyst"
    elif neuroticism <= 3:
        job_field = "Surgeon OR Stock Trader OR Emergency Response Officer OR Pilot"
    else:
        job_field = "jobs near me"

    return job_field


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        age = int(request.form["age"])
        if age < 17:
            age = 17
        elif age > 28:
            age = 28

        openness = 9 - int(request.form["openness"])
        neuroticism = 9 - int(request.form["neuroticism"])
        conscientiousness = 9 - int(request.form["conscientiousness"])
        agreeableness = 9 - int(request.form["agreeableness"])
        extraversion = 9 - int(request.form["extraversion"])

        inputdata = [[
            request.form["gender"],
            age,
            openness,
            neuroticism,
            conscientiousness,
            agreeableness,
            extraversion
        ]]

        for i in range(len(inputdata)):
            if inputdata[i][0] == "Male":
                inputdata[i][0] = 1
            else:
                inputdata[i][0] = 0

        df1 = pd.DataFrame(inputdata)
        testdf = df1[[0, 1, 2, 3, 4, 5, 6]]
        maintestarray = testdf.values

        y_pred = mul_lr.predict(maintestarray)
        personality_type = str(y_pred[0])

        # Get job recommendations based on Big 5 traits
        job_search_query = get_job_recommendation(
            openness, conscientiousness, extraversion, agreeableness, neuroticism)
        encoded_query = urllib.parse.quote(job_search_query)
        google_jobs_url = f"https://www.google.com/search?q={encoded_query}&ibp=htl;jobs&hl=en"

        # Open Google Jobs search in a new tab
        webbrowser.open_new_tab(google_jobs_url)

        return render_template("result.html", per=personality_type)


@app.route("/learn")
def learn():
    return render_template("learn.html")


@app.route("/working")
def working():
    return render_template("working.html")

# Handling error 404


@app.errorhandler(404)
def not_found_error(error):
    return render_template("error.html", code=404, text="Page Not Found"), 404

# Handling error 500


@app.errorhandler(500)
def internal_error(error):
    return render_template("error.html", code=500, text="Internal Server Error"), 500


if __name__ == "__main__":
    app.run()
