from flask import Flask, render_template, flash, request, send_file
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
import thread


# App config.
DEBUG = True
app = Flask(__name__)
# app.config.from_object(__name__,template_folder='./')
# app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    Src = TextField('Src:\t(lon,lat)\t', validators=[validators.required()])
    Dest = TextField('Dest:\t(lon,lat)\t', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    print form.errors
    if request.method == 'POST':
        if request.form['btn'] == 'Randomise traffic':
            os.system("python /home/ubuntu/NewYork/map/utils/net_to_json.py")
            flash("Done !")
            return render_template('main_map.html', form=form)
        elif request.form['btn'] == "Hotspots":
            return render_template('hotSpot.html')

        Src = request.form['Src'].strip('').split(',')
        Dest = request.form['Dest'].strip('').split(',')
        Src = Src[0]+' '+Src[1]
        Dest = Dest[0]+' '+Dest[1]
        print(Src,Dest)
        argv_ = Src +" "+ Dest
        # Src = Src.strip()
        # Dest = Dest.strip()
        # print from_edge
        if Src == "" or Dest == "":
            flash("Src Dest cannot be blank !")
            return render_template('main_map.html', form=form)
        # for  i  in xrange(1,10):
        print(argv_)
        table_gen=open("/home/ubuntu/NewYork/map/tables/table_input","w")
        table_gen.write("0")
        table_gen.close()

        os.system("python /home/ubuntu/NewYork/map/utils/latlon_edge_id.py "+argv_+" >/home/ubuntu/NewYork/map/tables/path_input")
        
        path_gen=open("/home/ubuntu/NewYork/map/tables/path_input","r")
        for  i  in xrange(1,10):
            print(path_gen.readlines())
        # path_gen.write(from_edge+"\n")
        # path_gen.write(to_edge+"\n")
        # path_gen.close()
        flash("Please wait...")
 
        os.system("python /home/ubuntu/NewYork/map/sumo/table_gen.py < /home/ubuntu/NewYork/map/tables/table_input")
        try:
            # os.system('killall firefox')
            print"path_predict"
            os.system("python /home/ubuntu/NewYork/map/utils/path_predict.py < /home/ubuntu/NewYork/map/tables/path_input")
            print "get_lat_lon"
            os.system("python /home/ubuntu/NewYork/map/utils/get_lat_lon.py")
            print "display_map"
            os.system("python /home/ubuntu/NewYork/map/utils/display_map.py")
            # os.system('cp home/ubuntu/Desktop/trajectory_clone/_map.html home/ubuntu/Desktop/trajectory_clone/templates/_map.html')
            # os.system("killall firefox")
            # if os.path.exists("_map.html"):
            #   for i in range(89):
            #       print  "yes"
            #   os.system("cp home/ubuntu/NewYork/map/_map.html home/ubuntu/NewYork/map/templates/_map.html")
            return render_template("_map.html")
            return send_file("home/ubuntu/NewYork/map/tables/out_path_lat_lon", attachment_filename='path.txt')
        except:
            flash("Path not found!")

        # if form.validate():
        #     # Save the comment here.
        #     flash('Hello ' + name)
        # else:
        #     flash('All the form fields are required. ')
 
    return render_template('main_map.html', form=form)

@app.route('/return-files/')
def return_files_tut():
    try:
        return send_file('home/ubuntu/NewYork/map/tables/out.json', attachment_filename='JSON_output.json')
    except Exception as e:
        return str(e)

@app.route('/traffic_gen/')
def traffic_new():
    print ("Randomizing Traffic..")
    flash("Please wait...")
    os.system("python home/ubuntu/NewYork/map/utils/net_to_json.py")
    flash("Done!")
 
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(host= '0.0.0.0', port=80)
