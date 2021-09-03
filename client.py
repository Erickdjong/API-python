from flask import Flask, render_template,request,Response,jsonify
import json
import requests

app = Flask(__name__)


#index
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/masuk/mobil')
def mobil():
    return render_template('form_mobil.html')

@app.route('/masuk/mobil',methods =['POST'])
def masuk_mobil():
    kode = request.form['kode_kartu'].upper
    data = {
        "kode_kartu": kode()
        }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data_json =json.dumps(data)
    r = requests.post("http://127.0.0.1:5000/parkir/mobil", data=data_json, headers= headers)
    
    arr = json.loads(r.text)

    return render_template('table_mobil.html', arrs=arr)


@app.route('/masuk/motor')
def motor():
    return render_template('form_motor.html')

@app.route('/masuk/motor',methods =['POST'])
def masuk_motor():
    kode = request.form['kode_kartu'].upper

    data = {
        "kode_kartu": kode(),
        }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data_json =json.dumps(data)
    r = requests.post("http://127.0.0.1:5000/parkir/motor", data=data_json, headers= headers) 

    arr = json.loads(r.text)

    return render_template('table_motor.html', arrs=arr)




@app.route('/keluar')
def keluar():
    return render_template('form_keluar.html')
    

@app.route('/keluar',methods=['POST'])
def masuk_keluar():
    kode = request.form['kode_kartu'].upper
    code = kode()
    data = {
            "kode_kartu": code
        }

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data_json =json.dumps(data)
    r = requests.put(f"http://127.0.0.1:5000/parkir/kode/{code}", data=data_json, headers= headers)
    arr = json.loads(r.text) 
    return render_template('table_keluar.html', arrs=arr)



# @app.route('/ambil')
# def ambil():
#     return render_template('ambil.html')

# @app.route('/ambil',methods =['POST'])
# def ambil_data():
#     kode = request.form['kode_kartu'].upper
#     code = kode()
#     r = requests.get(f"http://127.0.0.1:5000/parkir/kode/{code}")  
#     return r.text


app.run(port=6060, debug=True)
