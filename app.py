from flask import *
from datetime import timedelta
import codecs
import re
import os
from waitress import serve

app = Flask(__name__)

app.secret_key = '--- secret key ---'
app.permanent_session_lifetime = timedelta(minutes=5)

def containsFlag(candidate):
    pattern = re.compile('.*<[Ss][Cc][Rr][Ii][Pp][Tt]>[\s]*alert([\s]*[\'\"]*.*[\'\"]*[\s]*);[\s]*</[Ss][Cc][Rr][Ii][Pp][Tt]>.*')
    if pattern.match(candidate) is None:
        return False
    else :
        return True    

def containsFlagEx(candidate):
    pattern = re.compile('.*\'[\s]*>[\s]*<[Ss][Cc][Rr][Ii][Pp][Tt]>[\s]*alert([\s]*[\'\"]*.*[\'\"]*[\s]*);[\s]*</[Ss][Cc][Rr][Ii][Pp][Tt]>.*')
    if pattern.match(candidate) is None:
        return False
    else :
        return True    

'''''''''''''''''
'/' GET request 
'''''''''''''''''
@app.route('/')
def index():
    if "pcid" not in session: #端末ID未設定
        return redirect('/initpc')
    pcid = session['pcid']    

    try:
        with codecs.open('data/'+pcid+'.json', 'r', 'utf-8') as f:
            terminalData = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return redirect('/initpc')

    if terminalData['nickname'] == '' : #端末ID未設定
        return redirect('/pledge')

    if request.args.get('p') is not None:   
        terminalData['currentpg'] = int(request.args.get('p'))

    if request.args.get('h') is not None:   
        terminalData['hinted'][int(request.args.get('h'))] = 1

    #端末用JSONデータファイル出力
    with codecs.open('data/'+pcid+'.json', 'w', 'utf-8') as f:
        json.dump(terminalData, f, indent=2, ensure_ascii=False)

    comments = []

    try:
        with codecs.open('data/com_'+pcid+'_'+str(terminalData['currentpg'])+'.json', 'r', 'utf-8') as f:
            comments = json.load(f)
    except FileNotFoundError as e:
        print(e)

    return render_template("main.html", current = terminalData, pgComments = comments)


###################################################
# 講師用機能 
###################################################
@app.route('/monitor')
def monitor():
    files = os.listdir("data")
    myfile = 'filename.txt'
    pattern = re.compile('com_.*.json')
    patternMd = re.compile('.*.md')

    current = []
    for filename in files:
        if patternMd.match(filename) is not None:
            continue
        if pattern.match(filename) is None:
            print(filename)
            single = {}
            try:
                with codecs.open('data/'+filename, 'r', 'utf-8') as f:
                    single = json.load(f)
                    print(single)
                    single['pc'] = filename[0:-5]
            except FileNotFoundError as e:
                print(e)            
            current.insert(0, single)
            print('OK')
    return render_template("monitor.html", status = current)

###################################################
# アサイメントの送信データ処理 
###################################################
'''''''''''''''''
'/p8comment' POST request 
'''''''''''''''''
@app.route('/p8comment', methods=['POST'])
def p8comment():
    pcid = session['pcid']    

    try:
        with codecs.open('data/'+pcid+'.json', 'r', 'utf-8') as f:
            terminalData = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return redirect('/initpc')

    comments = []
    single = {}
    try:
        with codecs.open('data/com_'+pcid+'_8.json', 'r', 'utf-8') as f:
            comments = json.load(f)
    except FileNotFoundError as e:
        print(e)

    single['commenter'] = request.form['commenter']
    single['comment'] = request.form['comment']
    single['title'] = request.form['title']
    single['color'] = request.form['color']
    comments.insert(0, single)

    if terminalData['score'][8] == 0 :
        if containsFlagEx( single['color'] ) :
            terminalData['score'][8] = 2 - terminalData['hinted'][8]   

    #端末用JSONデータファイル出力
    with codecs.open('data/com_'+pcid+'_8.json', 'w', 'utf-8') as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

    #端末用JSONデータファイル出力
    with codecs.open('data/'+pcid+'.json', 'w', 'utf-8') as f:
        json.dump(terminalData, f, indent=2, ensure_ascii=False)

    return redirect('/')  


'''''''''''''''''
'/p7comment' POST request 
'''''''''''''''''
@app.route('/p7comment', methods=['POST'])
def p7comment():
    pcid = session['pcid']    

    try:
        with codecs.open('data/'+pcid+'.json', 'r', 'utf-8') as f:
            terminalData = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return redirect('/initpc')

    comments = []
    single = {}
    try:
        with codecs.open('data/com_'+pcid+'_7.json', 'r', 'utf-8') as f:
            comments = json.load(f)
    except FileNotFoundError as e:
        print(e)

    single['commenter'] = request.form['commenter']
    single['comment'] = request.form['comment']
    single['title'] = request.form['title']
    comments.insert(0, single)

    if terminalData['score'][7] == 0 :
        if containsFlag( single['commenter'] ) :
            terminalData['score'][7] = 2 - terminalData['hinted'][7]   

    #端末用JSONデータファイル出力
    with codecs.open('data/com_'+pcid+'_7.json', 'w', 'utf-8') as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

    #端末用JSONデータファイル出力
    with codecs.open('data/'+pcid+'.json', 'w', 'utf-8') as f:
        json.dump(terminalData, f, indent=2, ensure_ascii=False)

    return redirect('/')  


'''''''''''''''''
'/p6comment' POST request 
'''''''''''''''''
@app.route('/p6comment', methods=['POST'])
def p6comment():
    pcid = session['pcid']    

    try:
        with codecs.open('data/'+pcid+'.json', 'r', 'utf-8') as f:
            terminalData = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return redirect('/initpc')

    comments = []
    single = {}
    try:
        with codecs.open('data/com_'+pcid+'_6.json', 'r', 'utf-8') as f:
            comments = json.load(f)
    except FileNotFoundError as e:
        print(e)

    single['commenter'] = request.form['commenter']
    single['comment'] = request.form['comment']
    single['title'] = request.form['title']
    comments.insert(0, single)

    if terminalData['score'][6] == 0 :
        if containsFlag( single['comment'] ) :
            terminalData['score'][6] = 2 - terminalData['hinted'][6]   

    #端末用JSONデータファイル出力
    with codecs.open('data/com_'+pcid+'_6.json', 'w', 'utf-8') as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

    #端末用JSONデータファイル出力
    with codecs.open('data/'+pcid+'.json', 'w', 'utf-8') as f:
        json.dump(terminalData, f, indent=2, ensure_ascii=False)

    return redirect('/')  


###################################################
# トレーニングセッションの送信データ処理 
###################################################

'''''''''''''''''
'/p1comment' POST request 
'''''''''''''''''
@app.route('/p1comment', methods=['POST'])
def p1comment():
    pcid = session['pcid']    

    try:
        with codecs.open('data/'+pcid+'.json', 'r', 'utf-8') as f:
            terminalData = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return redirect('/initpc')

    comments = []
    single = {}
    try:
        with codecs.open('data/com_'+pcid+'_1.json', 'r', 'utf-8') as f:
            comments = json.load(f)
    except FileNotFoundError as e:
        print(e)

    single['commenter'] = request.form['commenter']
    single['comment'] = request.form['comment']
    comments.insert(0, single)

    if containsFlag( single['comment'] ) or  containsFlag( single['commenter'] ) :
        terminalData['score'][1] = 1;   

    #端末用JSONデータファイル出力
    with codecs.open('data/com_'+pcid+'_1.json', 'w', 'utf-8') as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

    #端末用JSONデータファイル出力
    with codecs.open('data/'+pcid+'.json', 'w', 'utf-8') as f:
        json.dump(terminalData, f, indent=2, ensure_ascii=False)

    return redirect('/')    

'''''''''''''''''
'/p3comment' POST request 
'''''''''''''''''
@app.route('/p3comment', methods=['POST'])
def p3comment():
    pcid = session['pcid']    

    try:
        with codecs.open('data/'+pcid+'.json', 'r', 'utf-8') as f:
            terminalData = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return redirect('/initpc')

    comments = []
    single = {}
    try:
        with codecs.open('data/com_'+pcid+'_3.json', 'r', 'utf-8') as f:
            comments = json.load(f)
    except FileNotFoundError as e:
        print(e)

    single['commenter'] = request.form['commenter']
    single['comment'] = request.form['comment']
    comments.insert(0, single)

    if containsFlag( single['commenter'] ) :
        terminalData['score'][3] = 1;   


    #端末用JSONデータファイル出力
    with codecs.open('data/com_'+pcid+'_3.json', 'w', 'utf-8') as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

    #端末用JSONデータファイル出力
    with codecs.open('data/'+pcid+'.json', 'w', 'utf-8') as f:
        json.dump(terminalData, f, indent=2, ensure_ascii=False)

    return redirect('/')    

'''''''''''''''''
'/p5comment' POST request 
'''''''''''''''''
@app.route('/p5comment', methods=['POST'])
def p5comment():
    pcid = session['pcid']    

    try:
        with codecs.open('data/'+pcid+'.json', 'r', 'utf-8') as f:
            terminalData = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return redirect('/initpc')

    comments = []
    single = {}
    try:
        with codecs.open('data/com_'+pcid+'_5.json', 'r', 'utf-8') as f:
            comments = json.load(f)
    except FileNotFoundError as e:
        print(e)

    single['commenter'] = request.form['commenter']
    single['comment'] = request.form['comment']
    single['evaluate'] = request.form['evaluate']
    comments.insert(0, single)

    print(single['evaluate'])
    if containsFlag( single['evaluate'] ) :
        terminalData['score'][5] = 1;   


    #端末用JSONデータファイル出力
    with codecs.open('data/com_'+pcid+'_5.json', 'w', 'utf-8') as f:
        json.dump(comments, f, indent=2, ensure_ascii=False)

    #端末用JSONデータファイル出力
    with codecs.open('data/'+pcid+'.json', 'w', 'utf-8') as f:
        json.dump(terminalData, f, indent=2, ensure_ascii=False)

    return redirect('/')    

###################################################
# 設定、登録関係のルート 
###################################################

'''''''''''''''''
' '/pledge' GET request 
'''''''''''''''''
@app.route('/pledge')
def pledge():
    if "pcid" not in session: #端末ID未設定
        return redirect('/initpc')
    return render_template("pledge.html")

'''''''''''''''''
'/pledged' POST request 
'''''''''''''''''
@app.route('/pledged', methods=['POST'])
def pledged():
    if "pcid" not in session: #端末ID未設定
        return redirect('/initpc')
    pcid = session['pcid']    

    nickname = request.form['nickname']

    try:
        with codecs.open('data/'+pcid+'.json', 'r', 'utf-8') as f:
            terminalData = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return redirect('/initpc')
        
    terminalData['nickname'] = nickname

    #端末用JSONデータファイル出力
    with codecs.open('data/'+pcid+'.json', 'w', 'utf-8') as f:
        json.dump(terminalData, f, indent=2, ensure_ascii=False)

    return redirect('/')

'''''''''''''''''
'/initpc' GET request 
'''''''''''''''''
@app.route('/initpc')
def initPc():
    session.clear()
    return render_template("initialize.html")

'''''''''''''''''
'/initialize' GET request 
'''''''''''''''''
@app.route('/initialize') 
def initialize():
    pcid = ""
    if request.args.get('pcid') is None:
        return redirect('/initpc')

    pcid = request.args.get('pcid')

    initialData = {}
    try:
        with codecs.open('data/'+pcid+'.json', 'r', 'utf-8') as f:
            initialData = json.load(f)
    except FileNotFoundError as e:
        #端末用JSONデータの初期値
        initialData = { "nickname": "", "currentpg": 0, "score": [0,0,0,0,0,0,0,0,0], "hinted":[0,0,0,0,0,0,0,0,0]}

    #端末用JSONデータファイル出力
    with codecs.open('data/'+pcid+'.json', 'w', 'utf-8') as f:
        json.dump(initialData, f, indent=2, ensure_ascii=False)

    #セッションで端末IDを管理
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=3)
    session["pcid"] = pcid        

    return redirect('/')

if __name__=='__main__':
    # app.run()
    serve(app, host='0.0.0.0', port=8080)
    