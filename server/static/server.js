var server = (function(){
    var socket = new WebSocket('ws://' + window.location.host + '/socket' + window.location.pathname);
    var pass = function(){};

    Type = {
        user : 0,
        keyDown : 1,
        keyUp : 2,
        switchOn : 3,
        switchOff : 4,
        buttonPress : 5
    };

    Remote = {
        keyDown : pass,
        keyUp : pass,
        switchOn : pass,
        switchOff : pass,
        buttonPress : pass,
        userChange : pass,
        leave : pass,
        fileUpload : pass,
        fileProgram : pass,
        broadcast : pass
    }

    console.table(socket);
    socket.onmessage = function(event) {
        obj = JSON.parse(event.data);
        if (obj.broadcast == 1){
            delete obj.broadcast
            Remote.broadcast(obj);
        }
        switch(obj.action){
            case Type.user:
                if (obj.behave == 'liver_leave')
                    Remote.leave()
                else if (obj.behave == 'user_change')
                    Remote.userChange(obj.change);
                else if (obj.behave == 'file_upload')
                    Remote.fileUpload(obj.info);
                else if (obj.behave == 'file_program')
                    Remote.fileProgram()
                break;
            case Type.keyDown:
                Remote.keyDown(obj.code);
                break;
            case Type.keyUp:
                Remote.keyUp(obj.code);
                break;
            case Type.switchOn:
                Remote.switchOn(obj.id);
                break;
            case Type.switchOff:
                Remote.switchOff(obj.id);
                break;
            case Type.buttonPress:
                Remote.buttonPress(obj.id);
                break;
        }
    };

    socket.onclose = function(event) {
    };

    socket.onopen = function(event) {
    };

    function send(data){
        if (socket.readyState == WebSocket.OPEN)
            socket.send(JSON.stringify(data));
        else
            console.log('socket not open');
    }

    return {
        user : {
            acquire : function(){
                send({
                    'action' : Type.user,
                    'behave' : 'acquire'
                });
            },
            release : function(){
                send({
                    'action' : Type.user,
                    'behave' : 'release'
                });
            }
        },
        broadcast: function(message){
            send({
                'broadcast' : 1,
                'message' : message
            })
        },
        keyDown : function(key){
            send({
                'action' : Type.keyDown,
                'code' : key
            });
        },
        keyUp : function(key){
            send({
                'action' : Type.keyUp,
                'code' : key
            });
        },
        switchOn : function(id){
            send({
                'action' : Type.switchOn,
                'id' : id
            });
        },
        switchOff : function(id){
            send({
                'action' : Type.switchOff,
                'id' : id
            });
        },
        buttonPress : function(id){
            send({
                'action' : Type.buttonPress,
                'id' : id
            });

        },
        remote : {
            setKeyDown : function(func){
                Remote.keyDown = func;
            },
            setKeyUp : function(func){
                Remote.keyUp = func;
            },
            setSwitchOn : function(func){
                Remote.switchOn = func;
            },
            setSwitchOff : function(func){
                Remote.switchOff = func;
            },
            setButtonPress : function(func){
                Remote.buttonPress = func;
            },
            setUserChange : function(func){
                Remote.userChange = func;
            },
            setLeave : function(func){
                Remote.leave = func;
            },
            setFileUpload : function(func){
                Remote.fileUpload = func;
            },
            setFileProgram : function(func){
                Remote.fileProgram = func;
            },
            setBroadcast : function(func){
                Remote.broadcast = func;
            }
        }
    }
})();
