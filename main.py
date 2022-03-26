from ast import Return
from urllib.request import urlopen
from flask import *
from requests import get, post
import json, random, hashlib, base64, string, socket

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/api", methods=['GET', 'POST'])
def api():
    return render_template('api.html')

@app.route("/api/", methods=['GET', 'POST'])
def api1():
    return render_template('api.html')

@app.errorhandler(404)
def notfound(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internalerr(e):
    return render_template('500.html'), 500

@app.route("/api/spamcall", methods=['GET', 'POST'])
def spam_call():
    if request.args.get('no'):
        no = request.args.get('no')
        if str(no).startswith('8'):
            hasil = ''
            exec = post('https://id.jagreward.com/member/verify-mobile/'+no).json()
            if exec['result'] == 1:
                hasil = "[!] Spam Berhasil"
                status = 200
            else:
                hasil = "[!] Spam Gagal"
                status = False
            return {
                "status": status,
                "message": hasil
            }
        else:
            return {
                "status": False,
                "message": "[!] Tolong masukkan nomor awalan 8"
            }
    else:
        return {
            "status": False,
            "message": "[!] Tolong masukkan parameter no"
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
                "status": 200,
                "message": "Web "+cj+" Vuln Clickjacking"
            }
        elif not status: 
            return {
                "status": False,
                "message": "Web "+cj+" Not Vuln Clickjacking"
            }
        else:
            return {
                "status": False,
                "message": "unknow error"
            }
    else:
        return {
            "status": False,
            "message": "[!] Tolong masukkan parameter cj"
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
                "status": 200,
                "message": "CMS Found, CMS = OPenCarte"
            }
        elif "Joomla" in cmsjoomla.text:
            return {
                "status": 200,
                "message": "CMS Found, CMS = Joomla"
            }
        elif "WordPress" in cmswp.text:
            return {
                "status": 200,
                "message": "CMS Found, CMS = WordPress"
            }
        elif "sites/default" in cmsdrupal.text:
            return {
                "status": 200,
                "message": "CMS Found, CMS = Drupal"
            }
        else:
            return {
                "status": False,
                "message": "CMS Not Found, url = "+url
            }
    else:
        return {
            "status": False,
            "message": "Masukkan parameter c"
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
                "status": 200,
                "message": ipdata[0]['slug']
            }
            return data
    else:
        return {
            "status": 200,
            "message": "Masukkan parameter u"
        }

@app.route("/api/randomquotes")
def random_quote():
    sl = json.loads(open('quotes.json','r').read())
    js = random.choice(sl)
    return {
        "author": js["nama"],
        "quote": js["quote"]
    }

@app.route("/api/main", methods=['GET', 'POST'])
def gbk():
    if request.args.get('m'):
        otak = ['gunting','batu','kertas']
        encer = request.args.get('m')
        mesin = random.choice(otak)
        if encer == 'gunting' and mesin == 'batu':
            return {
                "status": 1,
                "bot": mesin,
                "message": "[X] HAHAHAHA Kamu Kalah!"
            }
        elif encer == 'batu' and mesin == 'kertas':
            return {
                "status": 1,
                "bot": mesin,
                "message": "[X] HAHAHAHA Kamu Kalah!"
            }
        elif encer == 'kertas' and mesin == 'gunting':
            return {
                "status": 1,
                "bot": mesin,
                "message": "[X] HAHAHAHA Kamu Kalah!"
            }
        elif encer == 'gunting' and mesin == 'kertas':
            return {
                "status": 2,
                "bot": mesin,
                "message": "[+] Hore kamu menang!"
            }
        elif encer == 'batu' and mesin == 'gunting':
            return {
                "status": 2,
                "bot": mesin,
                "message": "[+] Hore kamu menang!"
            }
        elif encer == 'kertas' and mesin == 'batu':
            return {
                "status": 2,
                "bot": mesin,
                "message": "[+] Hore kamu menang!"
            }
        elif encer == 'gunting' and mesin == 'gunting':
            return {
                "status": 0,
                "bot": mesin,
                "message": "[=] Wah Kita Sama!"
            }
        elif encer == 'batu' and mesin == 'batu':
            return {
                "status": 0,
                "bot": mesin,
                "message": "[=] Wah Kita Sama!"
            }
        elif encer == 'kertas' and mesin == 'kertas':
            return {
                "status": 0,
                "bot": mesin,
                "message": "[=] Wah Kita Sama!"
            }
    else:
        return {
            "status": False,
            "message": "Masukkan parameter m"
        }

@app.route("/api/passgenerator", methods=['GET', 'POST'])
def password_generator():
    if request.args.get('p'):
        text = request.args.get("p")
        sha1 = hashlib.sha1()
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        sha384 = hashlib.sha384()
        sha512 = hashlib.sha512()

        sha1.update(text.encode("utf-8"))
        md5.update(text.encode("utf-8"))
        sha256.update(text.encode("utf-8"))
        sha384.update(text.encode("utf-8"))
        sha512.update(text.encode("utf-8"))
        
        psha1 = sha1.hexdigest()
        pmd5 = md5.hexdigest()
        psha25 = sha256.hexdigest()
        psha384 = sha384.hexdigest()
        psha512 = sha512.hexdigest()

        return{
            "status": 200,
            "sha1": psha1,
            "md5": pmd5,
            "sha25": psha25,
            "sha384": psha384,
            "sha512": psha512,
            "message": "Password generator berhasil"
        }
    else:
        return {
            "status": False,
            "message": "Masukkan parameter p"
        }

@app.route("/api/b64", methods=['GET', 'POST'])
def b64encdec():
    if request.args.get('enc'):
        sample_string = request.args.get("enc")
        sample_string_bytes = sample_string.encode("ascii")
        
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return {
            "status": 200,
            "message": "Berhasil encode",
            "b64enc": base64_string
        }
    elif request.args.get('dec'):
        sample_string = request.args.get("dec")
        sample_string_bytes = sample_string.encode("ascii")
        
        base64_bytes = base64.b64decode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return {
            "status": 200,
            "message": "Berhasil encode",
            "b64dec": base64_string
        }
    else:
        return {
            "status": False,
            "message": "Masukkan parameter enc atau dec"
        }

@app.route('/api/iphost', methods=['GET', 'POST'])
def getIP():
    if request.args.get('ip'):
        host = request.args.get('ip')
        ip = socket.gethostbyname(host)
        return {
            "status": 200,
            "iphost": ip,
            "message": "berhasil"
        }
    else:
        return {
            "status": False,
            "message": "Masukkan parameter ip"
        }

@app.route('/api/md5crack', methods=['GET', 'POST'])
def md5crack():
    if request.args.get('md5'):
        md5_c = request.args.get("md5")
        pwd = open("mdpass.txt", 'r')
        for password in pwd:
            md5 = hashlib.md5()
            md5.update(password.strip().encode('utf-8'))
            if md5_c.strip() == md5.hexdigest():
                return {
                    "status": 200,
                    "password": password.strip(),
                    "message": "Password Ditemukan"
                }
        else:
            return {
                    "status": False,
                    "password": "",
                    "message": "Password Tidak ditemukan"
                }
    else:
        return {
            "status": False,
            "message": "masukkan parameter md5"
        }

@app.route('/api/adfind', methods=['GET', 'POST'])
def admninfind():
    if request.args.get('af'):
        url = request.args.get("af")
        file = open("admin.txt", "r")	
        try:
            for link in file.read().splitlines():
                curl = url + link
                res = get(curl)
                if 'login' in res.text or 'Login' in res.text or 'LogIn' in res.text and res.status_code == 200:
                    return {
                        "status": 200,
                        "admin": curl,
                        "message": "Panel Admin Berhasil ditemukan"
                    }
            else:
                return {
                        "status": False,
                        "admin": "",
                        "message": "Panel Admin Gagal ditemukan"
                    }
        
        except KeyboardInterrupt:
            return {
                "status": False,
                "message": "Shotdown Requests"
            }
        except:
            return {
                "status": False,
                "message": "Unknow Error"
            }
    else:
        return {
            "status": False,
            "message": "masukkan parameter af"
        }

if __name__ == "__main__":
    app.run()
