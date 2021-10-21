from flask import Flask, render_template, request
app = Flask(__name__)

import psycopg2

hostname = '127.0.0.1'
database = 'NGO'
username = 'postgres'
pwd = 'bishal@123'
port_id = 5432
conn = None
cur = None
try :
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    print("HELLO")
    cur = conn.cursor() 
    view_table = '''select * from Food_LOG order by id'''
    cur.execute(view_table)
    arrtup = cur.fetchall() 
    conn.commit()   
    @app.route("/") 
    def func() : 
        return render_template("home.html") 
    
    @app.route("/view") 
    def funtu() : 
        view_table = '''select * from Food_LOG order by id'''
        cur.execute(view_table)
        return render_template("view.html",list = cur.fetchall())    
    
    @app.route("/donate") 
    def funtua() :  
        view_table = '''select * from Food_LOG order by id'''
        cur.execute(view_table)
        return render_template("donate.html",list = cur.fetchall())

    @app.route("/donate", methods = ["POST"]) 
    def fucr() : 
        print("HELLO....")
        a = 0
        b = 'Visnu' 
        c = 500000
        a = int(request.form['no'])
        b = request.form['name'] 
        c = int(request.form['quant'])  
        view_table = '''select * from Food_LOG order by id'''
        cur.execute(view_table) 
        arr = (len(cur.fetchall())+1,b,c) 
        conn.commit()
        view_table = '''select * from Food_LOG order by id'''
        cur.execute(view_table)
        if(a==0 or len(cur.fetchall())==0) : 
            #arrtup.append(arr)  
            
            cur.execute('''insert into Food_LOG values(%s,%s,%s)''',arr) 
        else :
            view_table = '''select * from Food_LOG order by id'''
            cur.execute(view_table)
            cur.execute('''update Food_LOG set quantity_in_kg = {} where id = {}'''.format(cur.fetchall()[a-1][2]+c,a))
        conn.commit() 
        view_table = '''select * from Food_LOG order by id'''
        cur.execute(view_table)
        #arrtup = cur.fetchall() 
        return render_template("donate.html",list = cur.fetchall())

    @app.route("/request") 
    def funtuareq() :  
        view_table = '''select * from Food_LOG order by id'''
        cur.execute(view_table)
        return render_template("request.html",list = cur.fetchall())

    @app.route("/request", methods = ["POST"]) 
    def Reqfucr() : 
        print("HELLO....")
        a = 0
        b = 'Visnu' 
        c = 500000
        a = int(request.form['no'])
        b = request.form['name'] 
        c = int(request.form['quant'])   
        view_table = '''select * from Food_LOG order by id'''
        cur.execute(view_table)
        lstar = cur.fetchall()
        if(a>0 and a<=len(lstar)) :
            qutn = lstar[a-1][2] - c 
        
        if(qutn<=0) :
                view_table = '''select * from Food_LOG order by id'''
                cur.execute(view_table)
                #lstar = cur.fetchall()  
                #print(cur.fetchall()[a][1])   
                cur.execute('''delete from Food_LOG where id = {}'''.format(a))
                conn.commit()
                #cur.execute('''delete from Food_LOG where id = {}'''.format(a))
                #conn.commit()
                #cur.execute('''update Food_LOG set id = id -1 where id > {}'''.format(a))
                #conn.commit()
        else :
            cur.execute('''update Food_LOG set quantity_in_kg = {} where id = {}'''.format(qutn,a))
            conn.commit() 
        fa = 0
        view_table = '''select * from Food_LOG order by id'''
        cur.execute(view_table)
        c = 0
        for tupu in cur.fetchall() : 
            c+=1
            if(tupu[0]>c) :  
                cur.execute('''update Food_LOG set id = {} where id = {}'''.format(c,tupu[0])) 
                conn.commit()   
        #cur.execute('''update Food_LOG set id = id -1 where id >= {}'''.format(fa))
        #conn.commit()
        view_table = '''select * from Food_LOG order by id'''
        cur.execute(view_table)
        return render_template("request.html",list = cur.fetchall())  

#Start from here today
    @app.route("/donate_signin") 
    def donators_sign_in() :  
        return render_template("donate_sign_in.html", xman = "",lnk = "")
    
    @app.route("/donate_signin", methods = ["POST"]) 
    def donators_sign_in_again() :  
        eml = str(request.form['email']).lower() 
        paswd = request.form['password']  
        cur.execute('''select * from donetor''')
        don_passwd = cur.fetchall() 
        xm = "invalid password or email please refill it again"
        ln = "" 
        for tup in don_passwd :
            if(tup[1]==eml) :
                if(tup[4]==paswd) :
                    xm = "SUCESS, now please click on the below link"
                    ln = "Donators section" 
                    break  
                  
        return render_template("donate_sign_in.html", xman = xm, lnk = ln)

#Second means request
    @app.route("/request_signin") 
    def requesters_sign_in() :  
        return render_template("request_sign_in.html", xman = "",lnk = "",lnk2 = "")
    
    @app.route("/request_signin", methods = ["POST"]) 
    def requesters_sign_in_again() :  
        eml = str(request.form['email']).lower() 
        paswd = request.form['password'] 
        cur.execute('''select * from requester''')
        don_passwd = cur.fetchall()  
        xm = "invalid password or email please refill it again"  
        ln = "" 
        ln2 = ""  
        for tup in don_passwd :
            if(tup[1]==eml) : 
                if(tup[4]==paswd) :
                    xm = "SUCESS, now please click any of the below link as per your choise" 
                    ln = "Requesters section"
                    ln2 = "View food items"
                    break 
                  
        return render_template("request_sign_in.html", xman = xm, lnk = ln, lnk2 = ln2)

    @app.route("/donate_signUP") 
    def donetors_sign_up() :  
        return render_template("donate_sign_UP.html", txt = "")   

    @app.route("/donate_signUP", methods = ["POST"]) 
    def donators_sign_up_again() :  
        nam = str(request.form['name'] )
        eml = str(request.form['email']).lower() 
        inst = str(request.form['inst_name'])
        adres = str(request.form['adress'])
        paswd = str(request.form['password'])  
        tx = "Thankyou for Signing UP now please go back and singIn to acess your priviledges" 
        cur.execute('''select * from donetor''')
        don_passwd = cur.fetchall()  
        conn.commit() 
        bulabis = True 
        for tup in don_passwd :
            if(tup[1]==eml) : 
                tx = "Sorry emailId already exists please try another one" 
                bulabis = False 
                break

        if bulabis :
            tuplu = (nam,eml,inst,adres,paswd)   
            cur.execute('''insert into donetor values(%s,%s,%s,%s,%s)''',tuplu) 
            conn.commit()
        
        return render_template("donate_sign_UP.html", txt = tx)   

#REQUESTers SIGN IN
    @app.route("/requesters_signUP") 
    def requester_sign_up() :  
        return render_template("request_sign_UP.html", txt = "")   

    @app.route("/requesters_signUP", methods = ["POST"]) 
    def requester_sign_up_again() :  
        nam = str(request.form['name'] )
        eml = str(request.form['email']).lower() 
        inst = str(request.form['inst_name'])
        adres = str(request.form['adress'])
        paswd = str(request.form['password'])  
        tx = "Thankyou for Signing UP now please go back and singIn to acess your priviledges" 
        cur.execute('''select * from requester''')
        don_passwd = cur.fetchall()  
        conn.commit() 
        bulabis = True 
        for tup in don_passwd :
            if(tup[1]==eml) : 
                tx = "Sorry emailId already exists please try another one" 
                bulabis = False 
                break

        if bulabis :
            tuplu = (nam,eml,inst,adres,paswd)   
            cur.execute('''insert into requester values(%s,%s,%s,%s,%s)''',tuplu) 
            conn.commit()
        
        return render_template("request_sign_UP.html", txt = tx)   


    if __name__ == "__main__" : 
        app.run(debug=True)  
    #truncate_table = '''truncate table emp'''
    #cur.execute(truncate_table)
except Exception as error:
    print('Contains Error! '+str(error)) 
finally : 
    if cur is not None : 
        cur.close()
    if conn is not None : 
        conn.close()




