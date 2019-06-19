export default class ProfileEditImage {
  constructor(imageHtmlElement, imageChangeHtmlElements, imageClearHtmlElements) {
    this.imageHtmlElement = imageHtmlElement;
    this.imageChangeHtmlElements = imageChangeHtmlElements;
    this.imageClearHtmlElements = imageClearHtmlElements;
  }

  toggleImageChangeOnClick() {
    let imageChangeContainer = this.imageChangeHtmlElements.container;
    console.log(this.imageChangeHtmlElements.toggle);
    this.imageChangeHtmlElements.toggle.on('click', function() {
      imageChangeContainer.style.display = (imageChangeContainer.style.display == "block") ? 'none' : 'block'
    })
  }

  removeImageClearOnInput() {
    let imageClearContainer = this.imageClearHtmlElements.container;
    let imageClearCheckbox = this.imageClearHtmlElements.checkbox;
    let imageHtmlElement = this.imageHtmlElement;
    imageHtmlElement.on('change', function() {
      if (imageHtmlElement.value != '') {
        imageClearContainer.css("display", "none");
        imageClearCheckbox.prop('checked', false);
      }
    })
  }
}
