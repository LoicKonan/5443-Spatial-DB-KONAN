import json
import psycopg2

class DatabaseCursor(object):
    """https://stackoverflow.com/questions/32812463/setting-schema-for-all-queries-of-a-connection-in-psycopg2-getting-race-conditi
    https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
    """

    def __init__(self, conn_config_file):
        with open(conn_config_file) as config_file:
            self.conn_config = json.load(config_file)

    def __enter__(self):
        self.conn = psycopg2.connect(
            "dbname='"
            + self.conn_config["dbname"]
            + "' "
            + "user='"
            + self.conn_config["user"]
            + "' "
            + "host='"
            + self.conn_config["host"]
            + "' "
            + "password='"
            + self.conn_config["password"]
            + "' "
            + "port="
            + self.conn_config["port"]
            + " "
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SET search_path TO " + self.conn_config["schema"])

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # some logic to commit/rollback
        self.conn.commit()
        self.conn.close()


class DBQuery(object):
    def __init__(self, config):
        self.result = {}
        self.config = config
        self.limit = 1000
        self.offset = 0

    def __query(self, sql, qtype=None):
        with DatabaseCursor(self.config) as cur:
            #print(sql)
            cur.execute(sql)

            if qtype == 1:
                self.result["data"] = cur.fetchone()
            elif qtype == 2:
                self.result["data"] = cur.fetchmany()
            elif qtype == 3:
                self.result["data"] = cur.fetchall()

            self.result["limit"] = self.limit
            self.result["offset"] = self.offset
            self.result["sql"] = sql
            self.result["success"] = cur.rowcount > 0
            self.result["effectedRows"] = cur.rowcount
        return self.result

    def queryPost(self, sql, **kwargs):

        return self.__query(sql)

    def queryOne(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit

        return self.__query(sql + f" LIMIT {self.limit} OFFSET {offset}",1)

    def queryMany(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit
        return self.__query(sql + f" LIMIT {self.limit} OFFSET {offset}",3)


    def queryAll(self, sql, **kwargs):

        limit = kwargs.get("limit", self.limit)
        offset = kwargs.get("offset", self.offset)
        self.result["offset"] = offset

        if limit:
            self.limit = limit

        return self.__query(sql + f" LIMIT {self.limit} OFFSET {offset}",3)




# class DBQuery(object):
#     def __init__(self, config):
#         self.result = {}
#         self.config = config
#         self.limit = 1000
#         self.offset = 0

#     def __query(self, sql, qtype=3):
#         with DatabaseCursor(self.config) as cur:
#             #print(sql)
#             cur.execute(sql)

#             if qtype == 1:
#                 self.result["data"] = cur.fetchone()
#             elif qtype == 2:
#                 self.result["data"] = cur.fetchmany()
#             else:
#                 self.result["data"] = cur.fetchall()

#             self.result["limit"] = self.limit
#             self.result["offset"] = self.offset
#             self.result["sql"] = sql
#             self.result["success"] = cur.rowcount > 0
#             self.result["effectedRows"] = cur.rowcount
#         return self.result

#     def queryOne(self, sql, **kwargs):

#         limit = kwargs.get("limit", self.limit)
#         offset = kwargs.get("offset", self.offset)
#         noPagination = kwargs.get("noPagination",None)
#         self.result["offset"] = offset

#         if limit:
#             self.limit = limit
        
#         loff = f" LIMIT {self.limit} OFFSET {offset}"

#         if noPagination:
#             loff = ""

#         return self.__query(sql + loff)

#     def queryAll(self, sql, **kwargs):

#         limit = kwargs.get("limit", self.limit)
#         offset = kwargs.get("offset", self.offset)
#         noPagination = kwargs.get("noPagination",None)

#         self.result["offset"] = offset

#         if limit:
#             self.limit = limit

#         loff = f" LIMIT {self.limit} OFFSET {offset}"

#         if noPagination:
#             loff = ""

#         return self.__query(sql + loff)

#     def queryMany(self, sql, **kwargs):

#         limit = kwargs.get("limit", self.limit)
#         offset = kwargs.get("offset", self.offset)
#         noPagination = kwargs.get("noPagination",None)

#         self.result["offset"] = offset

#         if limit:
#             self.limit = limit

#         loff = f" LIMIT {self.limit} OFFSET {offset}"

#         if noPagination:
#             loff = ""

#         return self.__query(sql + loff)
