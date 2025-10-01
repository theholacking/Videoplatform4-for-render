import os
from flask import Flask,render_template,request,session,jsonify,redirect,url_for
from flask_mysqldb import MySQL
import boto3 
from botocore.config import Config
from werkzeug.utils import secure_filename
import mimetypes
from dotenv import load_dotenv
from flask_cors import CORS
from flask_bcrypt import Bcrypt


#load
load_dotenv()


app= Flask(__name__)
CORS(app)
#===========configs =======#
uploadfolder='static/video_folder'
app.config['UPLOAD_FOLDER'] = 'uploadfolder'
app.secret_key='shahwah'
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_PORT'] = int(os.getenv("MYSQL_PORT"))
app.config['MYSQL_SSL_CA'] =os.path.join(os.getcwd(), "certs/ca.pem")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
mysql=MySQL(app)

#===========r2 configs=======#

r2 = boto3.client(
    "s3",
    endpoint_url=os.getenv("R2_ENDPOINT"),
    aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
    config=Config(signature_version="s3v4")
)


bucket=os.getenv("R2_BUCKET")
#===========AUTH ROUTES =======#

@app.route('/')
@app.route('/home')
def home():
    session.clear()
    return render_template('register.html')


''' registering a new user '''  
@app.route('/register', methods=["POST"])
def registration():
    session.clear()
    cur=mysql.connection.cursor()
    data=request.get_json()
    username=data.get('username')
    passhash=data.get('passhash')
    email=data.get('email')
    cur.execute("insert into users (username ,email ,passhash) values(%s,%s,%s)",(username,email,passhash))
    mysql.connection.commit()
    user=cur.rowcount
    cur.close()
    
    if user > 0 :
        return jsonify({"Succes":"True","xanta":"Sadaqo laguugu diiwaan galiyay 😁😂🤣"})
    else:
        return jsonify({"Succes":"False","xanta":"Sadaqo xitaa waa laguugu diiwaan galin waayay 😁😂🤣"}),401

    


'''login check for registered'''
@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def soogalid():
    session.get('username')==False
    session.clear()
    cur=mysql.connection.cursor()
    data=request.get_json()
    username=data.get('username')
    passhash=data.get('passhash')
    cur.execute("select * from users where username=%s and passhash=%s",(username,passhash))
    user=cur.fetchone()
    cur.close()

    if user:
        session['user_id']=user[0]
        session['username']=username
        print(session['username'],'has entered the house')
        return jsonify({"succes":"True","xanta":"login succesful🥱😁😄😤"})
    else:
         return jsonify({"succes":"False","xanta":"beenta jooji"}),401
    

''' logging the user out '''

@app.route('/log_out')
def bananka():
    print(session['username'], 'wuu ka baxay meesha')
    session.clear()
    return redirect(url_for("home"))

#=========== VIDEO ROUTES =======#

'''display all videos'''
@app.route('/videos')
def allvideos():
    cur=mysql.connection.cursor()
    cur.execute("select id,title,descriptions from videos order by id desc")
    videos=cur.fetchall()
    cur.close()
    video_list=[]
    for vid in videos:
         file_name=vid[2]
         signed_url = r2.generate_presigned_url(
         "get_object",
         Params={"Bucket": bucket, "Key": file_name},
         ExpiresIn=3600  # 1 hour
          )
         video_list.append({"id":vid[0],"title":vid[1],"url":signed_url})
    
    '''
    markii hore shaxda all in one laga rabay
       cur.execute("select id,content,created_at from comments order by id desc")
    comments=cur.fetchall()
    ecomments=[]
    for all in comments:
        ecomments.append({"id":all[0],"comment":all[1],"time":all[2]}) 
       
    cur.execute("select count(content) from  comments")
    numofcomments=cur.fetchall()
    print(numofcomments)
    tirada=[]
    for number in numofcomments:
        tirada.append({"shaxda":number[0]}) #,(comments= ecomments , tirada= numofcomments)
    '''
    
    return render_template("allvideos.html",videos=video_list) 
    


''' first go to upload page'''
@app.route('/upload_page')
def preview():

    return render_template('upload.html')

'''upload a new video and preview'''
@app.route('/upload',methods=["POST"])
def upload():
        if "video" not in request.files:
         return jsonify({"cml":"see cml hee"}),400
        
        file = request.files["video"]
        title = request.form.get("title","untitled")
        userId=session.get('user_id')
        filename=secure_filename(file.filename)
        if file.filename == "":
            return "error Empty filename", 400

        mimetype, _ = mimetypes.guess_type(filename)
        #r2
        r2.upload_fileobj( file,
                          bucket,
                          filename,
                          ExtraArgs={"ContentType": mimetype or "application/octet-stream"})

        # #publi url oo la ogeen
        # # file_url=f"{os.getenv('R2_ENDPOINT')}/{bucket}/{filename}"




        #filesql
        cur=mysql.connection.cursor()
        cur.execute("insert into videos (user_id,title,descriptions) values(%s,%s,%s)",(userId,title,filename))
        mysql.connection.commit()
        cur.close()

        return jsonify({"xanaan": "damiinimo", "url": filename})
        # return jsonify({"message": "Upload successful", "url": file_url})

'''play a videos<id>'''
@app.route('/videos/<int:video_id>')
def playvideo(video_id):
    cur=mysql.connection.cursor()
    cur.execute("select id,title,descriptions from videos where id=%s ",(video_id,))
    videos=cur.fetchall()
    
    video_list=[]
    for vid in videos:
         file_name=vid[2]
         signed_url = r2.generate_presigned_url(
         "get_object",
         Params={"Bucket": bucket, "Key": file_name},
         ExpiresIn=3600  # 1 hour
          )
         video_list.append({"id":vid[0],"title":vid[1],"url":signed_url})


    cur.execute("select * from comments where video_id =%s ",(video_id,))
    comments = cur.fetchall()

    cur.execute("select count(*) from comments where video_id =%s ",(video_id,))
    comments_len, = cur.fetchone()

    cur.execute("select count(*) from likes where video_id =%s ",(video_id,))
    likes_len, = cur.fetchone()
       
    cur.close()
    comment_list = []
    for c in comments:
        co_id=c[0]  
        us_id=c[1]  
        vi_id=c[2]  
        
        comment_list.append({"content" :c[3],"timecreated":c[4]})  

    return render_template("play.html",videos=video_list, comment=comment_list,commentcount=comments_len ,total_likes =likes_len )


'''remove video and delete<id>'''
@app.route('/delete<id>')
def deletevideo():
    return 'deleted video'

#=========== dashboard  ROUTE =======#
@app.route('/dashboard')
def dashboard():
    return render_template("profile.html")
#=========== COMMENT AND LIKES ROUTES =======#

'''add videos/<id>/ comment'''
@app.route('/videos/<video_id>/addcomment',methods=["POST"])
def addcomment(video_id):
    cur=mysql.connection.cursor()
    data=request.get_json()
    content=data.get('comment')
    cur.execute("insert into comments (user_id,video_id,content) values (%s,%s,%s)",(session["user_id"],video_id,content))
    mysql.connection.commit()
    thenewcomment= cur.rowcount
    if thenewcomment > 0:
     return jsonify({"Succes":"xaaraan","qaanjeerta":"comment ku dhiigle tahy"})
    else:
        return jsonify({"Succes":"noioh", "qaanjeerta":"comment ku dhiigle iska dhigi rabtay lkn waa fashilantay"})

''' delete videos/<id>/comments   '''
@app.route('/delete<id>')
def deletecomment():
    return 'deleted video'

'''toggle videos<id>/like'''
@app.route('/videos/<video_id>/like_blue',methods=["POST"])
def like(video_id):
    cur=mysql.connection.cursor()
    cur.execute("insert into likes (user_id,video_id) values (%s,%s)",(session["user_id"],video_id))
    mysql.connection.commit()
    thenewcomment= cur.rowcount
    print(thenewcomment)
    if thenewcomment > 0:
     return jsonify({"Succes":"True","message":"you liked the video bro"})
    else:
        return jsonify({"Succes":"False","message":"maya laguuma baahna"})
    


if __name__=="__main__":
    app.run(debug=True,port=5050)
