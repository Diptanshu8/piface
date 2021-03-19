from app import app
from flask import render_template, jsonify, make_response, request
from app import logger
import traceback
import os,subprocess
import psutil as ps
import time

# Constants
NAS_MNT_POINT = "/home/pi/Taansh_HD"
DELGW_CONF = "/home/pi/.conf/deluge/web.conf"
NAS_MNT_CMD = ["sudo","mount.cifs","-vvv","//192.168.1.1/DJ","/home/pi/Taansh_HD/", "-o", "guest,vers=1.0"]
DELGD_CMD = ["deluged"]
DELGW_CMD = ["deluge-web","-f"]
SYNCTHING_CMD = "screen -s /bin/bash -d -m syncthing -logfile ~/syncthing.log"
MMM_START = "sudo systemctl start magicmirror"
MMM_STATUS = "sudo systemctl status magicmirror"
MMM_STOP = "sudo systemctl stop magicmirror"
RETROPIE_LAUNCH_CMD = 'screen -s /bin/bash -d -m emulationstation'

# Userdetails for base.html
user = {'username':'Skrill'}

@app.route('/get_ip_addr')
def get_ip_addr():
    ip_addr = None
    o = subprocess.run(["hostname","-I"], capture_output=True)
    ip_addr = o.stdout.decode("utf-8")
    if (o.returncode==0):
        return make_response(jsonify(ip_addr), 200);
    else:
        return make_response(jsonify(ip_addr), 500);

@app.route('/nas_mount_status')
def nas_mount_status():
    mount_status = os.path.ismount(NAS_MNT_POINT)
    if not mount_status:
        subprocess.run(NAS_MNT_CMD, capture_output=True) 
        mount_status = os.path.ismount(NAS_MNT_POINT)
    return jsonify(os.path.ismount(NAS_MNT_POINT))
    
@app.route('/deluge_status')
def deluge_status():
    d_status = "Disabled"
    d_web_status = "Disabled"
    pidlist = [(p.pid, p.name()) for p in ps.process_iter()]
    for p in pidlist:
        if "deluged" in p[1]:
            d_status = "Enabled"
        if "deluge-web" in p[1]:
            d_web_status = "Enabled"

    if (d_status == "Disabled"):
        try:
            subprocess.run(DELGD_CMD)
        except subprocess.CalledProcessError as e:
            return make_response(jsonify(e), 500)
    if (d_web_status == "Disabled"):
        try:
            subprocess.run(DELGW_CMD)
            # Mandatory delay for deluge web to start 
            time.sleep(2)
        except subprocess.CalledProcessError as e:
            return make_response(jsonify(e), 500)
    pidlist = [(p.pid, p.name()) for p in ps.process_iter()]
    for p in pidlist:
        if "deluged" in p[1]:
            d_status = "Enabled"
        if "deluge-web" in p[1]:
            d_web_status = "Enabled"
    if d_status == d_web_status =="Enabled":
        return make_response(jsonify(d_status), 200)
    return make_response(jsonify(d_status), 500)

@app.route('/syncthing_status')
def syncthing_status():
    status = "Disabled"
    pidlist = [(p.pid, p.name()) for p in ps.process_iter()]
    for p in pidlist:
        if "syncthing" in p[1]:
            status = "Enabled"
            return make_response(jsonify(status), 200)

    if (status == "Disabled"):
        os.system(SYNCTHING_CMD)
        time.sleep(2)

    pidlist = [(p.pid, p.name()) for p in ps.process_iter()]
    for p in pidlist:
        if "syncthing" in p[1]:
            status = "Enabled"
            return make_response(jsonify(status), 200)

    return make_response(jsonify(status), 500)

@app.route('/display_up')
def display_up():
    os.system("startx")
    return make_response(jsonify("Power Up the Pixel Desktop"), 200)

@app.route('/magicmirror_start')
def magicmirror_start():
    status = "Disabled"
    ret_code = os.system(MMM_STATUS)
    if ret_code == 0:       # on the basis of retcode of systemctl
        status = "Enabled"

    if (status == "Disabled"):
        os.system(MMM_START)
        time.sleep(2)

        ret_code = os.system(MMM_STATUS)
        if ret_code == 0:
            status = "Enabled"
        else:
            return make_response(jsonify(status), 500)
    return make_response(jsonify(status), 200)

@app.route('/magicmirror_stop')
def magicmirror_stop():
    status = "Enabled"
    ret_code = os.system(MMM_STATUS)
    if ret_code == 768:         # on the basis of retcode of systemctl
        status = "Disabled"

    if (status == "Enabled"):
        os.system(MMM_STOP)

        ret_code = os.system(MMM_STATUS)
        if ret_code == 768:
            status = "Disabled"
        else:
            return make_response(jsonify(status), 500)
    return make_response(jsonify(status), 200)

@app.route('/launch_retropie')
def launch_retropie():
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
    os.system("sudo shutdown -r now")
    return make_response(jsonify("Rebooting..."), 200)

@app.route('/settings')
def settings():
    return render_template('settings.html', title="DJPI's Piface Settings", user = user)

@app.route('/')
def index():
    return render_template('functions.html', title="DJPI's Piface", user = user)

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

