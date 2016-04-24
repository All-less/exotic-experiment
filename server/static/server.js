var server = (function(){
    var socket = new WebSocket('ws://' + window.location.host + '/socket' + window.location.pathname);
    var pass = function(){};

    Type = {
        action : 0,
        status : 1,
        operation : 2,
        info : 3
    };

    Action = {
        acquire : "acquire",
        release : "release",
        broadcast : "broadcast"
    };

    Status = {
        key_pressed : "key_pressed",
        switch_on : "switch_on",
        switch_off : "switch_off",
        button_pressed : "button_pressed",
        button_released : "button_released",
        file_upload : "file_upload",
        bit_file_program : "bit_file_program"
    }

    Operation = {
        key_press : 1,
        switch_on : 2,
        switch_off : 3,
        button_pressed : 4,
        button_released : 5
    }

    Info = {
        user_changed : "user_changed",
        fpga_disconnected : "fpga_disconnected"
    };

    Remote = {
        keyPress : pass,
        switchOn : pass,
        switchOff : pass,
        buttonPress : pass,
        buttonRelease : pass,
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
        switch(obj.type){
            case Type.action:
                switch (obj.action){
                    case Action.broadcast:
                        Remote.broadcast(obj);
                        break;
                }
                break;
            case Type.status:
                switch (obj.status){
                    case Status.key_pressed:
                        Remote.keyPress(obj.key_code);
                        break;
                    case Status.switch_on:
                        Remote.switchOn(obj.id);
                        break;
                    case Status.switch_off:
                        Remote.switchOff(obj.id);
                        break;
                    case Status.button_pressed:
                        Remote.buttonPress(obj.id);
                        break;
                    case Status.button_released:
                        Remote.buttonRelease(obj.id);
                        break;
                    case Status.file_upload:
                        Remote.fileUpload(obj.file);
                        break;
                    case Status.bit_file_program:
                        Remote.fileProgram(obj.size);
                        break;
                }
                break;
            case Type.operation:
                break;
            case Type.info:
                if (obj.info == Info.fpga_disconnected)
                    Remote.leave();
                else if (obj.info == Info.user_changed)
                    Remote.userChange(obj.user);
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
                    'type' : Type.action,
                    'action' : 'acquire'
                });
            },
            release : function(){
                send({
                    'type' : Type.action,
                    'action' : 'release'
                });
            }
        },
        broadcast: function(message){
            send({
                'type' : Type.action,
                'action' : Action.broadcast,
                'content' : message
            });
        },
        keyPress : function(key){
            send({
                'type' : Type.operation,
                'operation' : Operation.key_press,
                'key_code' : key
            });
        },
        switchOn : function(id){
            send({
                'type' : Type.operation,
                'operation' : Operation.switch_on,
                'id' : id
            });
        },
        switchOff : function(id){
            send({
                'type' : Type.operation,
                'operation' : Operation.switch_off,
                'id' : id
            });
        },
        buttonPress : function(id){
            send({
                'type' : Type.operation,
                'operation' : Operation.button_pressed,
                'id' : id
            });
        },
        buttonRelease : function(id){
            send({
                'type' : Type.operation,
                'operation' : Operation.button_released,
                'id' : id
            });
        },
        remote : {
            setKeyPress : function(func){
                Remote.keyPress = func;
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
            setButtonRelease : function(func){
                Remote.buttonRelease = func;
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
