from flask import Flask, render_template, request, redirect

app = Flask(__name__)

data = {
    "allowance": 0,
    "expenses": 0,
    "savings": 0,
    "logs": []  
}

def get_balance():
    return data["allowance"] - (data["expenses"] + data["savings"])

@app.route('/')
def index():
    return render_template('index.html', data=data, balance=get_balance())

@app.route('/add_allowance', methods=['POST'])
def add_allowance():
    amount = float(request.form.get('amount', 0))
    data["allowance"] += amount
    data["logs"].append(f"Added ₱{amount} to Allowance")
    return redirect('/')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = float(request.form.get('amount', 0))
    category = request.form.get('category')
    
    if amount <= get_balance():
        data["expenses"] += amount
        data["logs"].append(f"Spent ₱{amount} on {category}")
    else:
        print("Not enough balance!")
        
    return redirect('/')

@app.route('/add_savings', methods=['POST'])
def add_savings():
    amount = float(request.form.get('amount', 0))
    if amount <= get_balance():
        data["savings"] += amount
        data["logs"].append(f"Set aside ₱{amount} for Savings")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)