from flask import make_response, render_template, request, g
from . import routes

def debug(info, type="INFO", forceBreak=False):
    if forceBreak:
        raise ValueError('Something is wrong! {}'.format(info))
    else:
        stmt = "[{}]: {}".format(type, info)
        print("\n\n{}\n\n".format(stmt))

class Handler():
    @staticmethod
    def current_user_id():
        user_id = request.cookies.get("user-id")
        return user_id

    @staticmethod
    def current_user():
        user_id = request.cookies.get("user-id")
        if user_id != None:
            cur = g.sqlite_db.cursor()
            cur.execute("""
            SELECT array_to_json(array_agg(users)) FROM users
                WHERE user_id={};
            """.format(user_id)
            )
            user = cur.fetchone()

            if user:
                return user[0][0]
            else:
                return None
        else:
            return False

class Render():
    @staticmethod
    def html(temp, code=200, **params):
        params['user'] = Handler.current_user()
        response = make_response(render_template(temp, **params), code)
        return response

    @staticmethod
    def text_response(text, code=200, **params):
        response = make_response(text, code)
        return response

    @staticmethod
    def str(temp, **params):
        string = render_template_string(temp, **params)
        return string

    @staticmethod
    def json(temp, **params):
        if "_json" in temp:
            json = render_template(temp, **params)
            return json
        else:
            error = "_json not found, wrong render path?"
            print(error)
            return error
