from turtle import pos
from flask import Flask, json
from flask import jsonify
from flask_cors import CORS
from flask import Flask, redirect, request, render_template, session, flash
import datetime
import sqlite3
import time
from werkzeug.utils import secure_filename

from comment.comment_acction import CommentAcction
from post.post_acction import PostAcction

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origin": "*"}})
connection_data = ('phongtro.db')


@app.route('/api/')
def index():
    return ("hello")


@app.route('/api/resigter', methods=['POST'])
def resigter():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    repassword = request.form['repassword']
    email = request.form['email']
    phone = request.form['phone']
    con = sqlite3.connect(connection_data)
    cur = con.cursor()
    isRecordExit = 0
    rows = cur.execute(
        "SELECT * FROM user WHERE username ='"+str(username)+"'")
    for row in rows:
        isRecordExit = 1
    if isRecordExit == 1:
        return "Account has been exited", 401
    else:
        if(password == repassword):
            sql = "INSERT INTO user('name','username','password','email','phone') VALUES ('"+str(name) + \
                "','"+str(username)+"','"+str(password) + \
                "','"+str(email)+"','"+str(phone)+"')"
            cur.execute(sql)
            con.commit()
            con.close()
        else:
            return "Invalid", 401
    return "thanh cong", 200


@app.route('/api/login', methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
    print(username, password)
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    isRecordExit = 0
    sql = "SELECT * FROM user WHERE username ='"+str(username)+"'"
    cur.execute(sql)
    for row in cur:
        isRecordExit = 1
    if isRecordExit == 1:
        if str(row[2]) == username and str(row[3]) == password:
            return "thanh cong", 200
        else:
            return "error", 401
    else:
        print(" tai khoan khong ton tai")
        return "khong ton tai", 401
    return redirect('/api/')


@app.route('/api/sigout')
def sigout():
    session.pop("username", None)
    flash("You have been log out !!")
    return redirect('/api/login')


@app.route('/api/addcmt', methods=['POST'])
def addcomment():
    detail = request.form["comment"]
    username = request.form["username"]
    time = datetime.datetime.now()
    post_ID = request.form["post_ID"]
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    sql = "INSERT INTO comment('detail','username','time','post_ID') VALUES('" + \
        str(detail)+"','"+str(username)+"','" + \
        str(time)+"'," + post_ID+")"
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "thanh cong", 200


@ app.route('/api/showcomment')
def showcommet():
    Comment = CommentAcction(connection_data)
    result = Comment.show_all()
    return jsonify(result)


@app.route('/api/showcmtbyID/<int:id>')
def showcmtbyID(id):
    Comment = CommentAcction(connection_data)
    result = Comment.showbyID(id)
    return jsonify(result)


@app.route('/api/addpost', methods=['POST'])
def addpost():
    ids = int(round(time.time() * 100))
    loai = ''
    #pic = request.files['file']

    title = request.form['title']
    types = request.form['type']
    if types == 'thue':
        loai = 'Cho Thuê'
    elif types == 'tim':
        loai = 'Tìm Phòng'
    elif types == 'ghep':
        loai = 'Ở Ghép'
    elif types == 'homestay':
        loai = 'Căn Hộ'
    elif types == 'other':
        loai = 'Khác'
    dientich = request.form['dientich']
    diachi = request.form['diachi']
    detail = request.form['detail']
    username = request.form['username']
    cost = request.form['cost']
    time_posted = datetime.datetime.now()

    con = sqlite3.connect(connection_data)
    cur = con.cursor()
    sql = "INSERT INTO post ('post_ID','title', 'type','dientich','address', 'detail', 'username','timeposted','cost') VALUES ('"+str(ids)+"','"+str(
        title)+"','"+str(loai)+"','"+str(dientich)+"','"+str(diachi)+"','"+str(detail)+"','"+str(username)+"','"+str(time_posted)+"','"+str(cost)+"')"
    cur.execute(sql)
    # filename = secure_filename(pic.filename)
    # mimetype = pic.mimetype
    # if not filename or not mimetype:
    #     return 'Bad upload!', 400
    # sql2 = "INSERT INTO image_save(name_file,'post_ID',img,mimetype) VALUES (" + \
    #     filename+",'"+str(ids)+"',"+pic.read()+","+mimetype+")"
    # cur.execute(sql2)
    con.commit()
    con.close()
    return "thanh cong", 200


@app.route('/api/showpost')
def showpost():
    Posts = PostAcction(connection_data)
    rs = Posts.show_all()
    return jsonify(rs)


@app.route('/api/deletepost/<int:id>')
def deletepost(id):
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    sql = "DELETE FROM post WHERE post_ID='"+str(id)+"'"
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "thanh cong", 200


@app.route('/api/selectpost/<int:id>')
def selectpostById(id):
    Posts = PostAcction(connection_data)
    result = Posts.showById(id)
    return jsonify(result)


@app.route('/api/editpost', methods=['POST'])
def editpostById():
    post_ID = request.form['post_ID']
    title = request.form['title']
    type = request.form['type']
    detail = request.form['detail']
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    sql = "UPDATE post SET title='" + \
        str(title)+"', type='"+str(type)+"', detail='" + \
        str(detail)+"' WHERE post_ID = "+post_ID
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "thanh cong", 200


@app.route("/api/showbytype/<int:id>")
def showbyType(id):
    if id == 1:
        type = 'Cho Thuê'
    elif id == 2:
        type = 'Tìm Phòng'
    elif id == 3:
        type = 'Ở Ghép'
    elif id == 4:
        type = 'Căn Hộ'
    elif id == 5:
        type = 'Khác'
    Posts = PostAcction(connection_data)
    result = Posts.showbytype(type)
    return jsonify(result)


@app.route('/api/deletecomment/<int:id>')
def delete(id):
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    sql = "DELETE FROM comment WHERE comment_ID='"+str(id)+"'"
    cur.execute(sql)
    conn.commit()
    conn.close()
    return "thanh cong", 200


@app.route('/api/search/<string:value>')
def search(value):
    Posts = PostAcction(connection_data)
    rs = Posts.search(value)
    return jsonify(rs)


@app.route('/api/report/<int:id>')
def report(id):
    print("id report: "+str(id))
    return "thanh cong ", 200


@app.route('/api/like/<int:id>')
def like(id):
    conn = sqlite3.connect(connection_data)
    cur = conn.cursor()
    cur.execute("SELECT * FROM comment WHERE comment_ID='"+str(id)+"'")
    for row in cur:
        point = int(row[5])
        point += 1
    cur.execute("UPDATE comment SET point ='"+str(point) +
                "' WHERE comment_ID='"+str(id)+"'")
    conn.commit()
    conn.close()
    return "ok", 200


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=5000)
