var privacy1_checkbox = document.getElementById('privacy-1')
var privacy2_checkbox = document.getElementById('privacy-2')
var update_btn = document.getElementById('update-btn')

privacy1_checkbox.addEventListener('click', function() {
  toggleUpdateBtn()
})
privacy2_checkbox.addEventListener('click', function() {
  toggleUpdateBtn()
})

function toggleUpdateBtn() {
  if (privacy1_checkbox.checked && privacy2_checkbox.checked) {
    update_btn.style.display = 'block'
  } else {
    update_btn.style.display = 'none'
  }
}
