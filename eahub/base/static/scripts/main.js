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

// add multiselect class to groups selection on profile/edit/community
$('#id_groups').removeClass('selectmultiple').addClass('form-control multiselect-form')

// add setting for all multiselect forms
$('.multiselect-form').multiselect({
  numberDisplayed: 1
});

var menu_btn = document.getElementById('burger-btn')
var navbar = document.getElementById('navbar')
menu_btn.addEventListener('click', function() {
  navbar.style.display = navbar.style.display == 'inline-block' ? 'none' : 'inline-block';
})
