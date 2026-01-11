import requests

ZONE_ID = "53c144d455d1d3d866e03f1de8f29c30"
API_TOKEN = "ltdoj1OTB37QcCp2BpWchMNR_pW9XUOqM84NHmAu"
CNAME = "spinardi.onthewifi.com"

HEADERS = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
        }

###--- WEB METHODS ---###

def get():
    url = (f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records")
    r = requests.get(url, headers=HEADERS)
    data = r.json()
    return data

def cpost(nombre):
    DATA= {
            "type": "CNAME",
            "name": f"{nombre}",
            "content": f"{CNAME}",
            "ttl": 3600,
            "proxied": False
            }

    url = (f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records")
    r = requests.post(url, headers=HEADERS, json=DATA)
    data = r.json()
    return data, r

def cdelete(record):
    url = (f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record['id']}")
    r = requests.delete(url, headers=HEADERS)
    data = r.json()
    print(data)
    print(r.status_code)
    return data, r





#########################



def get_doms():
    data = get()
    records= []
    for idx,record in enumerate(data["result"], start=1):
        print(f"[{idx}] {record['name']}")
        records.append(record)
    print(f"[{idx+1}] Exit")

 



def del_doms():
    records = get_doms()
    total = len(records)
    res = int(input("Introduce el número: "))

    if res < 1 or res > total + 1:
        print("Inválido")
    elif res == total + 1:
        print("Saliendo...")
    else:
        record = records[res -1]
        cdelete(record)
        print(f"{record['name']} eliminado correctamente.")
        

def add_dom():
    nombre = input("Nombre: ")
    data,r = cpost(nombre)
    
    if r.status_code == 200:
        print("[BIEN] Listo crack")
    if r.status_code == 400:
        if data["errors"][0]["code"] == 81053:
            print("Dominio ya existente")
        elif data["errors"][0]["code"] == 9000:
            print("Nombre inválido")
        else:
            print("Error desconocido")


#get_doms()
#del_doms()




def menu():
    print("[1] Consultar mis dominios")
    print("[2] Agregar dominio")
    print("[3] Eliminar dominio")

while True:
    menu()
    option = int(input("Elige: "))
    
    if option == 1:
        get_doms();
        break
    if option == 2:
        del_doms()
        break
    if option == 3:
        add_dom()
        break

