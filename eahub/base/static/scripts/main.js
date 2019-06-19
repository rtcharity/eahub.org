import DataTable from './datatable.js';
import Navbar from './navbar.js';
import MultiselectForm from './multiselect-form.js'

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

  console.log(selectorsWithOldStyle)
  const multiselectForm = new MultiselectForm(selectorsWithOldStyle, 10);
  multiselectForm.applySettings();
});
