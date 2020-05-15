from app import app
from flask import render_template

# Constants
NAS_MNT_POINT = "/home/pi/Taansh_HD"
NAS_MNT_CMD = ["sudo","mount.cifs","-vvv","//192.168.1.1/DJ","/home/pi/Taansh_HD/", "-o", "guest,vers=1.0"]

# Userdetails for base.html
user = {'username':'Taansh'}

# Feature list to enumerate all the features being provided right now
features = [
    {
	    'name' : 'IP Address',
	    'Desc' : "Display the IP address of the raspberry pi"
    },
    {
            'name' : "NAS mount",
            'Desc' : "Displays status of NAS mount"
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

@app.route('/nas_mount_status')
def nas_mount_status():
    import os,subprocess
    mount_status = os.path.ismount(NAS_MNT_POINT)
    if not mount_status:
        subprocess.run(NAS_MNT_CMD, capture_output=True) 
        mount_status = os.path.ismount(NAS_MNT_POINT)

    return render_template('functions.html', title="Diptanshu's", user = user, mount_status = os.path.ismount(NAS_MNT_POINT))
    
@app.route('/deluge_status')
def deluge_status():
    import psutil as ps
    d_status = "Disabled"
    pidlist = [(p.pid, p.name()) for p in ps.process_iter()]
    for p in pidlist:
        if "deluge" in p[1]:
            d_status = "Enabled"
    print("Inside deluge_status for d_status = "+ d_status)
    return render_template('functions.html', title="Diptanshu's", user = user, d_status = d_status)

@app.route('/')
def index():
    return render_template('functions.html', title="Diptanshu's", user = user, features = features)
