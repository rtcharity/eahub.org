export default class Navbar {
  constructor(burgerBtnHtmlElement, navbarHtmlElement) {
    this.burgerBtnHtmlElement = burgerBtnHtmlElement;
    this.navbarHtmlElement = navbarHtmlElement;
  }

  toggleMenuOnClick() {
    const that = this;
    this.burgerBtnHtmlElement.addEventListener('click', function() {
      that.navbarHtmlElement.style.display = that.navbarHtmlElement.style.display == 'inline-block' ? 'none' : 'inline-block';
    })
  }

  disappearMenuOnMovingCursorAway() {
    this.navbarHtmlElement.onmouseout = function(event) {
      var element_left = event.target
      var element_new = event.relatedTarget
      if (element_new.className.includes('container') || element_new.id == 'body') {
        navbar.style.display = 'none'
      }
    }
  }

}
