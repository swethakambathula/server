#Getting the libraries we will use in this assignment
import threading
from flask import Flask, render_template, session, copy_current_request_context,request

from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
import time,socket, flask



#Initializing the parameters of the flask server and the sockets 
#We will need threading too. This is a multithreaded server.
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'confidential!'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


#If the client connects to this server, then we need to welcome them
@socket_.on('connection', namespace='/test')#Listening to the client connection
def my_emitter(stuff):
    thismoment1 = time.time()#We want to register the time it takes to emit or respond to a request
    session['counter'] = session.get('counter', 0) + 1#This line will appear severally in this server. We are enumerating the logs
    emit('response',
         {'data': stuff['data'], 'count': session['counter']})
    thismoment2 = time.time()
    difference = str(thismoment2-thismoment1) #Getting time difference
  
    print("Duration in seconds :" + difference)#Time spent to serve the request by the client

def update():
    
    time.sleep(1)#Clock will count after every second
    
    socket_.emit('my_respons',
         {'data': time.time()},
        namespace='/test')
    print("emitted")#You may comment this out if it seems a nuisance to you. After every second, it is displayed on the terminal!
    update()
    
t=threading.Thread(target=update)




@socket_.on('connect', namespace='/test')
def handle_connect():
    print('Client connected!')#If the client connects, print this: Client connected!
   
    if not t.is_alive():
        t.start()


@app.route('/')
def index():
    
    return render_template('index.html', async_mode=socket_.async_mode)
    
    
    

   
   
   
   
#We are displaying information about the server when the client asks so via a submit button on the client side.
@socket_.on('client', namespace='/test')
def client_request(something):
    
    
    #Parameters of interest used by the server
    protocol = protocols[proto]
    canonnam = canonname
    famil = families[family]
    
    sockaddress = sockaddr
    typs = types[socktype]
    
    hostname, aliases, addresses = socket.gethostbyaddr('127.0.0.1') 
    now1 = time.time()
    session['counter'] = session.get('counter', 0) + 1
    emit('response',
         {'data':"Family:"+" "+famil, 'count': session['counter']})
    
    emit('response',
         {'data':"Protocols:"+" "+protocol, 'count': session['counter']})
    emit('response',
         {'data':" Canon Name:"+" "+canonnam, 'count': session['counter']})
    emit('response',
         {'data':" Type:"+" "+typs, 'count': session['counter']})
    emit('response',
         {'data':"Socket Address:"+" "+sockaddress, 'count': session['counter']})
    emit('response',
         {'data':"***Host:"+" "+hostname+"*** "+ "Address: "+" "+flask.request.host_url 
         +"*** "+ "Connection is from {} to {}".format(socket.gethostname(), request.remote_addr) , 'count': session['counter']})
   
    
    now2 = time.time()
    duration = str(now2-now1) 
    print (socket.gethostname())
    
   
    
    print("Duration in seconds :" + duration)
    hostname, aliases, addresses = socket.gethostbyaddr('127.0.0.1')
    print ('Hostname :', hostname)
    print ('Aliases  :', aliases)
    print ('Addresses:', addresses)
    
    information('127.0.0.1')
    
 



 
#The socket module has several parameters such as the family, protocols, socket type etc. We need them
@socket_.on('mapper', namespace='/test')
def information(that):
    
    return dict( (getattr(socket, x), x)
                 for x in dir(socket)
                 if x.startswith(that)
                 )

families = information('AF_')
types = information('SOCK_')
protocols = information('IPPROTO_')

for response in socket.getaddrinfo('127.0.0.1', 'http',socket.AF_INET, socket.SOCK_STREAM,  socket.IPPROTO_TCP, socket.AI_CANONNAME):
    
    # We need to decompress the tuple
    family, socktype, proto, canonname, sockaddr = response

    print ('Which Family?:', families[family])
    print ('Socket Type:', types[socktype])
    print ('Protocols Used:', protocols[proto])
    print ('Canonical Name:', canonname)
    print ('Address:', sockaddr)
    

@app.route('/url')#When we visit 127:0.0.0.1:8080/url we will find the url of the host
def url():
    
    url = flask.request.host_url
    
    print("Client visited"+" "+url)
    
   
    return url


@socket_.on('close_socket', namespace='/test') #Disconnecting the server request by the client. By doing so, the server will close the socket of the client

def close_socket():
    @copy_current_request_context
    def can_disconnect():
        disconnect()#Closing the client socket

    session['counter'] = session.get('counter', 0) + 1
    emit('response',
         {'data': 'Server stopped listening to you! Goodbye!', 'count': session['counter']},
         callback=can_disconnect)
         



   

socket_.run(app,port=8080)#Server executes from here