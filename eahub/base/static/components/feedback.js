async function ajaxSubmit(){
  document.getElementById('page_url').value = window.location.pathname;
  const form = document.getElementById('form');
  const response = await fetch(form.action, {
    method: form.method,
    body: new URLSearchParams(new FormData(form)),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(response => {
    if(response.status === 200) {
      document.getElementById("successmsg").style.display = "block";
      document.getElementById("form").style.display = "none"; 
    }
    else {
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

document.getElementById("feedbackSubmit").onclick = ajaxSubmit;
document.getElementById("feedbackSubmitAgain").onclick = refreshFeedback;

