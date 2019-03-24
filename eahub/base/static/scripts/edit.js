document.getElementById('image-change-toggle').addEventListener('click', function() {
  var image_change = document.getElementById('image-change')
  image_change.style.display = (image_change.style.display == "block") ? 'none' : 'block'
})

document.getElementById('id_image').addEventListener('change', function() {
  if (image_form.value != '') {
    var image_clear_div = document.getElementById('image-clear')
    var image_clear_checkbox = document.getElementById('image-clear_id')
    image_clear_div.style.display = 'none'
    image_clear_checkbox.checked = false
  }
})
