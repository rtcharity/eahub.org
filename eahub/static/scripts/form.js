$('.multiselect-form').multiselect();

var field_cause_areas_other = document.getElementById('field_cause_areas_other')
var field_expertise_other = document.getElementById('field_expertise_other')
var field_pledge_other = document.getElementById('field_pledge_other')
var textarea_cause_areas_other = document.getElementById('id_cause_areas_other')
var textarea_expertise_other = document.getElementById('id_expertise_other')
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
