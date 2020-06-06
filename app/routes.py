from app import app
from flask import render_template, jsonify, make_response, request
from app import logger
import traceback

# Constants
NAS_MNT_POINT = "/home/pi/Taansh_HD"
DELGW_CONF = "/home/pi/.conf/deluge/web.conf"
NAS_MNT_CMD = ["sudo","mount.cifs","-vvv","//192.168.1.1/DJ","/home/pi/Taansh_HD/", "-o", "guest,vers=1.0"]
DELGD_CMD = ["deluged"]
DELGW_CMD = ["deluge-web","-f"]
RETROPIE_LAUNCH_CMD = 'screen -s /bin/bash -d -m emulationstation'

# Userdetails for base.html
user = {'username':'Taansh'}

@app.route('/get_ip_addr')
def get_ip_addr():
    import subprocess
    ip_addr = None
    o = subprocess.run(["hostname","-I"], capture_output=True)
    ip_addr = o.stdout.decode("utf-8")
    if (o.returncode==0):
        return make_response(jsonify(ip_addr), 200);
    else:
        return make_response(jsonify(ip_addr), 500);


@app.route('/nas_mount_status')
def nas_mount_status():
    import os,subprocess
    mount_status = os.path.ismount(NAS_MNT_POINT)
    if not mount_status:
        subprocess.run(NAS_MNT_CMD, capture_output=True) 
        mount_status = os.path.ismount(NAS_MNT_POINT)
    return jsonify(os.path.ismount(NAS_MNT_POINT))
    
@app.route('/deluge_status')
def deluge_status():
    import psutil as ps
    import subprocess
    d_status = "Disabled"
    pidlist = [(p.pid, p.name()) for p in ps.process_iter()]
    for p in pidlist:
        if "deluged" in p[1]:
            d_status = "Enabled"

    if (d_status == "Disabled"):
        try:
            subprocess.run(DELGD_CMD)
        except subprocess.CalledProcessError as e:
            return make_response(jsonify(e), 500)

    pidlist = [(p.pid, p.name()) for p in ps.process_iter()]
    for p in pidlist:
        if "deluged" in p[1]:
            d_status = "Enabled"
    return make_response(jsonify(d_status), 200)

@app.route('/delugeweb_status')
def delugeweb_status():
    import psutil as ps
    import subprocess
    d_status = "Disabled"
    pidlist = [(p.pid, p.name()) for p in ps.process_iter()]
    for p in pidlist:
        if "deluge-web" in p[1]:
            d_status = "Enabled"

    if (d_status == "Disabled"):
        try:
            subprocess.run(DELGW_CMD)
        except subprocess.CalledProcessError as e:
            return make_response(jsonify(e), 500)

    pidlist = [(p.pid, p.name()) for p in ps.process_iter()]
    for p in pidlist:
        if "deluge-web" in p[1]:
            d_status = "Enabled"

    return make_response(jsonify(d_status), 200)

@app.route('/launch_retropie')
def launch_retropie():
    import psutil as ps
    import os
    status = "Disabled"
    pidlist = [(p.pid, p.name()) for p in ps.process_iter()]
    for p in pidlist:
        if "emulation" in p[1]:
            status = "Enabled"

    if (status == "Disabled"):
        os.system(RETROPIE_LAUNCH_CMD)
        status = "Enabled"
    return make_response(jsonify(status), 200)

@app.route('/reboot')
def reboot():
    import os
    os.system("sudo shutdown -r now")
    return make_response(jsonify("Rebooting..."), 200)

@app.route('/')
def index():
    return render_template('functions.html', title="Diptanshu's", user = user)

@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        logger.app_log.info('%s %s %s %s %s',
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response

@app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every Exception. """
    tb = traceback.format_exc()
    logger.app_log.error('5xx INTERNAL SERVER ERROR\n%s',
                  tb)
    return "Internal Server Error", 500

# command to kill emulationstation
# ps -ef | awk '/emulation/ {print $2}' | xargs kill
#

