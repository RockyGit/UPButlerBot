import psycopg2

class PostgreSQL:

    dsn = ("host='localhost' dbname='info' user='postgres' password='admin'")
    dsn2 = ("host='localhost' dbname='postgres' user='postgres' password='admin'")

    def __init__(self):
        self.conn = psycopg2.connect(self.dsn)
        self.conn2 = psycopg2.connect(self.dsn2)
        self.cur = self.conn.cursor()
        self.cur2 = self.conn2.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.conn as cons:
            with cons.cursor() as curs:
                return curs.execute('SELECT * FROM info').fetchall()

    def select_phone(self, phone):
        """ Получаем запись по номеру телефона """
        with self.conn as cons:
            with cons.cursor() as curs:
                curs.execute('SELECT * FROM info WHERE phone = %s', (phone,))
                return curs.fetchall()

    def select_fio(self, f, i='', o=''):
        """ Получаем запись по fio """
        with self.conn as cons:
            with cons.cursor() as curs:
                if o:
                    curs.execute('SELECT * FROM info WHERE s_name = %s and f_name = %s and p_name = %s',
                                 (f,i,o,))
                else:
                    curs.execute('SELECT * FROM info WHERE s_name = %s and f_name = %s',
                                 (f,i,))
                return curs.fetchall()

    def select_company(self, company):
        """ Получаем запись пo company """
        with self.conn as cons:
            with cons.cursor() as curs:
                curs.execute('SELECT * FROM info WHERE company = %s', (company,))
                return curs.fetchall()

    def select_5(self):
        with self.conn as cons:
            with cons.cursor() as curs:
                return curs.fetchall()

    def select_like_fiz(self, st):
        #st = '%%'+st+'%%'
        stri = ''
        fields = ['docs.sname', 'docs.fname', 'docs.pname',  'docs.inn']
        for f in fields:
            for s in st:
                stri = stri + f + " like '%%" + s + "%%' or "
        queryfiz = 'select docs.sname, docs.fname, docs.pname,  docs.inn ' \
                    'from docs where ' + stri[0:len(stri) - 3]
        with self.conn2 as cons:
            with cons.cursor() as curs:
                curs.execute(queryfiz)
                return curs.fetchall()


    def select_like_ur(self, st):
        # st = '%%'+st+'%%'
        stri_f = ''
        stri_d = ''
        stri_h = ''
        fields_heads = ['sname', 'fname', 'pname', 'inn']
        fields_founders = ['sname', 'fname', 'pname', 'inn']
        fields_docs = ['naimorg', 'naimorgsokr', 'inn']
        for f in fields_heads:
            for s in st:
                stri_h = stri_h + f + " like '%%" + s + "%%' or "
        for f in fields_founders:
            for s in st:
                stri_f = stri_f + f + " like '%%" + s + "%%' or "
        for f in fields_docs:
            for s in st:
                stri_d = stri_d + f + " like '%%" + s + "%%' or "
        query_h = 'SELECT sname, fname, pname, inn ' \
                   'from docs WHERE ' + stri_h[0:len(stri_h) - 3]
        query_f = 'select sname, fname, pname, inn ' \
                  'from docs where ' + stri_f[0:len(stri_f) - 3]
        query_d = 'select naimorg, naimorgsokr, inn ' \
                  'from docs where ' + stri_d[0:len(stri_d) - 3]
        with self.conn2 as cons:
            with cons.cursor() as curs:
                curs.execute("SELECT * FROM (" + query_h + ") as heads,("+
                             query_f + ") as founders,("
                             + query_d + ") as docs order by heads.inn, founders.inn, docs.inn")
                return curs.fetchall()


    def find_user(self, id):
        with self.conn as cons:
            with cons.cursor() as curs:
                curs.execute('SELECT * FROM pers WHERE id = %s', (id,))
                return curs.fetchone()

    def reg_user(self, phone, id):
        with self.conn as cons:
            with cons.cursor() as curs:
                return curs.execute('INSERT INTO pers VALUES (%s, %s, %s)', (phone,id,'CURRENT_DATE',))

    def insert_person(self, values):
        with self.conn as cons:
            with cons.cursor() as curs:
                return curs.execute('INSERT INTO pers VALUES (%s)', (values))

    def copy_to_docs(self,file):
        io = open(file, 'r')
        with self.conn2 as cons:
            with cons.cursor() as curs:
                flag = curs.copy_from(io, 'docs', ';')
                io.close()
                return flag

    def copy_to_okved(self,file):
        io = open(file, 'r')
        with self.conn2 as cons:
            with cons.cursor() as curs:
                flag = curs.copy_from(io, 'okved', '&')
                io.close()
                return flag

    def copy_from_json(self, file):
        io = open(file, 'r')
        readAll = io.readlines()
        with self.conn2 as cons:
            with cons.cursor() as curs:
                flag = curs.executemany("INSERT INTO okved VALUES (%s)", (readAll,))
                io.close()
                return flag

    def copy_to_okveddocs(self,file):
        io = open(file, 'r')
        with self.conn2 as cons:
            with cons.cursor() as curs:
                flag = curs.copy_from(io, 'okveddocs', ';')
                io.close()
                return flag

    def copy_to_heads(self,file):
        io = open(file, 'r')
        with self.conn2 as cons:
            with cons.cursor() as curs:
                flag = curs.copy_from(io, 'heads', ';')
                io.close()
                return flag

    def copy_to_founders(self,file):
        io = open(file, 'r')
        with self.conn2 as cons:
            with cons.cursor() as curs:
                flag = curs.copy_from(io, 'founders', ';')
                io.close()
                return flag

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    # def close(self):
    #     """ Закрываем текущее соединение с БД """
    #     self.cur.close()
    #     self.conn.close()