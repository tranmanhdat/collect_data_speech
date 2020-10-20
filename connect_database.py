import pymysql.cursors


def get_all_sentences():
    result = []
    dict_sentences = {}
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='45rtfgvb',
                                 db='transcript_collection',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM sentences "
            cursor.execute(sql)
            for row in cursor:
                dict_sentences["id"] = row['id']
                dict_sentences["sentence"] = row['script']
                result.append(dict_sentences)
                # dict_sentences[row['id']] = row['script']
                # id.append(int(row['id']))
    finally:
        connection.close()

    return result

if __name__ == '__main__':
    dict_sentences, id = get_all_sentences()
    print(dict_sentences)
    print(id)