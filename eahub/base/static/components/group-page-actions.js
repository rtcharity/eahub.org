$(document).ready(() => {
  initGroupPageActions()
});


function initGroupPageActions() {
  let claimGroupHtmlElements = {
    toggle_btn: document.getElementById('claim_group_toggle'),
    confirm_field: document.getElementById('claim_group_confirm_field'),
    togglers: document.getElementsByClassName('claim_group_toggler')
  }

  let reportGroupHtmlElements = {
    toggle_btn: document.getElementById('report_group_inactive_toggle'),
    confirm_field: document.getElementById('report_group_inactive_confirm_field'),
    togglers: document.getElementsByClassName('report_group_inactive_toggler')
  }
  
  const groupPageActions = new GroupPageActions([claimGroupHtmlElements, reportGroupHtmlElements]);
  groupPageActions.toggleEachElementOnClick();
}


class GroupPageActions {
  constructor(htmlElements) {
    this.htmlElements = htmlElements;
  }

  toggleEachElementOnClick() {
    const that = this;
    for (let htmlElement of that.htmlElements) {
      that.toggleOnClick(htmlElement);
    }
  }

  toggleOnClick(htmlElement) {
    for (let toggler of htmlElement.togglers) {
      toggler.addEventListener('click', function() {
        htmlElement.confirm_field.style.display = htmlElement.confirm_field.style.display == 'block' ? 'none' : 'block';
        htmlElement.toggle_btn.style.display = htmlElement.toggle_btn.style.display == 'none' ? 'inline-block' : 'none';
      })
    }
  }
}
