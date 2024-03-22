var socket = io();

AddListeners()
ListenAddBtn()

function AddListeners(){
    var reqsended = document.querySelectorAll('.reqsended');

reqsended.forEach((reqbtn) => {
    reqbtn.addEventListener('mouseover', (e) => {
        e.target.style.backgroundColor = 'rgb(165, 89, 89)'
        e.target.textContent = 'X'
    });
});

reqsended.forEach((reqbtn) => {
    reqbtn.addEventListener('mouseout', (e) => {
        e.target.style.backgroundColor = 'rgb(165, 136, 89)'
        e.target.textContent = 'Request Sended'
    });
});

var reqtaket = document.querySelectorAll('.reqtaket');

reqtaket.forEach((takebtn) => {
    takebtn.addEventListener('mouseover', (e) => {
        e.target.style.backgroundColor = 'rgb(82, 130, 105)'
        e.target.textContent = '+'
    });
});

reqtaket.forEach((takebtn) => {
    takebtn.addEventListener('mouseout', (e) => {
        e.target.style.backgroundColor = 'rgb(82, 130, 125)'
        e.target.textContent = 'Request Taket'
    });
})};

function ListenAddBtn(){
    var btns = document.querySelectorAll('.btn');
    btns.forEach((cbtn) => {
        cbtn.addEventListener('click', (e) => {
            var addid = e.target.getAttribute('id');
            var addidsplit = String(addid).split('_')
            var newReqSended = document.createElement('div')


            if (addidsplit[0] == 'add') {
                newReqSended.classList.add('btn','reqsended')
                newReqSended.id = "undo_" + addidsplit[1]
                newReqSended.innerHTML = 'Request Sended'
                e.target.parentNode.replaceChild(newReqSended, e.target)
            }
            else if (addidsplit[0] == 'undo') {
                newReqSended.classList.add('btn','addfriend')
                newReqSended.id = "add_" + addidsplit[1]
                newReqSended.innerHTML = 'Add Friend'
                e.target.parentNode.replaceChild(newReqSended, e.target)
            }
            else if (addidsplit[0] == 'acc') {
                var mes_a = document.createElement('a')
                mes_a.setAttribute('href', '/messages/' + addidsplit[1])
                newReqSended.classList.add('btn','sendmsg')
                newReqSended.id = "_"
                newReqSended.innerHTML = 'Send Message'
                mes_a.appendChild(newReqSended)
                e.target.parentNode.replaceChild(mes_a, e.target)
            }



            socket.emit('add',{
                'data': addid
            });

            AddListeners()
            ListenAddBtn()
            
        });
    });
};



socket.on('add', data => {
    addMes(data.username, data.msg)
})