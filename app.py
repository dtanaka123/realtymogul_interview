from flask import Flask,request,jsonify
import csv
import unittest
from settings import APP_CSV_FILE

app = Flask(__name__)

"""
Before we serve our first request I'm going to read the property CSV file into memory. The
reason I did this is because I want to cache the data into memory as the file is only 48KB, so 
a persistent data storage (ie RDBMS/Datastore/etc) is not necessary. Also it appears be a data set 
that would incur many more READ operations than WRITE so caching in memory would be ok in most cases
in terms of consistency.

"""

properties = []

@app.before_first_request
def app_setup():
    print "Parsing CSV File"
    with open(APP_CSV_FILE, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        first = True
        headers = {}
        for row in reader:
            if first is True:
                first = False
                for i in range(0,len(row)):
                    headers[i] = row[i]
            else:
                properties.append(process_row(row,headers))
    
def process_row(row,headers):
    property_dict = {}
    missing_count = 0
    encoded_str = ''
    prev_val_bool = None
    cur_val_bool = None
    current_seq_count = 0
    for i in range(0,len(row)):
            
        if len(row[i]) > 0:
            cur_val_bool = True
        else:
            cur_val_bool = False

        #Populate the properties value
        property_dict[headers[i]] = row[i]
        if row[i] == '':
            missing_count += 1
                        
        if prev_val_bool is not None and cur_val_bool != prev_val_bool:
            encoded_str += str(current_seq_count)
            current_seq_count = 1
        else:
            current_seq_count += 1
                        
        prev_val_bool = cur_val_bool
                
    encoded_str += str(current_seq_count)
    property_dict['MISSING_DATA_ENCODING'] = encoded_str
    property_dict['MISSING_FIELD_COUNT'] = missing_count
    
    return property_dict
        
    

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
@app.route('/data', methods=['GET'])
def get_data():
    state = request.args.get('state')
    results = []
    if state is not None:
        for p in properties:
            if p['STATE_ID'] == state:
                results.append(p)
                
    else:
        results = properties
        
    return jsonify(results),200
    
    
class TestMethods(unittest.TestCase):

    def test_process_row(self):
        headers = {
            0:'H1',
            1:'H2',
            2:'H3',
            3:'H4',
            4:'H5'
        }
        prop = process_row(['asdfas','','','asdfasd','dfasd'],headers)
        self.assertEqual(prop['MISSING_DATA_ENCODING'],'122')
        self.assertEqual(prop['MISSING_FIELD_COUNT'],2)
        
        
if __name__ == "__main__":
    unittest.main()
    