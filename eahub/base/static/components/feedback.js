function togglemodal(){
  var m = document.getElementById("feedbackModal")
  m.classList.toggle("show");
  var element = document.getElementById("feedback");
  element.classList.toggle("active");
  document.getElementById("overlay").classList.toggle("active");    
}
document.getElementById('page_url').value = window.location.href;

async function ajaxsubmit(){
  var form = document.getElementById('form');
  const response = await fetch(form.action, {
    method: form.method,
    body: new URLSearchParams(new FormData(form)),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(response => {
    if(response.status == "200") {
      document.getElementById("successmsg").style.display = "block";
      document.getElementById("form").style.display = "none"; 
    }
    if(response.status != "200") {
      document.getElementById("errormsg").style.display = "block";    
    }
  });
}

function refreshFeedback() {
  document.getElementById("successmsg").style.display = "none";
  document.getElementById("errormsg").style.display = "none";
  document.getElementById("form").reset();
  document.getElementById("form").style.display = "block";
}
