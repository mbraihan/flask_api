from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
import os

load_dotenv()

# PostgreSQL Database credentials loaded from the .env file
DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

app = Flask(__name__)

# CORS implemented so that we don't get errors when trying to access the server from a different server location
CORS(app, support_credentials=True)


try:
    con = psycopg2.connect(
        database=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD)

    cur = con.cursor()

    # GET: Fetch all cameras from the database
    @app.route('/')
    def fetch_all_cameras():
        cur.execute('SELECT * FROM cameras')
        rows = cur.fetchall()
        print(rows)

        return jsonify(rows)

    # GET: Fetch cameras by camerasId from the database
    @app.route('/<int:id>')
    def fetch_by_id(id=None):
        cur.execute(f'SELECT * FROM cameras WHERE id = {id}')
        rows = cur.fetchall()
        print(rows)

        return jsonify(rows)

    # POST: Create cameras and add them to the database
    @app.route('/add-camera', methods=['GET', 'POST'])
    def add_cameras():
        if request.method == 'POST':
            data = request.form.to_dict()
            print(data)
            cur.execute("INSERT INTO cameras (u_name, password, ip_addr, port_number, channel_no, stream_type, mac_address) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (f"{data['u_name']}", f"{data['password']}", data['ip_addr'],
                        f"{data['port_number']}", f"{data['channel_no']}", f"{data['stream_type']}", f"{data['mac_address']}"))
            con.commit()
            return 'Form submitted'
            return redirect('http://localhost:3000', code="200") #Redirect to homepage
        else:
            return 'Form submission failed'

    # # DELETE: Delete cameras by camerasId from the database
    # @app.route('/delete-cameras', methods=['GET', 'DELETE'])
    # def delete_by_id():
    #     id = request.form.to_dict()
    #     print(id['camerasId'])
    #     cur.execute(
    #         f"DELETE FROM cameras WHERE id = {id['camerasId']} RETURNING cameras_name")
    #     con.commit()

    #     return 'cameras Deleted'

    # # PUT: Update cameras by camerasId from the database
    # @app.route('/update-cameras', methods=['GET', 'PUT'])
    # def update_by_id():

    #     cur.execute(
    #         'UPDATE cameras SET cameras_name = \'Goldeneye\' WHERE id = 1')
    #     con.commit()

    #     return 'cameras Updated'


        # POST: Create cameras and add them to the database
    @app.route('/add-product', methods=['GET', 'POST'])
    def add_products():
        if request.method == 'POST':
            data = request.form.to_dict()
            print(data)
            cur.execute("INSERT INTO products (product_name, brand_name, description, upc_code) VALUES (%s, %s, %s, %s)",
                        (f"{data['product_name']}", f"{data['brand_name']}", data['description'], f"{data['upc_code']}"))
            con.commit()
            return 'Form submitted'
            return redirect('http://localhost:3000', code="200") #Redirect to homepage
        else:
            return 'Form submission failed'

except:
    print('Error')

if __name__ == '__main__':
    app.run(debug=True)