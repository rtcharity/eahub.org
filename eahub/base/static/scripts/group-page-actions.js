export default class GroupPageActions {
  constructor(htmlElements) {
    this.htmlElements = htmlElements;
  }

  toggleEachElementOnClick() {
    for (let htmlElement of this.htmlElements) {
      this.toggleOnClick(htmlElement);
    }
  }

  toggleOnClick(htmlElement) {
    for (let toggler of htmlElement.togglers) {
      toggler.on('click', function() {
        htmlElement.confirm_field.style.display = htmlElement.confirm_field.style.display == 'block' ? 'none' : 'block';
        htmlElement.toggle_btn.style.display = htmlElement.toggle_btn.style.display == 'none' ? 'inline-block' : 'none';
      })
    }
  }
}
