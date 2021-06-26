import pymysql
import MLparams
import numpy as np

def connectDB():
    connection = pymysql.connect(host=MLparams.DB_SERVER,user=MLparams.USER_NAME,passwd=MLparams.PASSWORD,database=MLparams.DB_NAME )
    return connection

def checkTableExists(dbcon, tablename):
    try:
        dbcur = dbcon.cursor()
        dbcur.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(tablename.replace('\'', '\'\'')))
        if dbcur.fetchone()[0] == 1:
            dbcur.close()
            return True

        dbcur.close()
        return False
    except Exception as e:
        return {'error': str(e)}

def checkEmpty(tablename):
    try:
        dbcon = connectDB()
        cursor = dbcon.cursor()
        query = "SELECT count(*) from {}".format(tablename)
        record = cursor.execute(query)
        data = cursor.fetchone()
        print(data[0])
        if data[0] == 0:
            return True
            
        return False
    except Exception as e:
        return {'error': str(e)}    

# creates a connection, if dbcon is not passed explicitly, therefore it commits and collects it by itself
# If it comes from outside then it does nothing on the dbcon object
def insert(dbcon, tablename,element_dict):
    try:
        closeConnection = False
        if dbcon == "":
            closeConnection = True
            dbcon = connectDB()

        #sql = "INSERT INTO place_embeddings (place_id, word_vector) VALUES (%s, %s)"
        #val = ("John", "Highway 21")
        query = "INSERT INTO {} ".format(tablename)
        val_names = "("
        values = " VALUES ("

        for key in element_dict:
            val_names += "{}, ".format(key)
            if key.find('id') != -1 or key == 'Id' or key == 'avg_num':
                values += "{}, ".format(element_dict[key])
            else:
                values += "'{}', ".format(element_dict[key])

        val_names = val_names[:-2]
        val_names += ")"
        values = values[:-2]
        values += ")"

        query = query + val_names + values

        cursor = dbcon.cursor()
        cursor.execute(query)
        insert_id = dbcon.insert_id()

        if closeConnection == True:
            dbcon.commit()
            dbcon.close()
        return {'insert_id': insert_id}
    except Exception as e:
        return {'error': str(e)}
    
def select(id, primary_key, tablename):
    try:
        dbcon = connectDB()
        cursor = dbcon.cursor()
        query = "SELECT * FROM {} WHERE {} = {}".format(tablename, primary_key, id)
        cursor.execute(query)
        record = cursor.fetchall()

        dbcon.close()

        return record
    except Exception as e:
        return {'error': str(e)}

def select_mulparams(element_dict, tablename):
    try:
        dbcon = connectDB()
        cursor = dbcon.cursor()
        query = "SELECT * FROM {} ".format(tablename)
        where_clause = "WHERE"

        for key in element_dict:
            where_clause +=" {} = '{}' AND ".format(key,element_dict[key])

        where_clause = where_clause[:-5]
        query += where_clause

        cursor.execute(query)
        record = cursor.fetchall()

        dbcon.close()

        return record
    except Exception as e:
        return {'error': str(e)}

def selectAll(tablename):
    try:
        dbcon = connectDB()
        cursor = dbcon.cursor()
        query = "SELECT * FROM {}".format(tablename)
        cursor.execute(query)
        record = cursor.fetchall()

        dbcon.close()

        return record
    except Exception as e:
        return {'error': str(e)}  

# In case many ids are passed. We will return multiple rows
def selectIds(ids, primary_key, tablename):
    try:
        dbcon = connectDB()
        cursor = dbcon.cursor()
        query = "SELECT * FROM {} WHERE {} IN (".format(tablename, primary_key)
        for id in ids:
            query += "{}, ".format(id)

        query = query[:-2]
        query += ")"

        cursor.execute(query)
        record = cursor.fetchall()

        dbcon.close()

        return record
    except Exception as e:
        return {'error': str(e)}

def select_like(colname,tablename,text):
    try:
        dbcon = connectDB()
        cursor = dbcon.cursor()
        query = "SELECT * FROM {} WHERE {} LIKE '%{}%'".format(tablename, colname, text)
        cursor.execute(query)
        record = cursor.fetchall()

        dbcon.close()

        return record
    except Exception as e:
        return {'error': str(e)}  

def update(primary_key, element_dict, tablename):
    try:
        dbcon = connectDB()
        cursor = dbcon.cursor()
        #query = "UPDATE {} SET {} = {} WHERE {} = {}".format(tablename, column, value, primary_key, id)
        query = "UPDATE {} ".format(tablename)
        set_clause = "SET "
        where_clause = "WHERE "
        for key in element_dict:
            if key == primary_key:
                where_clause += "{} = {}".format(key, element_dict[key])
            else:
                if key.find('id') != -1 or key == 'Id' or key == 'avg_num':
                    set_clause += "{} = {}, ".format(key, element_dict[key])
                else:
                    set_clause += "{} = '{}', ".format(key, element_dict[key])

        set_clause = set_clause[:-2]
        set_clause += " "
        query = query + set_clause + where_clause

        cursor.execute(query)

        dbcon.commit()
        dbcon.close()

    except Exception as e:
        return {'error': str(e)}

def delete(id, primary_key, tablename):
    try:
        dbcon = connectDB()
        cursor = dbcon.cursor()
        query = "DELETE FROM {} WHERE {} = {}".format(tablename, primary_key, id)
        cursor.execute(query)

        dbcon.commit()
        dbcon.close()
    except Exception as e:
        return {'error': str(e)}

def deserializedata(string_vec):
    word_vec = list(string_vec.split(" "))
    word_vec = [float(ele) for ele in word_vec]
    word_vec = np.array(word_vec)
    word_vec = word_vec.reshape(1,-1)
    return word_vec

def serializedata(word_vec):
    string_vec = word_vec.tolist()[0]
    string_vec = " ".join([str(i) for i in string_vec])
    return string_vec
    
