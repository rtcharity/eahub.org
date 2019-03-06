$(document).ready( function () {
    var dataTableProfiles = $('#datatable-profiles').DataTable({
      order: [[1, 'asc']],
      columns: [
        { "orderable": false, "targets": 0 },
        null,
        null,
        null
      ],
      lengthChange: false,
      pageLength: 100,
      sDom: 'ltipr'
    } );

    var dataTableGroups = $('#datatable-groups').DataTable({
      lengthChange: false,
      pageLength: 100,
      sDom: 'ltipr'
    } );

    applySearchFunctionality(dataTableProfiles)
    applySearchFunctionality(dataTableGroups)

    $('.text-block-from-database').linkify();
    $('.profile').linkify();
    $('.info').linkify();
});

function applySearchFunctionality (datatable) {
  $("#filterbox").keyup(function() {
    datatable.search(this.value).draw();
  });
}

var selectors_with_old_style = [$('#id_local_groups'), $('#id_available_as_speaker')]
selectors_with_old_style.forEach(function(selector) {
  selector.removeClass('selectmultiple').addClass('form-control multiselect-form')
})

// add setting for all multiselect forms
$('.multiselect-form').multiselect({
  numberDisplayed: 1
});

var menu_btn = document.getElementById('burger-btn')
var navbar = document.getElementById('navbar')
menu_btn.addEventListener('click', function() {
  navbar.style.display = navbar.style.display == 'inline-block' ? 'none' : 'inline-block';
})

let claim_group = {
  toggle_btn: document.getElementById('claim_group_toggle'),
  confirm_field: document.getElementById('claim_group_confirm_field'),
  togglers: document.getElementsByClassName('claim_group_toggler')
}

let report_group_inactive = {
  toggle_btn: document.getElementById('report_group_inactive_toggle'),
  confirm_field: document.getElementById('report_group_inactive_confirm_field'),
  togglers: document.getElementsByClassName('report_group_inactive_toggler')
}

function toggleButton(obj) {
  for (let toggler of obj.togglers) {
    toggler.addEventListener('click', function() {
      obj.confirm_field.style.display = obj.confirm_field.style.display == 'block' ? 'none' : 'block';
      obj.toggle_btn.style.display = obj.toggle_btn.style.display == 'none' ? 'inline-block' : 'none';
    })
  }
}

toggleButton(claim_group)
toggleButton(report_group_inactive)
