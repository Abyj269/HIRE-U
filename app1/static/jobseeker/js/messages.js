
let input_message = document.querySelector('#input-message');
let message_body = document.querySelector('.chat-content');
let send_message_form = document.querySelector('#send-message-form');


const USER_ID=document.querySelector('#loggeduser').value;
const sent_to=document.querySelector('#senttouser').value;

let loc=window.location
let wsStart='ws://'

if(loc.protocol==='https')
{
    wsStart='wss://'
}
let endpoint = wsStart + loc.host + loc.pathname


var socket=new WebSocket(endpoint)

socket.onopen =async function(event)
{
    console.log('open',event)
}

socket.onmessage =async function(messageEvent)
{
    console.log('message',messageEvent)
    let data =JSON.parse(messageEvent.data)
    let message=data['message']
    newMessage(message)

}

socket.onerror =async function(event)
{
    console.log('error',event)
}
socket.onclose =async function(closeEvent)
{
    console.log('close',closeEvent)
}



function newMessage(message,sent_by_id) {
	if (message.trim() === '') {
        return false;
    }

    let message_element;
    if(sent_by_id == USER_ID)
    {
        message_element= `
        <div class="d-flex flex-row justify-content-start chat_reciever">
       
        <div>
          <p class="small p-2 ms-3 mb-1 rounded-3" style="background-color: #f5f6f7;">${message}</p>

        </div>
      </div>
        
        `;
       
    }
    else
    {
        message_element= `   <div class="d-flex flex-row justify-content-end mb-4 pt-1 chat_user">
        <div>
            <p class="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">${message}</p>
        </div>
       
    </div>
    `;
    }
   


   
	    
    let new_message = document.createElement('div');
    new_message.innerHTML = message_element;

    message_body.appendChild(new_message);

    message_body.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
      });
    input_message.value = '';

}

   
send_message_form.addEventListener('submit', function(e) {
    e.preventDefault();
   
    const message = input_message.value;
   
    const data = {
        'message': message,
        'sent_by':USER_ID,
        'sent_to':sent_to,
    };

  
    if (socket.readyState === WebSocket.OPEN) {
        // Use the WebSocket send() method directly
        socket.send(JSON.stringify(data));
    }

    // Use reset() method to reset form
    send_message_form.reset();
});

socket.onerror = function(event) {
    console.error("WebSocket error observed: ", event);
};















