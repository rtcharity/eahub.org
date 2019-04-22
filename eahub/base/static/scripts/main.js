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
});

function applySearchFunctionality (datatable) {
  $("#filterbox").keyup(function() {
    datatable.search(this.value).draw();
  });
}

var selectors_with_old_style = [$('#id_local_groups'), $('#id_available_as_speaker'), $('#id_open_to_job_offers'), $('#id_available_to_volunteer')]
selectors_with_old_style.forEach(function(selector) {
  selector.removeClass('selectmultiple').addClass('form-control multiselect-form')
})

// add setting for all multiselect forms
$('.multiselect-form').multiselect({
  numberDisplayed: 1,
  enableCaseInsensitiveFiltering: true
});

var menu_btn = document.getElementById('burger-btn')
var navbar = document.getElementById('navbar')
menu_btn.addEventListener('click', function() {
  navbar.style.display = navbar.style.display == 'inline-block' ? 'none' : 'inline-block';
})
