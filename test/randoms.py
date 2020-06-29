import uuid

def gen_random_user():
    return ("user-"+str(uuid.uuid1()))

def gen_random_psw():
    return ("psw-"+ str(uuid.uuid4()))
