from app import app
from flask import render_template
# Userdetails for base.html
user = {'username':'Taansh'}

# Feature list to enumerate all the features being provided right now
features = [
    {
	    'name' : 'IP Address',
	    'Desc' : "Display the IP address of the raspberry pi"
    },
]
@app.route('/get_ip_addr')
def get_ip_addr():
    import subprocess
    ip_addr = None
    o = subprocess.run(["hostname","-I"], capture_output=True)
    if (o.returncode==0):
    	ip_addr = o.stdout
    return render_template('functions.html', title="Diptanshu's", user = user, ip_addr = ip_addr)

@app.route('/')
def index():
    return render_template('functions.html', title="Diptanshu's", user = user, features = features)
