## Socket

#### Create a new socket

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

#### Connect to server

```python
try :
    s.connect((host, port))
    s.setblocking(0) # non-blocking mode, an error will be raised if send() or recv() fails to work
except :
    # ...
    sys.exit()
```

#### Send data to server

```python
s.send(string)
```

#### Receive data from server

```python
try:
	content = s.recv(buffer_size)
except socket.error:
	# ...
```

## JSON

#### Convert string to json

```python
json.dumps()
```

#### Convert json to string

```python
json.loads()
```
