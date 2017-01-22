import mysql.connector
from datetime import datetime
import json
import uuid

class requestQueue():
    addToQueueSQL = ('INSERT INTO apiQueue(id, typeName, typeId)')
    def __init__(self):
        self.CNX = mysql.connector.connect(
            user='root', 
            password='password',
            host='localhost',
            database='loldata')
        self.cursor = CNX.cursor()

    def add(self, typeName, typeId):
        uuid = uuid.uuid4()
        dto = {
                'id': uuid,
                'typeName': typeName,
                'typeId': typeId,
                'addedOn': datetime.utcnow()
                }
        try:
            self.cursor.execute(addToQueueSQL, dto)
            self.CNX.commit()
        except Exception as e:
            print('Error adding to api queue: ' + e)

    def __exit__(self):
        self.cursor.close()
        self.CNX.close()

