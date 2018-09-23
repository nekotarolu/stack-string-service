import datetime
import sqlite3
import config

def init_db():
    ret = True

    now = datetime.datetime.now()
    connection = sqlite3.connect(config.DATABASE_LOCATION)
    try:
        coursor = connection.cursor()
        connection.execute("CREATE TABLE IF NOT EXISTS variable (target TEXT PRIMARY KEY NOT NULL, date TEXT NOT NULL)")
        connection.execute("CREATE TABLE IF NOT EXISTS stack (target TEXT NOT NULL, number INTEGER NOT NULL, str TEXT NOT NULL, date TEXT NOT NULL, PRIMARY KEY(target, number))")

        coursor.execute("SELECT * FROM variable WHERE target = '"+ config.GLOBAL_TARGET +"'")
        if len(coursor.fetchall()) > 0:
            print("in if: len(coursor.fetchall()) > 0")
        else:
            print("in else: INSERT INTO variable!!")
            now_str = now.strftime('%Y%m%d%H%M%S')
            connection.execute("INSERT INTO variable (target, date) VALUES ( ?, ? )", (config.GLOBAL_TARGET, now_str))
            
    except sqlite3.Error as e:
        ret = False
        print("sqlite3 error occurred:", e.args[0])

    connection.commit()
    connection.close()

    return ret

def push_stack(target: str, string: str):
    print("-- PushStack start --")

    ret = True

    #DataBase init.
    init_db()

    #PushStack real start.
    now = datetime.datetime.now()
    connection = sqlite3.connect(config.DATABASE_LOCATION)
    try:
        coursor = connection.cursor()

        target_p = target
        if target_p is None:
            print("target_p is None!")
            target_p = "None"
        print("target_p=" + target_p)

        result = coursor.execute("SELECT MAX(number) FROM stack WHERE target ='" + target_p + "'").fetchall()
        print(result)

        number_p = 0
        if result[0][0] is None:
            print("in if: Push result is None.")
        else:
            number_p = result[0][0] + 1
            print("in else: Push result select max(number) ", result[0][0])
        print("number_p=" + str(number_p))

        string_p = string
        if string_p is None:
            print("string_p is None!")
            string_p = "None"
        print("string_p=" + string_p)

        now_str = now.strftime('%Y%m%d%H%M%S')

        insert_sql = "INSERT INTO stack (target, number, str, date) VALUES (?, ?, ?, ?)"
        insert_prm = (target_p, number_p, string_p, now_str)
        coursor.execute(insert_sql, insert_prm)

        print("stack string: insert success!!")
    except sqlite3.Error as e:
        ret = False
        print("sqlite3 error occurred:", e.args[0])

    connection.commit()
    connection.close()

    print("-- PushStack end --")
    return ret


def pop_stack(target: str):
    print("-- PopStack Start --")

    #DataBase init.
    init_db()

    #PopStack real start.
    connection = sqlite3.connect(config.DATABASE_LOCATION)
    try:
        coursor = connection.cursor()
        target_p = target
        if target_p is None:
            print("target_p is None!")
            target_p = "None"
        print("target_p=" + target_p)

        if config.DATA_PERSISTENCE_FLAG is True:
            result = coursor.execute("SELECT number, str FROM stack WHERE target ='"+ target_p + "' ORDER BY number DESC").fetchall()
        else:
            result = coursor.execute("SELECT number, str FROM stack WHERE target ='"+ target_p + "' AND number =(SELECT MAX(number) FROM stack WHERE target ='"+ target_p +"')").fetchall()
            connection.execute("DELETE FROM stack WHERE target ='"+ target_p + "' AND number =(SELECT MAX(number) FROM stack WHERE target ='"+ target_p +"')")
            connection.commit()
        print(result)

    except sqlite3.Error as e:
        result = None
        print("sqlite3 error occurred:", e.args[0])

    connection.close()

    print("-- PopStack End --")
    return result


def is_empty(target: str):
    ret = True

    init_db()

    connection = sqlite3.connect(config.DATABASE_LOCATION)
    try:
        coursor = connection.cursor()
        target_p = target
        if target_p is None:
            print("target_p is None!")
            target_p = "None"
        print("target_p=" + target_p)
        
        result = coursor.execute("SELECT MAX(number) FROM stack WHERE target ='" + target_p + "'").fetchall()
        print(result)
        
        if result[0][0] is None:
            ret = True
            print("isEmpty true!")
        else:
            ret = False
            print("isEmpty false.")
    except sqlite3.Error as e:
        ret = False
        print("sqlite3 error occurred:", e.args[0])

    connection.close()
    print("-- isEmpty End --")

    return ret

