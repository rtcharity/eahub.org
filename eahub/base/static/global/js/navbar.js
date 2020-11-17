export function initNavbar() {
  const navbar = new Navbar($('#navbar-toggle-icon'), $('#navbar'));
  navbar.toggleMenuOnClick();
  navbar.disappearMenuOnMovingCursorAway();
}

class Navbar {
  constructor(navbarToggleIcon, navbarHtmlElement) {
    this.navbarToggleIcon = navbarToggleIcon;
    this.navbarHtmlElement = navbarHtmlElement;
  }

  toggleMenuOnClick() {
    const that = this;
    this.navbarToggleIcon.click(function(e) {
        var classList = that.navbarToggleIcon[0].classList;
        if (classList.contains("navbar-toggle-up")) {
            classList.remove("navbar-toggle-up")
            classList.add("navbar-toggle-down")
        } else {
            classList.remove("navbar-toggle-down")
            classList.add("navbar-toggle-up")
        }
        e.stopImmediatePropagation();
        that.navbarHtmlElement.toggle();
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
