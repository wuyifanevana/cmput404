import socket, time, sys
from multiprocessing import Process

# get ip
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    print(f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_request(addr, conn):
    print("Connected by", addr)
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to google")
    addr.sendall(send_full_data)

    addr.shutdown(socket.SHUT_WR) # shutdown() is different from close()

    data = addr.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    # send data back
    conn.send(data)


def main():
    HOST = "localhost"
    extern_host = "www.google.com"
    PORT = 8001
    BUFFER_SIZE = 1024
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        # allow reused addresses, bind, and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)
        
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(extern_host)

                # connect proxy_end
                proxy_end.connect((remote_ip, PORT))
                p = Process(target=handle_request, args=(proxy_end, conn))
                p.daemon = True
                p.start()
                print("Started process ", p)

                conn.close()

if __name__ == "__main__":
    main()
