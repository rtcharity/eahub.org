async function ajaxSubmit(){
  document.getElementById('page_url').value = window.location.pathname;
  const form = document.getElementById('feedbackForm');
  const response = await fetch(form.action, {
    method: form.method,
    body: new URLSearchParams(new FormData(form)),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(response => {
    if(response.status === 200) {
      document.getElementById("feedbackSuccessMsg").style.display = "block";
      document.getElementById("feedbackSubmitAgain").style.display = "block";
      document.getElementById("feedbackForm").style.display = "none";
      document.getElementById("feedbackSubmit").style.display = "none";
    }
    else {
      document.getElementById("feedbackErrorMsg").style.display = "block";
    }
  });
}

function refreshFeedback() {
  document.getElementById("feedbackSuccessMsg").style.display = "none";
  document.getElementById("feedbackErrorMsg").style.display = "none";
  document.getElementById("feedbackSubmitAgain").style.display = "none";
  document.getElementById("feedbackForm").reset();
  document.getElementById("feedbackForm").style.display = "block";
  document.getElementById("feedbackSubmit").style.display = "block";
}

document.getElementById("feedbackSubmit").onclick = ajaxSubmit;
document.getElementById("feedbackSubmitAgain").onclick = refreshFeedback;

