export default class MultiselectForm {
    constructor(selectorsWithOldStyle, minItemsInListForMultiselect) {
      this.selectorsWithOldStyle = selectorsWithOldStyle;
      this.minItemsInListForMultiselect = minItemsInListForMultiselect;
    }

    applySettings() {
      this.addMultiselectClassTo();
      this.enableSearchForListWithAtLeast(this.minItemsInListForMultiselect)
      $('.multiselect-form').multiselect({
        numberDisplayed: 1
      })
    }

    addMultiselectClassTo() {
      this.selectorsWithOldStyle.forEach(function(selector) {
        selector.removeClass('selectmultiple').addClass('form-control multiselect-form')
      })
    }

    enableSearchForListWithAtLeast(num) {
      let className = 'select-with-at-least-'+num+'-items'
      this.addClassNameToListsWithAtLeast(num, className)
      $('.' + className).multiselect({
        enableCaseInsensitiveFiltering: true
      })
    }

    addClassNameToListsWithAtLeast(num, className) {
      const multiselectForms = document.getElementsByClassName('multiselect-form')
      for (var i=0; i <= multiselectForms.length; i++) {
        let multiselectForm = multiselectForms[i]
        if (multiselectForm.length > num) multiselectForm.classList.add(className)
      }
    }
}
