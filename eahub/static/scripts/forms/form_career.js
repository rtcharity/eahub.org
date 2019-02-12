$(document).ready(function() {
  var field_expertise_other = document.getElementById('field_expertise_other')
  var textarea_expertise_other = document.getElementById('id_expertise_other')
  var multiselect_container = document.getElementsByClassName('multiselect-container')[0]

  var other_checkboxes = helpers.getOtherCheckboxes(multiselect_container)

  multiselect_container.addEventListener('click',function() {
    other_checkboxes.forEach(function(other_checkbox) {
      if (helpers.checkForm(other_checkbox, 'career')) {
        if (other_checkbox.checked == true) {
          field_expertise_other.style.display = 'block'
        } else {
          field_expertise_other.style.display = 'none'
          textarea_expertise_other.value = ''
        }
      }
    })
  })

})
