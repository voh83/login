import sys
sys.path.append("C:\\Users\\vlonc_000\\Documents\\08 code\\test_firebase")
import requests
import json
import randoms

def test_api_is_up():
    url="http://127.0.0.1:5000/"
    response = requests.request("GET", url)
    assert response.status_code == 200
    assert response.json()["message"]=="Hello World!"

def test_register_user_fails_when_empty_values_are_given():
    url="http://127.0.0.1:5000/register"
    payload={'email':'',"password":''}

    headers = {
        'Content-Type': "application/json"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    assert response.status_code == 204

def test_register_user_fails_when_user_already_exist():
    url="http://127.0.0.1:5000/register"
    payload={'email':'usuario-1',"password":'psw-1'}

    headers = {
        'Content-Type': "application/json"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    assert response.status_code == 409
    assert response.json()["message"]=="Usuario ya existe"

def test_register_user_successfully():

    url="http://127.0.0.1:5000/register"

    payload={'email':randoms.gen_random_user(),"password":randoms.gen_random_psw()}

    headers = {
        'Content-Type': "application/json"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    assert response.status_code == 409
    assert response.json()["message"]=="Usuario ya existe"  

def test_login_user_succesfully():
    register_url="http://127.0.0.1:5000/register"
    headers = {'Content-Type': "application/json"}
   
   #Given
    email=randoms.gen_random_user()
    password=randoms.gen_random_psw()
    payload={'email':email,"password":password}
    

    #User Register
    response = requests.request("POST", register_url, data=json.dumps(payload), headers=headers)

    login_url="http://127.0.0.1:5000/login"

    response = requests.request("POST", login_url, data=json.dumps(payload), headers=headers)

    #TODO:Agregar todo lo que es el token....
    assert response.status_code == 200
    assert response.json()["message"]=="Usuario Loggeado exitosamente" 

def test_login_fail_when_empty_values_are_given():

    url="http://127.0.0.1:5000/login"

    payload={'email':'','password':''}

    headers = {
        'Content-Type': "application/json"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    assert response.status_code == 204

def test_login_fail_when_worng_password_is_given():
    register_url="http://127.0.0.1:5000/register"
    headers = {'Content-Type': "application/json"}
   
   #Given
    email=randoms.gen_random_user()
    password=randoms.gen_random_psw()
    register_payload={'email':email,"password":password}
    
    #User Register
    response = requests.request("POST", register_url, data=json.dumps(register_payload), headers=headers)

    login_url="http://127.0.0.1:5000/login"
    login_payload={'email':email,"password":"wrong_password"}

    response = requests.request("POST", login_url, data=json.dumps(login_payload), headers=headers)
    
    assert response.status_code == 404
    assert response.json()["message"]=="Usuario/Constraseña Incorrectos" 