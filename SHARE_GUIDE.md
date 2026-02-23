# How to Share Your Local Library Server

## Option 1: From Mobile on Same WiFi

Make sure your phone and computer are connected to the SAME WiFi network.

### Steps:

1. **Find your PC's IP address:**
   - Open Command Prompt and run:
   
```
ipconfig
```

   - Look for "IPv4 Address" (e.g., `192.168.1.X`)

2. **Run the server:**
   
```
python app.py
```

3. **On your mobile phone:**
   - Open browser (Chrome or Safari)
   - Type in address bar:
   
```
http://YOUR_PC_IP:5000/api/books
```

For example, if your IP is `192.168.1.100`, enter:
```
http://192.168.1.100:5000/api/books
```

**Other endpoints you can try:**
- `/api/users`
- `/api/loans`
- `/api/books/search?q=search_term`

---

## Option 2: From Any Phone Using Internet (ngrok)

Use this when you're NOT on the same WiFi as your computer.

### Steps:

1.**Download ngrok:**
   - Go to https://ngrok.com/download
   - Sign up for free account
   - Extract ZIP and add to PATH

2.**Connect your account:**
   
```
ngrok config add-authtoken YOUR_TOKEN_HERE
```

(Get token from ngrok dashboard)

3.**Run both:**

Terminal 1:
```
python app.py
```

Terminal 2:
```
ngrok http 5000
```

4.**Share the URL shown by ngrok**, for example:
```https://abc123.ngrok.io 
```

Anyone can access it from anywhere!

---

## Quick Reference

| Scenario | What to Use |
|----------|-------------|
|Phone on same WiFi as PC | `http://192.X.X.X:5000/api/books` |
|Phone on different network | Use ngrok URL |
