export default class MultiselectForms {
    constructor(multiselectFormHtmlElements, selectorsWithOldStyle, minItemsInListForMultiselect) {
      this.multiselectFormHtmlElements = multiselectFormHtmlElements;
      this.selectorsWithOldStyle = selectorsWithOldStyle;
      this.minItemsInListForMultiselect = minItemsInListForMultiselect;
      this.classNameSelectWithAtLeast = null;
      this.minItemsRequiredForSearch = 0;
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
      const that = this;
      this.minItemsRequiredForSearch = num;
      this.classNameSelectWithAtLeast = 'select-with-at-least-'+ that.minItemsRequiredForSearch +'-items'
      this.addClassNameToListsWithAtLeast()
      $('.' + this.classNameSelectWithAtLeast).multiselect({
        enableCaseInsensitiveFiltering: true
      })
    }

    addClassNameToListsWithAtLeast() {
      const that = this;
      const multiselectForms = this.multiselectFormHtmlElements;
      for (let multiselectForm of multiselectForms) {
        if (multiselectForm.length > that.minItemsRequiredForSearch) multiselectForm.classList.add(that.classNameSelectWithAtLeast)
      }
    }
}
