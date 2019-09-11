'use strict';
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
var send2Server = function (){
    var msg = $('input#customer-input').val();
    socket.emit('send msg', {data: msg});
    }
    socket.on('res', function (msg){
        $('div.content').after('<div class="msg-content"><span>' + msg.data + '</span></div>')
    })