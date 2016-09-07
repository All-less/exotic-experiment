$(document).ready(function() {

    var switchNum = 4;
    var buttonNum = 4;

    var SWITCH_OPENING = 1;
    var SWITCH_OPENED = 2;
    var SWITCH_CLOSING = 3;
    var SWITCH_CLOESD = 4;
    var BUTTON_PRESSING = 6;
    var BUTTON_PRESSED = 7;
    var BUTTON_RELEASING = 8;
    var BUTTON_RELEASED = 9;

    /* try-open: 尝试打开开关 */
    var ANIM_TRY_OPEN = { "margin-top": "10px" };
    /* de-open: 取消半打开的状态 */
    var ANIM_DE_OPEN = { "margin-top": "0px" };
    /* succ-open: 开关被成功打开 */
    var ANIM_SUCC_OPEN = { "margin-top": "20px" };
    var ANIM_TRY_CLOSE = { "margin-top": "10px" };
    var ANIM_DE_CLOSE = { "margin-top": "20px" };
    var ANIM_SUCC_CLOSE = { "margin-top": "0px" };

    var switchStatus = new Array(switchNum).fill(SWITCH_CLOESD);
    var buttonStatus = new Array(buttonNum).fill(BUTTON_RELEASED);
    var switchTimeout = new Array(switchNum).fill(0);
    var buttonTimeout = new Array(buttonNum).fill(0);

    server.remote.setSwitchOn(function(id) {
        switch (switchStatus[id]) {
            case SWITCH_OPENING:
                clearTimeout(switchTimeout[id]);
                $("#switch" + id).animate(ANIM_SUCC_OPEN, 50);
                switchStatus[id] = SWITCH_OPENED;
                break;
        }
    });

    server.remote.setSwitchOff(function(id) {
        switch (switchStatus[id]) {
            case SWITCH_CLOSING:
                clearTimeout(switchTimeout[id]);
                $("#switch" + id).animate(ANIM_SUCC_CLOSE, 50);
                switchStatus[id] = SWITCH_CLOESD;
                break;
        }
    });

    new Array(switchNum).map(function(e, i) {
        $("#switch" + i).on("click", function() {
            console.log("switch " + i + " clicked.");
            switch (switchStatus[i]) {
                case SWITCH_CLOESD:
                    server.local.switchOn(i);
                    $(this).animate(ANIM_TRY_OPEN, 50);
                    switchStatus[i] = SWITCH_OPENING;
                    break;
                case SWITCH_OPENED:
                    server.local.switchOff(i);
                    $(this).animate(ANIM_TRY_CLOSE, 50);
                    switchStatus[i] = SWITCH_CLOSING;
                    break;
            }
            switchTimeout[i] = setTimeout(function() {
                switch (switchStatus[i]) {
                    case SWITCH_CLOSING:
                        switchStatus[i] = SWITCH_OPENED;
                        $(this).animate(ANIM_DE_CLOSE, 50);
                        break;
                    case SWITCH_OPENING:
                        switchStatus[i] = SWITCH_CLOESD;
                        $(this).animate(ANIM_DE_OPEN, 50);
                        break;
                }
            }, 60000);
        });
    });

    new Array(buttonNum).map(function(e, i) {
        $("#button" + i).on("mousedown", function() {

        }).on("mouseup", function() {

        });
    });
});