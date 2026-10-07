# END-CHAT
Encrypted, Secure, End-To-End Chatting powered by Port Forwarding.
===============================================================================

![END-CHAT Screenshot](images/screenshot.png)

# END-CHAT

A terminal-based encrypted chat application built with Python.

END-CHAT lets you **host your own chat server** and have other users connect to it over a network. Messages and usernames are encrypted using **AES-GCM**, while TCP sockets handle the connection between the server and clients. 🔐💬

### Features

* 🔒 AES-GCM encrypted messages
* 🌐 Host your own chat server
* 💻 Connect to remote servers
* 👤 Custom usernames
* ⚙️ Configurable server address & port
* 🧵 Multi-client support
* 🎨 Colored terminal interface
* 🚪 Simple `exit` command to leave chats
* 🐍 Built with Python

### How it works

One user starts **Create Server**, which opens a TCP server on the selected port. Other users can choose **Join Chat room/Server** and connect using the server's IP address.

For users connecting from outside the local network, **port forwarding may be required** depending on the network setup.

### Requirements

```bash
pip install requests colorama pycryptodome
```

Run it with:

```bash
python ENDCHAT.py
```

> ⚠️ This is a personal/learning project. Make sure you understand your network configuration before exposing a server to the internet.

---

Made with love 💓💓💓 by **zed / zxspe**!1!1111!!!!
