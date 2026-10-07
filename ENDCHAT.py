from shlex import join
import socket
import threading
import time
import sys
import requests
import colorama
import random
import secrets


from colorama import Fore
from Crypto.Cipher import AES


def typewriter(text):
    for letter in text:
        print(letter, end="", flush=True)
        time.sleep(0.001)
    print()




# this file is client/login screen btw

logo = r"""

        ███████╗███╗   ██╗██████╗        ██████╗██╗  ██╗ █████╗ ████████╗
        ██╔════╝████╗  ██║██╔══██╗      ██╔════╝██║  ██║██╔══██╗╚══██╔══╝
        █████╗  ██╔██╗ ██║██║  ██║█████╗██║     ███████║███████║   ██║   
        ██╔══╝  ██║╚██╗██║██║  ██║╚════╝██║     ██╔══██║██╔══██║   ██║   
        ███████╗██║ ╚████║██████╔╝      ╚██████╗██║  ██║██║  ██║   ██║   
        ╚══════╝╚═╝  ╚═══╝╚═════╝        ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                                                 
"""



typewriter(Fore.MAGENTA + logo + Fore.RESET)
print(Fore.YELLOW + "│━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│" + Fore.RESET)

typewriter(Fore.GREEN + "\n                                    END-CHAT." + Fore.RESET)

typewriter(Fore.GREEN + "                              SECURE, ENCRYPTED CHATTING." + Fore.RESET)
time.sleep(1)
print(Fore.RED + "   Connecting..." + Fore.RESET)
time.sleep(1)
print(Fore.GREEN + "   Connected." + Fore.RESET)

colorama.init()


keyletters = "0123456789abcdefABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=~`[]{}|;:',.<>/?"

rng = random.SystemRandom()
RANDOM_KEY = ''.join(rng.choice(keyletters) for _ in range(32))

KEY = RANDOM_KEY.encode()
PORT = 5555

defaultusername = "User"
server_address = ""
server_port = PORT

menu = """
[1] Create Server
[2] Join Chat room/Server
[3] Config
[4] Exit
[5] About/Info
"""

print(Fore.YELLOW + menu + Fore.RESET)

selection = input(
    Fore.YELLOW +
    "Select an option: " +
    Fore.RESET
)


# ENCRYPTION 

def encrypt(message):
    cipher = AES.new(KEY, AES.MODE_GCM)

    data, tag = cipher.encrypt_and_digest(
        message.encode()
    )

    return cipher.nonce + tag + data


def decrypt(data):
    nonce = data[:16]
    tag = data[16:32]
    message = data[32:]

    cipher = AES.new(
        KEY,
        AES.MODE_GCM,
        nonce=nonce
    )

    return cipher.decrypt_and_verify(
        message,
        tag
    ).decode()


# server 

if selection == "1":

    # Get local IP
    try:
        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()

    except:
        local_ip = "Unknown"


    # Get public IP
    try:
        public_ip = requests.get(
            "https://api.ipify.org",
            timeout=5
        ).text.strip()

    except:
        public_ip = "Unknown"


    print(
        Fore.YELLOW +
        "\nEND-CHAT SERVER" +
        Fore.RESET
    )

    print(Fore.YELLOW + f"Local IP : {local_ip}" + Fore.RESET)
    print(Fore.YELLOW + f"Port     : {PORT}" + Fore.RESET)
    print(Fore.YELLOW + f"Public IP: {public_ip}" + Fore.RESET)
    print()


    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    try:
        server.bind(
            ("0.0.0.0", PORT)
        )

        server.listen()

    except Exception as e:

        print(
            Fore.RED +
            f"Could not start server: {e}" +
            Fore.RESET
        )

        input("Press Enter...")
        sys.exit()
    print(
        Fore.GREEN +
        f"Listening on {local_ip}:{PORT}" +
        Fore.RESET
    )
    print(
        Fore.YELLOW +
        "(''exit' To Leave Chat.)" +
        Fore.RESET
    )
    print(
        Fore.YELLOW +
        f"Outside users connect to {public_ip}:{PORT}" +
        Fore.RESET
    )

    clients = []


    def send_packet(client, data):

        packet = (
            len(data).to_bytes(4, "big")
            + data
        )

        client.sendall(packet)


    def recv_packet(client):

        size_data = client.recv(4)

        if not size_data:
            return None

        size = int.from_bytes(
            size_data,
            "big"
        )

        data = b""

        while len(data) < size:

            chunk = client.recv(
                size - len(data)
            )

            if not chunk:
                return None

            data += chunk

        return data


    def broadcast(data, sender):

        for client in clients[:]:

            if client == sender:
                continue

            try:
                send_packet(
                    client,
                    data
                )

            except:

                if client in clients:
                    clients.remove(client)

                try:
                    client.close()
                except:
                    pass


    def handle_client(client, address):

        username = "Unknown"

        try:

            # Receive username
            username_data = recv_packet(client)

            if username_data is None:
                return

            username = decrypt(
                username_data
            )

            print(
                Fore.YELLOW +
                f"{username} joined END-CHAT." +
                Fore.RESET
            )


            while True:

                data = recv_packet(client)

                if data is None:
                    break

                # Send encrypted message to everyone else
                broadcast(
                    data,
                    client
                )


        except Exception as e:

            print(
                Fore.RED +
                f"{username} disconnected." +
                Fore.RESET
            )


        finally:

            if client in clients:
                clients.remove(client)

            try:
                client.close()
            except:
                pass


    while True:

        try:

            client, address = server.accept()

            clients.append(client)

            threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            ).start()

        except KeyboardInterrupt:

            print(
                Fore.RED +
                "\nServer stopped." +
                Fore.RESET
            )

            break


#client 

elif selection == "2":

    defaultusername = input(
        Fore.YELLOW +
        "Username: " +
        Fore.RESET
    ).strip()


    if not defaultusername:

        print(
            Fore.RED +
            "Invalid username." +
            Fore.RESET
        )

        input("Press Enter...")
        sys.exit()


    serverip = input(
        Fore.YELLOW +
        "Server IP: " +
        Fore.RESET
    ).strip()


    if not serverip:

        print(
            Fore.RED +
            "Invalid server IP." +
            Fore.RESET
        )

        input("Press Enter...")
        sys.exit()


    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )


    try:

        client.connect(
            (
                serverip,
                server_port
            )
        )

    except Exception as e:

        print(
            Fore.RED +
            f"Could not connect to END-CHAT." +
            Fore.RESET
        )

        input("Press Enter...")
        sys.exit()


    print(
        Fore.GREEN +
        "Connected to END-CHAT." +
        "(''exit' To Leave Chat.)" +
        Fore.RESET
    )


    def send_packet(data):

        client.sendall(
            len(data).to_bytes(4, "big")
            + data
        )


    def recv_packet():

        size_data = client.recv(4)

        if not size_data:
            return None

        size = int.from_bytes(
            size_data,
            "big"
        )

        data = b""

        while len(data) < size:

            chunk = client.recv(
                size - len(data)
            )

            if not chunk:
                return None

            data += chunk

        return data


    # Send encrypted username

    username_data = encrypt(
        defaultusername
    )

    send_packet(
        username_data
    )


    # Receive messages

    def receive_messages():

        while True:

            try:

                data = recv_packet()

                if data is None:
                    print(
                        Fore.RED +
                        "\nServer disconnected." +
                        Fore.RESET
                    )

                    break


                message = decrypt(data)

                print(
                    f"\n{message}"
                )

                print(
                    "> ",
                    end="",
                    flush=True
                )


            except:

                break


    threading.Thread(
        target=receive_messages,
        daemon=True
    ).start()


    # Send messages

    while True:

        try:

            message = input("> ")

        except (KeyboardInterrupt, EOFError):

            message = "exit"


        if message.lower() == "exit":

            try:
                client.close()
            except:
                pass

            print(
                Fore.RED +
                "Disconnected from END-CHAT." +
                Fore.RESET
            )

            break


        if not message:
            continue


        full_message = (
            f"{defaultusername}: {message}"
        )


        data = encrypt(
            full_message
        )


        try:

            send_packet(data)

        except:

            print(
                Fore.RED +
                "Connection lost." +
                Fore.RESET
            )

            break


# config

elif selection == "3":

    print(
        Fore.YELLOW +
        "CONFIGURATION" +
        Fore.RESET
    )


    configmenu = """
1. Change username
2. Change server address
3. Change server port
4. Back
"""


    print(
        Fore.LIGHTGREEN_EX +
        configmenu +
        Fore.RESET
    )


    config = input(Fore.MAGENTA +
        "Enter configuration: " +
        Fore.RESET
    ).strip()


    if config == "1":

        configuser = input(
            Fore.LIGHTGREEN_EX +
            "Enter new username: " +
            Fore.RESET
        ).strip()


        if not configuser:

            print(
                Fore.RED +
                "Invalid username." +
                Fore.RESET
            )

        else:

            defaultusername = configuser

            print(
                Fore.GREEN +
                f"Username changed to {defaultusername}" +
                Fore.RESET
            )


    elif config == "2":

        new_address = input(
            Fore.LIGHTGREEN_EX +
            "Enter new server address: " +
            Fore.RESET
        ).strip()


        if not new_address:

            print(
                Fore.RED +
                "Invalid server address." +
                Fore.RESET
            )

        else:

            server_address = new_address

            print(
                Fore.GREEN +
                f"Server address changed to {server_address}" +
                Fore.RESET
            )


    elif config == "3":

        try:

            new_port = int(
                input(
                    Fore.LIGHTGREEN_EX +
                    "Enter new server port: " +
                    Fore.RESET
                )
            )


            if new_port < 1 or new_port > 65535:

                print(
                    Fore.RED +
                    "Invalid server port." +
                    Fore.RESET
                )

            else:

                server_port = new_port

                print(
                    Fore.GREEN +
                    f"Server port changed to {server_port}" +
                    Fore.RESET
                )

        except ValueError:

            print(
                Fore.RED +
                "Port must be a number." +
                Fore.RESET
            )


    elif config == "4":

        pass


    else:

        print(
            Fore.RED +
            "Invalid configuration option." +
            Fore.RESET
        )


    input(
        "\nPress Enter..."
    )


#  exit

elif selection == "4":

    print(
        Fore.RED +
        "Exiting..." +
        Fore.RESET
    )

    time.sleep(0.9)

    print(
        Fore.YELLOW +
        "Bye." +
        Fore.RESET
    )

    sys.exit()

elif selection == "5":

    print(
        Fore.RED +
        "ABOUT/INFO" +
        Fore.RESET
    )

    time.sleep(0.9)

    print(
        Fore.YELLOW +
        "This is the ENDCHAT application. Version 1.0." +
        "\nDeveloped by zed" +
        "\nMUST KNOW: Please Enable Port Forwarding on your router or this application may not work correctly." +
        "\nThat is all! Have fun chatting, securely, and privately." +
        Fore.RESET
    )
    input("Enter to exit... ")
    

else:

    print(
        Fore.RED +
        "Invalid selection." +
        Fore.RESET
    )

    input(
        "Press Enter to close..."
    )
