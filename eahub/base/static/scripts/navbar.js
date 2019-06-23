export default class Navbar {
  constructor(burgerBtnHtmlElement, navbarHtmlElement) {
    this.burgerBtnHtmlElement = burgerBtnHtmlElement;
    this.navbarHtmlElement = navbarHtmlElement;
  }

  toggleMenuOnClick() {
    const that = this;
    this.burgerBtnHtmlElement.click(function(e) {
      e.stopImmediatePropagation();
      that.navbarHtmlElement.toggle();
    })
  }

  disappearMenuOnMovingCursorAway() {
    this.navbarHtmlElement.onmouseout = function(event) {
      console.log('mouseout')
      var element_left = event.target
      var element_new = event.relatedTarget
      if (element_new.className.includes('container') || element_new.id == 'body') {
        navbar.style.display = 'none'
      }
    }
  }
}
