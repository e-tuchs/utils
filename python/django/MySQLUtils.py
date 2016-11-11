# -*- coding: utf-8 -*-
import MySQLdb
from django.conf import settings


class MySqlDriver(object):

    _conn, db, db_host, db_user, db_pwd = (None for i in range(5))
    data_str = {}

    def __init__(self, target):         # target:  db name
        self.db = settings.DATABASES[target]['NAME']
        self.db_host = settings.DATABASES[target]['HOST']
        self.db_user = settings.DATABASES[target]['USER']
        self.db_pwd = settings.DATABASES[target]['PASSWORD']
        self.mysql_connect()

    def mysql_connect(self):
        try:
            self._conn = MySQLdb.connect(
                host=self.db_host, user=self.db_user, passwd=self.db_pwd, db=self.db, charset='utf8')
        except Exception, e:
            print e

    def execute_sql(self, tpl, place=()):
        fetchall, cur = None, None
        try:
            cur = self._conn.cursor()
            if place:
                cur.execute(tpl, place)
            else:
                cur.execute(tpl)
            self._conn.commit()
            fetchall = cur.fetchall()
        except Exception, e:
            print e
        finally:
            if cur:
                cur.close()
            return fetchall

    def upsert_items(self, table, db_dicts):
        '''
        :param insert_value:    type:dict  format:{ mysql_colume : value_for_colume}
        :param table:  target mysql table
        :return:    nothing
        '''
        insert_placeholders = ', '.join(['%s'] * len(db_dicts))
        columns = ', '.join(db_dicts.keys())
        upsert_holders = ', '.join(keys + " = %s " for keys in db_dicts.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )  ON DUPLICATE KEY UPDATE %s " %\
               (table, columns, insert_placeholders, upsert_holders)
        if db_dicts:
            return self.execute_sql(tpl=sql, place=(db_dicts.values()+db_dicts.values()))
        else:
            return None

    def select_item(self, table, where={}, fileds=[]):
        _where = ', '.join(keys + " = %s" for keys in where.keys())
        sql = "SELECT %s FROM %s WHERE %s" % (','.join(fileds), table, _where)
        return self.execute_sql(tpl=sql, place=(where.values()))

    def disconn(self):
        if self._conn:
            self._conn.close()
