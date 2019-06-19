export default class MultiselectForms {
    constructor(multiselectFormHtmlElements, selectorsWithOldStyle, minItemsInListForMultiselect) {
      this.multiselectFormHtmlElements = multiselectFormHtmlElements;
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
      for (let selector of this.selectorsWithOldStyle) {
        selector.removeClass('selectmultiple').addClass('form-control multiselect-form')
      }
    }

    enableSearchForListWithAtLeast(num) {
      let className = 'select-with-at-least-'+num+'-items'
      this.addClassNameToListsWithAtLeast(num, className)
      $('.' + className).multiselect({
        enableCaseInsensitiveFiltering: true
      })
    }

    addClassNameToListsWithAtLeast(num, className) {
      const multiselectForms = this.multiselectFormHtmlElements;
      for (let multiselectForm of multiselectForms) {
        if (multiselectForm.length > num) multiselectForm.addClass(className)
      }
    }
}
