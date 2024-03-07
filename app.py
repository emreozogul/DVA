import eel

@eel.expose
def say_hello_py(x ):
    print('Hello from %s ' % x )

user = []

@eel.expose  # Eel function
def set_title():  # Example to send data for javascript/html
    return "Code example - Eel + Bootstrap 4 + MongoDb"


@eel.expose  # Eel function
def get_users():
    all_users = user
    for x in all_users:
        x.pop("_id")  # Remove objects id
        all_users.append(x)
    return all_users

    

if __name__ == '__main__':
    eel.init('web')  # Give folder containing web files
    eel.start('index.html', size=(1000, 800) )    # Start
    