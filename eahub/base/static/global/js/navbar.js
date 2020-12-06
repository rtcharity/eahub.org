export function initNavbar() {
  const navbar = new Navbar($('#menu-toggle-icon'), $('#burger-btn'), $('#dropdown'), $('#navbar-collapsable'));
  navbar.toggleMenuOnClick();
  navbar.disappearMenuOnMovingCursorAway();
}

class Navbar {
  constructor(navbarToggleIcon, burgerBtn, dropdownElement, navbarCollapsable) {
    this.navbarToggleIcon = navbarToggleIcon;
    this.dropdownElement = dropdownElement;
    this.burgerBtn = burgerBtn;
    this.navbarCollapsable = navbarCollapsable;
  }

  toggleMenuOnClick() {
    const that = this;
    this.navbarToggleIcon.click(function(e) {that.toggleMenu(e)})
    this.burgerBtn.click(function(e) {that.toggleCollapsable(e)})
  }

  disappearMenuOnMovingCursorAway() {
    this.dropdownElement.onmouseout = function(event) {
      var element_left = event.target
      var element_new = event.relatedTarget
      if (element_new.className.includes('container') || element_new.id == 'body') {
        navbar.style.display = 'none'
      }
    }
  }

  toggleMenu(e) {
    var that = this;
    var classList = that.navbarToggleIcon[0].classList;
    if (classList.contains("menu-toggle-up")) {
        classList.remove("menu-toggle-up")
        classList.add("menu-toggle-down")
    } else {
        classList.remove("menu-toggle-down")
        classList.add("menu-toggle-up")
    }
    e.stopImmediatePropagation();
    that.dropdownElement.toggle();
  }

  toggleCollapsable(e) {
    e.stopImmediatePropagation();
    this.navbarCollapsable.toggle();
  }
}
