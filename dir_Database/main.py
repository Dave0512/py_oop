from database import Database
import pyodbc
import urllib


db_verb = Database(driver=r"{SQL Server Native Client 11.0};",
                   server=r"192.168.16.124;",
                   database=r"Vorlauf_DB;",
                   tr_conn=r"yes;")


cur = db_verb.cursor()
print(type(cur))

# def main():
#     with db_verb as db:
#         cur = db_verb.cursor()

#         # top5 = cur.execute(""" SELECT TOP 5 * from [Vorlauf_DB].[dbo].tbl_lieferanten """)
#         print(type(cur))

# if __name__ == "__main__":
#     main()




