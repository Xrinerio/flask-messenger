function addMes(username, mes){
    var newLi = document.createElement('li');
    var mymes = document.createElement('div');
    var nmymes = document.createElement('div');
    mymes.className = "mymes"
    nmymes.className = "nmymes"
    const textMes = document.createTextNode(mes);
    const place = document.querySelector("#messages")
    newLi.appendChild(textMes);

    if(username == document.getElementById('username').textContent){
        newLi.className = 'newmsg'
        nmymes.appendChild(newLi)
        place.prepend(nmymes)
    }else{
        newLi.className = "hostmsg"
        mymes.appendChild(newLi)
        place.prepend(mymes)
    };
}

var form = document.getElementById("form_send_msg");
function handleForm(event) { event.preventDefault(); } 
form.addEventListener('submit', handleForm);

var socket = io();


document.querySelector('#send_msg').addEventListener('click', () => {
    console.log("DA")
    var mes = document.querySelector('#message_input').value
    if (mes != ''){
        socket.send({
        'msg': mes
    })};
    document.querySelector('#message_input').value = '';
});

socket.on('message', data => {
    addMes(data.username, data.msg)
});