var server = (function(){
    var socket = new WebSocket('ws://' + window.location.host + '/socket' + window.location.pathname);
    var pass = function(){};

    Type = {
        user : 0,
        keyDown : 1,
        keyUp : 2,
        switchPress : 3
    };

    Remote = {
        keyDown : pass,
        keyUp : pass,
        switchPress : pass,
        userChange : pass,
        leave : pass
    }

    console.table(socket);
    socket.onmessage = function(event) {
        obj = JSON.parse(event.data);
        switch(obj.action){
            case Type.user:
                if (obj.behave == 'liver_leave')
                    Remote.leave()
                else if (obj.behave == 'user_change')
                    Remote.userChange(obj.change);
                break;
            case Type.keyDown:
                Remote.keyDown(obj.code);
                break;
            case Type.keyUp:
                Remote.keyUp(obj.code);
                break;
            case Type.switchPress:
                Remote.switchPress(obj.id);
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
        switchPress : function(id){
            send({
                'action' : Type.switchPress,
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
            setSwitchPress : function(func){
                Remote.switchPress = func;
            },
            setUserChange : function(func){
                Remote.userChange = func;
            },
            setLeave : function(func){
                Remote.leave = func;
            }
        }
    }
})();
