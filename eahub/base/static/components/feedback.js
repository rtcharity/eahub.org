async function ajaxsubmit(){
  document.getElementById('page_url').value = window.location.href;
  const form = document.getElementById('form');
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
