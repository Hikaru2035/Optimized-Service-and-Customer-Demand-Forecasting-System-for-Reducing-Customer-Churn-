from flask import Flask, request, redirect, url_for, render_template, session
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cần cho session

VALID_USERS = {
    "admin@example.com": "password123",
    "user@example.com": "secret456"
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if VALID_USERS.get(email) == password:
            session['user'] = email
            return redirect(url_for("dashboard"))
        else:
            return render_template("index.html", error="Invalid credentials. Try again")

    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/insight")
def show_csv():
    if "user" not in session:
        return redirect(url_for("login"))

    # Load CSV cho Customer List
    df_customer = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    customer_columns = df_customer.columns.tolist()
    customer_data = df_customer.to_dict(orient="records")

    # Load CSV cho Churn Prediction (giả sử bạn có dữ liệu riêng cho phần này)
    df_churn = pd.read_csv("output/output_with_churn.csv")  # Đổi tên file phù hợp với dữ liệu của bạn
    churn_columns = df_churn.columns.tolist()
    churn_data = df_churn.to_dict(orient="records")

    # Tạo dictionary lookup từ CustomerID -> [col4, col5]
    churn_lookup = {}
    if len(churn_columns) >= 5:
        for row in churn_data:
            churn_lookup[row[churn_columns[0]]] = [row[churn_columns[3]], row[churn_columns[4]]]
            
    return render_template("insight.html",
                       customer_columns=customer_columns,
                       customer_data=customer_data,
                       churn_columns=churn_columns[:3],  # Chỉ hiển thị 3 cột
                       churn_data=churn_data,
                       churn_lookup=churn_lookup)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
