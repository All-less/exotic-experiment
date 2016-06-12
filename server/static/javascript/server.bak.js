var server = (function(){

    var socket = new WebSocket('ws://' + window.location.host + '/socket' + window.location.pathname);
    function pass() {}

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
        file_upload : "file_uploaded",
        bit_file_program : "bit_file_programmed",
        disk_file_downloaded : "disk_file_downloaded"
    };

    Operation = {
        key_press : 1,
        switch_on : 2,
        switch_off : 3,
        button_pressed : 4,
        button_released : 5
    };

    Info = {
        user_changed : "user_changed",
        fpga_disconnected : "fpga_disconnected",
        broadcast : "broadcast"
    };

    Remote = {
        keyPressed : pass,
        switchOn : pass,
        switchOff : pass,
        buttonPressed : pass,
        buttonReleased : pass,
        userChanged : pass,
        leave : pass,
        fileUploaded : pass,
        fileProgramed : pass,
        broadcast : pass
    };

    socket.onmessage = function(event) {
        obj = JSON.parse(event.data);
        switch(obj.type){
            case Type.action:
                break;
            case Type.status:
                switch (obj.status){
                    case Status.key_pressed:
                        Remote.keyPressed(obj.key_code);
                        break;
                    case Status.switch_on:
                        Remote.switchOn(obj.id);
                        break;
                    case Status.switch_off:
                        Remote.switchOff(obj.id);
                        break;
                    case Status.button_pressed:
                        Remote.buttonPressed(obj.id);
                        break;
                    case Status.button_released:
                        Remote.buttonReleased(obj.id);
                        break;
                    case Status.file_upload:
                        Remote.fileUploaded(obj.file);
                        break;
                    case Status.bit_file_program:
                        Remote.fileProgramed(obj.size);
                        break;
                }
                break;
            case Type.operation:
                break;
            case Type.info:
                switch (obj.info){
                    case Info.fpga_disconnected:
                        Remote.leave();
                        break;
                    case Info.user_changed:
                        Remote.userChanged(obj.user);
                        break;
                    case Info.broadcast:
                        Remote.broadcast(obj);
                        break;
                }
                break;
        }
    };

    socket.onclose = function(event) {
    };

    socket.onopen = function(event) {
    };

    function send(data){
        if (socket.readyState == WebSocket.OPEN)
            socket.send(data);
        else
            console.log('socket not open');
    }

    function send_JSON(obj){
        send(JSON.stringify(obj));
    }

    /*
     * 针对每种Type生成相应的send_type函数,用于发送消息.
     */
    for (var key in Type){
        tkey = 'send_' + key;
        this[tkey] = (function(key){
            return function(){
                var argv = arguments;
                return function(){
                    var obj = {};
                    obj.type = Type[key];
                    obj[key] = argv[0];
                    Array.prototype.map.call(arguments, function(val, index){
                        obj[argv[index+1]] = val;
                    });
                    send_JSON(obj);
                }
            }
        })(key);
    }

    return {
        local : {
            user : {
                acquire : send_action(Action.acquire),
                release : send_action(Action.release)
            },
            broadcast: send_action(Action.broadcast, 'content'),
            keyPressed : send_operation(Operation.key_press, 'key_code'),
            switchOn : send_operation(Operation.switch_on, 'id'),
            switchOff : send_operation(Operation.switch_off, 'id'),
            buttonPressed : send_operation(Operation.button_pressed, 'id'),
            buttonReleased : send_operation(Operation.button_released, 'id')
        },
        remote : (function(){
            function capitalize(str){
                return str.charAt(0).toUpperCase() + str.slice(1);
            }
            funcs = {};
            /*
             * 针对Remote中的每一个key生成setKey函数,作为接收到相应消息的回调函数.
             */
            for (var key in Remote){
                rkey = 'set' + capitalize(key);
                funcs[rkey] = (function(key){
                    return function(func){
                        Remote[key] = func;
                    }
                })(key);
            }
            return funcs;
        })()
    }
})();
