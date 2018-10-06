import datetime
import os
import sqlite3
from bottle import route, request, abort, run

import config
import model

_GLOBAL_TARGET_="global"

@route("/")
def welcome_service():
        print("config.DATA_PERSISTENCE_FLAG=" + str(config.DATA_PERSISTENCE_FLAG))
        print("config.DATABASE_LOCATION" + str(config.DATABASE_LOCATION))
        print("config.GLOBAL_TARGET" + str(config.GLOBAL_TARGET))

        print("-- database setup start --")
        ret = model.init_db()
        if ret is True:
                print("-- database setup success --")
        else:
                print("-- database setup failed --")
       
        return "Welcome to the StackStringService!!"


@route("/PushStack", method=['PUT', 'POST'])
def push_stack_route_global():
        return push_stack_route(config.GLOBAL_TARGET)


@route("/PushStack/<target>", method=['PUT', 'POST'])
def push_stack_route(target):
        model.push_stack(target, request.query.string)
        return 'OK'


@route("/PopStack")
def pop_stack_route_global():
        return pop_stack_route(config.GLOBAL_TARGET)


@route("/PopStack/<target>")
def pop_stack_route(target):
        result = model.pop_stack(target)
        if result is None:
                abort(404, "No such database.")
        return str(result)


#return status code = 404: Stack is Empty.
#return status code = 200: Stack isnot Empty.
@route("/isEmpty", method="HEAD")
def is_empty_route_global():
        return is_empty_route(config.GLOBAL_TARGET)


@route("/isEmpty/<target>", method="HEAD")
def is_empty_route(target):
        if model.is_empty(target) is True:
                print("isEmpty true!")
                abort(404, "target stack is Empty.")
        else:
                print("isEmpty false.")

        return "isEmpty call."


if __name__ == "__main__":
        run(host=config.SERVER_HOST_ADDR, port=int(os.environ.get("PORT", config.SERVER_HOST_PORT)))
