from flask import Flask, render_template, jsonify, make_response, request, abort
from flask.wrappers import Response
import mysql.connector, math
from mysql.connector.errors import DatabaseError
from datetime import timedelta, datetime

app = Flask(__name__)

#koneksi ke-DB 
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="parkir"
)
if mydb.is_connected():
    print("Berhasil terhubung ke database")
else:
    print("gagal menghubungkan ke database")



# #home page
# @app.route('/')
# #fungsi home page  
# def home():
#     return render_template('index.html')


# TAMPIL DATA SEMUA 
@app.route('/parkir', methods =['GET'])
def parkir(): 
    # method GET 'mendapatkan semua id '
    if request.method == 'GET':
        cursor = mydb.cursor()
        sql = "SELECT * FROM parkir"
        cursor.execute(sql,)
        results = cursor.fetchall()
        payload = ["All data"]
        content = {}
        for result in results:
            content = {'id': result[0], 'kode_kartu': result[1], 'jam_msk': result[2], 'jam_keluar': result[3], 'jenis': result[4], 'kondisi': result[5], 'biaya': result[6],}
            payload.append(content)
            content = {}
        return jsonify(payload)

#MENAMBAH DATA  MOBIL
@app.route('/parkir/mobil', methods =['POST'])
def parkir_mobil(): 
        kode_kartu = request.json['kode_kartu'].upper()
        jam_msk = datetime.now()
        jenis = "Mobil"
        kondisi = "Aktif"
        #tambahdata
        cursor = mydb.cursor()
        sql = "INSERT INTO parkir(kode_kartu, jam_msk, jenis, kondisi ) VALUES (%s, %s, %s, %s)"
        val = (kode_kartu, jam_msk, jenis, kondisi)
        cursor.execute(sql, val,)
        mydb.commit()

        
        cursor = mydb.cursor()
        sql = "SELECT * FROM parkir where kode_kartu =%s"
        val = (kode_kartu,)
        cursor.execute(sql,val)
        result = cursor.fetchone()
   
        content = {'kode_kartu': result[1], 'jam_msk': result[2],'jenis': result[4], 'kondisi': result[5],}
        return jsonify(content)

#MENAMBAH DATA MOTOR 
@app.route('/parkir/motor', methods =['POST'])
def parkir_motor(): 
        kode_kartu = request.json['kode_kartu'].upper()
        jam_msk = datetime.now()
        jenis = "Motor"
        kondisi = "Aktif"

        #tambahdata
        cursor = mydb.cursor()
        sql = "INSERT INTO parkir(kode_kartu, jam_msk, jenis, kondisi) VALUES (%s, %s, %s, %s)"
        val = (kode_kartu, jam_msk, jenis, kondisi)
        cursor.execute(sql, val,)
        mydb.commit()
        
        cursor = mydb.cursor()
        sql = "SELECT * FROM parkir where kode_kartu =%s"
        val = (kode_kartu,)
        cursor.execute(sql,val)
        result = cursor.fetchone()
   
        content = {'kode_kartu': result[1], 'jam_msk': result[2],'jenis': result[4], 'kondisi': result[5],}
        return jsonify(content)
    

#PROSES id  
@app.route('/parkir/<id>', methods =['GET','PUT','DELETE'])
def parkir_id (id): 
    # method GET untuk mendapatkan id yang dimau entah itu motor atau mobil 
    if request.method == 'GET':
        cursor = mydb.cursor()
        sql = "SELECT * FROM parkir where id =%s"
        val = (id,)
        cursor.execute(sql,val)
        result = cursor.fetchone()
        if result is None:
            return Response ("data parkir not Found",status=404)

        content = {'id': result[0], 'kode_kartu': result[1], 'jam_msk': result[2], 'jam_keluar': result[3], 'jenis': result[4], 'kondisi': result[5], 'biaya': result[6],}
        return jsonify(content)

    # method PUT unutk mendapatkan id yang ingin diubah 
    elif request.method == 'PUT':
        # mengecek dataid untuk apakah id  yang ingin di ubah sesuai apa tidak 
        dataid = request.json['id']
        if int (id) != dataid:
            return Response ("id tidak sesuai ",status=500) 


        jam_keluar = datetime.now()
        kondisi = "Non Aktif"
        #
        cursor= mydb.cursor()
        sql = "SELECT * FROM parkir where id =%s"
        val = (id,)
        cursor.execute(sql,val)
        result = cursor.fetchone()
        #untuk mengecek data apakah id ada di dalam database atau tidakk 
        if result is None:
            mydb.commit()
            return Response ("data parkir not Found",status=404)

        sql = "UPDATE parkir SET jam_keluar =%s ,kondisi =%s WHERE id =%s "
        val = (jam_keluar,kondisi,id,)
        cursor.execute(sql, val,)
        mydb.commit()
        return request.json

    elif request.method == 'DELETE':
        cursor= mydb.cursor()
        sql = "DELETE FROM parkir WHERE id =%s "
        val = (id,)
        cursor.execute(sql, val)
        mydb.commit()
        return "{} data berhasil di hapus".format(cursor.rowcount)
    
    else: 
        return Response("unknown method",status=405)



################################################

@app.route('/parkir/kode/<kode_kartu>', methods =['GET','PUT','DELETE'])
def parkir_code(kode_kartu):
    # method GET untuk mendapatkan kode kartu  yang dimau 
    if request.method == 'GET':
        cursor = mydb.cursor()
        sql = "SELECT * FROM parkir WHERE kode_kartu =%s"
        val = (kode_kartu,)
        cursor.execute(sql,val)
        results = cursor.fetchall()
        payload = []
        for result in results:
            content = {'id': result[0], 'kode_kartu': result[1], 'jam_msk': result[2], 'jam_keluar': result[3], 'jenis': result[4], 'kondisi': result[5], 'biaya': result[6],}
            payload.append(content)
        return jsonify(payload)
        
        
    elif request.method == 'PUT':
        # mengecek dataid untuk apakah id  yang ingin di ubah sesuai apa tidak 
        datakartu = request.json['kode_kartu']
        if kode_kartu != datakartu:
            return Response ("kode tidak sesuai ",status=500) 

    
        kode = request.json['kode_kartu']
        kode_kartu = kode.upper()
        jam_keluar = datetime.now()
        kondisi = "Non Aktif"
        
        #
        cursor= mydb.cursor()
        sql = "SELECT * FROM parkir WHERE kode_kartu =%s"
        val = (kode_kartu,)
        cursor.execute(sql,val)
        result = cursor.fetchone()
        #untuk mengecek data apakah id ada di dalam database atau tidakk 
        if result is None:
            mydb.commit()
            return Response ("kode parkir not Found",status=404)

        sql = "UPDATE parkir SET jam_keluar =%s ,kondisi =%s WHERE kode_kartu =%s and kondisi ='aktif'"
        val = (jam_keluar,kondisi,kode_kartu,)
        cursor.execute(sql,val,)
        mydb.commit()
        return parkir_biaya(kode_kartu) # clear ubah/kodekartu

    elif request.method == 'DELETE':
        cursor= mydb.cursor()
        sql = "DELETE FROM parkir WHERE kode_kartu =%s "
        val = (kode_kartu,)
        cursor.execute(sql, val)
        mydb.commit()
        return "{} data berhasil di hapus".format(cursor.rowcount)
    
    else: 
        return Response("unknown method",status=405)





@app.route('/parkir/biaya/<kode_kartu>', methods = ['PUT'])
def parkir_biaya(kode_kartu):
    #biaya 
        cursor = mydb.cursor()
        jam_msk = "SELECT jam_msk FROM parkir WHERE kode_kartu = %s "
        val = (kode_kartu,)
        cursor.execute(jam_msk, val)
        results = cursor.fetchall()

        for data in results:
            masuk = data[0]  

        cursor = mydb.cursor()
        jam_keluar = "SELECT jam_keluar FROM parkir WHERE kode_kartu = %s "
        val = (kode_kartu,)
        cursor.execute(jam_keluar, val)
        results = cursor.fetchall()
        for keluar in results:
            out = keluar[0]
        

        cursor = mydb.cursor()
        jenis = "SELECT jenis FROM parkir WHERE kode_kartu = %s "
        val = (kode_kartu,)
        cursor.execute(jenis, val)
        results = cursor.fetchall()
        for knd in results:
            jns = knd[0]

        selisih = out - masuk
        lama_jam = ((selisih.days*24*60*60)+selisih.seconds)/ (60*60)
        a = math.ceil(lama_jam)

        # 1  
        if a == 1 and jns == "Motor"    :
            biaya = a * 2000
        elif a == 1 and jns == "Mobil"  :
            biaya = a * 3000
    
        #2
        elif a == 2 and jns == "Motor"  :
            biaya = a * 2000
        elif a == 2 and jns == "Mobil"  :
            biaya  = a * 3000
        
        #3
        elif a == 3 and jns == "Motor"  :
            biaya = a * 2000   
        elif a == 3 and jns == "Mobil"  :
            biaya = a * 3000
         

        #4
        elif a == 4 and jns == "Motor"  :
            biaya = a * 2000
        elif a == 4 and jns == "Mobil"  :
            biaya = a * 3000
         
        #5
        elif a == 5 and jns == "Motor"  :
            biaya = a * 2000
        elif a == 5 and jns == "Mobil"  :
            biaya = a * 3000
           
        #>=6
        elif a >= 6 and jns == "Motor"  :
            biaya = 6 * 2000
        elif a >= 6 and jns == "Mobil"  :
            biaya = 2 * 10000
            

        sql = "UPDATE parkir SET biaya =%s  WHERE kode_kartu =%s "
        val = (biaya, kode_kartu,)
        cursor.execute(sql,val,)
        mydb.commit()
        return harga(kode_kartu) # clear ubah/kodekartu



@app.route('/parkir/biaya/<kode_kartu>', methods = ['GET'])
def harga(kode_kartu):
    cursor = mydb.cursor()
    sql = "SELECT * FROM parkir where kode_kartu =%s"
    val = (kode_kartu,)
    cursor.execute(sql,val)
    result = cursor.fetchone()
   
    content = {'kode_kartu': result[1], 'jam_msk': result[2], 'jam_keluar': result[3], 'jenis': result[4], 'kondisi': result[5], 'biaya': result[6],}
    return jsonify(content)


app.run(debug=True)





# #form search
# @app.route('/satudata')
# def search():
#     return render_template('satu_data.html')

# #satu data
# @app.route('/satudata', methods =['GET','POST'])
# #fungsi ambil salah satu data 
# def ambil_data():
#     details = request.form['kode_kartu']
#     val = details.upper()
#     cursor = mydb.cursor()
#     sql = "SELECT * FROM parkir WHERE kode_kartu =%s"
#     cursor.execute(sql,(val,))
#     results = cursor.fetchall()
#     payload = []
#     content = {}
#     for result in results:
#         content = {'id': result[0], 'kode_kartu': result[1], 'tanggal_msk': result[2], 'jam_msk': result[3], 'tanggal_keluar': result[4], 'jam_keluar': result[5], 'jenis': result[6], 'kondisi': result[7], 'biaya': result[8], }
#         payload.append(content)
#         content = {}
#         return jsonify(payload)
     

# #form tambah data
# @app.route('/tambahdata')
# #fungsi tambah_page  
# def tambah():
#     return render_template('tambah.html')

# @app.route('/tambahdata', methods =['GET','POST'])
# #fungsi tambahdata  
# # def tambah_data():
#     kode = request.form['kode_kartu']
#     kode_kartu = kode.upper()
#     tgl_msk = request.form['tgl_msk']
#     jam_msk = request.form['jam_msk']
#     jns = request.form['jenis']
#     sts = request.form['sts']
#     #tambahdata
#     cursor = mydb.cursor()
#     sql = "INSERT INTO parkir(kode_kartu, tanggal_msk, jam_msk, jenis, kondisi ) VALUES (%s, %s, %s, %s, %s)"
#     val = (kode_kartu, tgl_msk, jam_msk, jns, sts)
#     cursor.execute(sql, val,)
#     mydb.commit()
#     return tampil_data()

# #form ubahdata
# @app.route('/ubahdata')
# #fungsi ubah page  
# def ubah():
#     return render_template('ubah.html')


# @app.route('/ubahdata',methods=['PUT'])
# #fungsi ubah_data
# def ubah_data():
#     kode = request.form['kode_kartu']
#     kode_kartu = kode.upper()
#     tgl_keluar = request.form['tanggal_keluar']
#     jam_keluar = request.form['jam_keluar']
#     sts = request.form['sts']
#     #
#     cursor= mydb.cursor()
#     sql = "UPDATE parkir SET tanggal_keluar =%s ,jam_keluar =%s ,kondisi =%s WHERE kode_kartu =%s "
#     val = (tgl_keluar),(jam_keluar),(sts),(kode_kartu)
#     cursor.execute(sql, val,)
#     mydb.commit()
#     return ambil_data()



# #form delete 
# @app.route('/hapusdata')
# def delete():
#     return render_template('hapus.html')

# @app.route('/hapusdata', methods =['GET','POST'])
# #fungsi hapus salah satu data 
# def hapus_data():
#     details = request.form['kode_kartu']
#     val = details.upper()
#     cursor = mydb.cursor()
#     sql = "DELETE FROM parkir WHERE kode_kartu =%s"
#     cursor.execute(sql, (val,))
#     mydb.commit()
#     return tampil_data()





