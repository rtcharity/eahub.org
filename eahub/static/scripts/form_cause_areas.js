$(document).ready(function() {
  var field_cause_areas_other = document.getElementById('field_cause_areas_other')
  var field_pledge_other = document.getElementById('field_pledge_other')
  var textarea_cause_areas_other = document.getElementById('id_cause_areas_other')
  var textarea_pledge_other = document.getElementById('id_giving_pledge_other')
  var multiselect_container = document.getElementsByClassName('multiselect-container')[0]
  var pledge_form = document.getElementById('pledge-form')
  var pledge_other;

  for (var i=0; i<pledge_form.children.length; i++) {
      if (pledge_form.children[i].value == 'OTHER') {
        pledge_other = pledge_form.children[i];
      }
  }

  pledge_form.addEventListener('click',function() {
    if (pledge_other.selected) {
      field_pledge_other.style.display = 'block'
    } else {
      field_pledge_other.style.display = 'none'
      textarea_pledge_other.value = ''
    }
  })

  var other_checkboxes = form.getOtherCheckboxes(multiselect_container)

  multiselect_container.addEventListener('click',function() {
    other_checkboxes.forEach(function(other_checkbox) {
      if (form.checkForm(other_checkbox, 'cause_area')) {
        if (other_checkbox.checked == true) {
          field_cause_areas_other.style.display = 'block'
        } else {
          field_cause_areas_other.style.display = 'none'
          textarea_cause_areas_other.value = ''
        }
      }
    })
  })

})
