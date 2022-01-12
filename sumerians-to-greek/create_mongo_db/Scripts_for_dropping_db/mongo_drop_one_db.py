from pymongo import MongoClient
import json as J

MC=MongoClient()

def Get_list_of_DB():
    global MC
    return MC.list_database_names()

def Drob_all_DBs():
    global MC
    for dbname in [
        x for x in MC.list_database_names() if x not in [
            'admin', 'config', 'local'
            ]
        ]:
        MC.drop_database(dbname)
    print('Workspace have been cleared')
    print()

def Drop_One_DB(dbname):
    global MC
    MC.drop_database(dbname)

def test1():
    dbname=input('Database name> ')
    Drop_One_DB(dbname)
    print(dbname,'is dropped')

def test():
    global MC
    Drob_all_DBs()
    for dbname in Get_list_of_DB():
        print(dbname)
    print()


if __name__=='__main__':
    test1()


    
    




    



