var form = (function() {
  return {
    checkForm: function(otherInput, formName) {
      if (otherInput.baseURI.indexOf(formName) !== -1) {
        return true;
      } else {
        return false;
      }
    },
    getOtherCheckboxes: function(multiselect_container) {
      var other_checkboxes = [];
      for (var i=0; i<multiselect_container.children.length; i++) {
        var input_multiselect = multiselect_container.children[i].children[0].childNodes[0].firstChild
        if (input_multiselect.value == 'OTHER') {
          other_checkboxes.push(input_multiselect);
        }
      }
      return other_checkboxes;
    }
  }
})()
