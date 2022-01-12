from pymongo import MongoClient
import os
import json as J
import sys


def init_sumer_2_greek_db():
    #############################################
    # Инициализация имен                        #
    #############################################
    dbname = 'sumer_2_greek'
    info_colname = 'doc_md'
    totum_colname = 'totum'
    file_name = 'site_docs_0000_plus.json'
    dir_name = sys.argv[1]
    ##############################################
    # Создаем базу и заполняем материалами сайта #
    ##############################################
    MC = MongoClient()
    db = MC[dbname]
    i_col = db[info_colname]
    d = J.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name), 'r', encoding='utf-8'))
    i_col.insert_many(d)
    i_col.create_index([('id_doc', 1)])
    #############################################
    # Добавляем коллекцию totum                 #
    #############################################
    os.chdir(dir_name)
    totum_file_names = os.listdir()
    t_col = db[totum_colname]
    for n in totum_file_names:
        jdoc = J.load(open(n, 'r', encoding='utf-8'))
        t_col.insert_many(jdoc)
    ind_dict = {
        'titles': 1,
        'subtitles': 1,
        'scheme': 1,
        'verse.rythm': 1,
        'verse.src': 1,
        'verse.trans.text': 1
    }
    for x in ind_dict:
        t_col.create_index([(x, ind_dict[x])])
    MC.close()


if __name__ == '__main__':
    init_sumer_2_greek_db()
