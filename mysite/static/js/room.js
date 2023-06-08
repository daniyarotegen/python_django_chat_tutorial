const roomName = JSON.parse(document.getElementById('room-name').textContent);
const chatThread = document.querySelector('#chat-thread');
const messageInput = document.querySelector('#chat-message-input');

const centrifuge = new Centrifuge("ws://" + window.location.host + "/connection/websocket");

centrifuge.on('connect', function (ctx) {
    console.log("connected", ctx);
});

centrifuge.on('disconnect', function (ctx) {
    console.log("disconnected", ctx);
});

const sub = centrifuge.subscribe('rooms:' + roomName, function (ctx) {
    const chatNewThread = document.createElement('li');
    const chatNewMessage = document.createTextNode(ctx.data.user + ': ' + ctx.data.message);
    chatNewThread.appendChild(chatNewMessage);
    chatThread.appendChild(chatNewThread);
    chatThread.scrollTop = chatThread.scrollHeight;
});

centrifuge.connect();

messageInput.focus();
messageInput.onkeyup = function (e) {
    if (e.keyCode === 13) {
        e.preventDefault();
        const message = messageInput.value;
        if (!message) {
            return;
        }
        sub.publish({ 'message': message });
        messageInput.value = '';
    }
};