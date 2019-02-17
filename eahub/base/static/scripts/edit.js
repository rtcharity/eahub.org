var privacy_checkbox = document.getElementById('privacy')
var update_btn = document.getElementById('update-btn')

privacy_checkbox.addEventListener('click', function() {
  if (privacy_checkbox.checked) {
    update_btn.style.display = 'block'
  } else {
    update_btn.style.display = 'none'
  }
})
