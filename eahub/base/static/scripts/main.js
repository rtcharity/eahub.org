import DataTable from './datatable.js';
import Navbar from './navbar.js';
import MultiselectForms from './multiselect-forms.js'
import GroupPageActions from './group-page-actions.js'
import ProfileEditImage from './profile-edit-image.js'

$(document).ready( function () {
  const dt = new DataTable($('#datatable-profiles'), $('datatable-groups'));
  dt.applySearchFunctionality(dt.dataTableProfiles);
  dt.applySearchFunctionality(dt.dataTableGroups);

  const navbar = new Navbar(document.getElementById('burger-btn'), document.getElementById('navbar'));
  navbar.toggleMenuOnClick();
  navbar.disappearMenuOnMovingCursorAway();

  const selectorsWithOldStyle = [
    $('#id_local_groups'),
    $('#id_available_as_speaker'),
    $('#id_open_to_job_offers'),
    $('#id_available_to_volunteer')
  ]

  const multiselectFormHtmlElements = $('.multiselect-form')
  const multiselectForm = new MultiselectForms(multiselectFormHtmlElements, selectorsWithOldStyle, 10);
  multiselectForm.applySettings();

  let claimGroupHtmlElements = {
    toggle_btn: $('#claim_group_toggle'),
    confirm_field: $('#claim_group_confirm_field'),
    togglers: $('#claim_group_toggler')
  }

  let reportGroupHtmlElements = {
    toggle_btn: $('#report_group_inactive_toggle'),
    confirm_field: $('#report_group_inactive_confirm_field'),
    togglers: $('#report_group_inactive_toggler')
  }

  const groupPageActions = new GroupPageActions([claimGroupHtmlElements, reportGroupHtmlElements]);
  groupPageActions.toggleEachElementOnClick();

  const imageHtmlElement = $('#id_image');
  const imageChangeHtmlElements = {
    container: $('#image-change'),
    toggle: $('#image-change-toggle')
  }
  const imageClearHtmlElements = {
    container: $('#image-clear'),
    checkbox: $('#image-clear_id')
  }
  const profileEditImage = new ProfileEditImage(imageHtmlElement, imageChangeHtmlElements, imageClearHtmlElements);
  profileEditImage.toggleImageChangeOnClick();
  profileEditImage.removeImageClearOnInput();
});
