$('.multiselect-form').multiselect();

var field_cause_areas_other = document.getElementById('field_cause_areas_other')
var textarea_cause_areas_other = document.getElementById('id_cause_areas_other')
var multiselect_container = document.getElementsByClassName('multiselect-container')[0]
var other_inputs = []
for (var i=0; i<multiselect_container.children.length; i++) {
  var input_multiselect = multiselect_container.children[i].children[0].childNodes[0].firstChild
  if (input_multiselect.value == 'OTHER') {
    other_inputs.push(input_multiselect);
  }
}

multiselect_container.addEventListener('click',function() {
  other_inputs.forEach(function(other_input) {
    if (checkForm(other_input, 'cause_area')) {
      if (other_input.checked == true) {
        field_cause_areas_other.style.display = 'block'
      } else {
        field_cause_areas_other.style.display = 'none'
        textarea_cause_areas_other.value = ''
      }
    }
    else if (checkForm(other_input, 'career')) {
      console.log('display textarea career other')
    }
  })
})

function checkForm(otherInput, formName) {
  if (otherInput.baseURI.indexOf(formName) !== -1) {
    return true;
  } else {
    return false;
  }
}
