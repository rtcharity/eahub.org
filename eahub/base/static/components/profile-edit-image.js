$(document).ready(() => {
  profileEditImageInit();
});


function profileEditImageInit() {
  const imageHtmlElement = document.getElementById('id_image');
  const imageChangeHtmlElements = {
    container: document.getElementById('image-change'),
    toggle: document.getElementById('image-change-toggle')
  }
  const imageClearHtmlElements = {
    container: document.getElementById('image-clear'),
    checkbox: document.getElementById('image-clear_id')
  }
  const profileEditImage = new ProfileEditImage(imageHtmlElement, imageChangeHtmlElements, imageClearHtmlElements);
  profileEditImage.toggleImageChangeOnClick();
  profileEditImage.removeImageClearOnInput();
}


class ProfileEditImage {
  constructor(imageHtmlElement, imageChangeHtmlElements, imageClearHtmlElements) {
    this.imageHtmlElement = imageHtmlElement;
    this.imageChangeHtmlElements = imageChangeHtmlElements;
    this.imageClearHtmlElements = imageClearHtmlElements;
  }

  toggleImageChangeOnClick() {
    let imageChangeContainer = this.imageChangeHtmlElements.container;
    this.imageChangeHtmlElements.toggle.addEventListener('click', function() {
      imageChangeContainer.style.display = (imageChangeContainer.style.display == "block") ? 'none' : 'block'
    })
  }

  removeImageClearOnInput() {
    let imageClearContainer = this.imageClearHtmlElements.container;
    let imageClearCheckbox = this.imageClearHtmlElements.checkbox;
    let imageHtmlElement = this.imageHtmlElement;
    imageHtmlElement.addEventListener('change', function() {
      if (imageHtmlElement.value != '') {
        imageClearContainer.style.display = "none";
        imageClearCheckbox.checked = false;
      }
    })
  }
}
