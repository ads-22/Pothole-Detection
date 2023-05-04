from flask import Flask, render_template, request
import route
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/predict', methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        src = request.form['source']
        dest = request.form['destination']
        x = route.solve(src,dest)
        
    return render_template('predict.html',src=src,dest=dest,x=x)

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)