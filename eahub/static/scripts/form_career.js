$('.multiselect-form').multiselect();
$(document).ready(function() {

  var field_expertise_other = document.getElementById('field_expertise_other')
  var textarea_expertise_other = document.getElementById('id_expertise_other')
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
      if (checkForm(other_input, 'career')) {
        if (other_input.checked == true) {
          field_expertise_other.style.display = 'block'
        } else {
          field_expertise_other.style.display = 'none'
          textarea_expertise_other.value = ''
        }
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
  
})
