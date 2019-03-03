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
} );

$('.multiselect-form').multiselect({
  numberDisplayed: 1
});

function applySearchFunctionality (datatable) {
  $("#filterbox").keyup(function() {
    datatable.search(this.value).draw();
  });
}

var menu_btn = document.getElementById('burger-btn')
var navbar = document.getElementById('navbar')
menu_btn.addEventListener('click', function() {
  navbar.style.display = navbar.style.display == 'inline-block' ? 'none' : 'inline-block';
})

var claim_group = document.getElementById('claim_group')
var claim_group_toggle = document.getElementById('claim_group_toggle')
var claim_group_togglers = document.getElementsByClassName('claim_group_toggler')

for (let toggler of claim_group_togglers) {
  toggler.addEventListener('click', function() {
    console.log(claim_group.style.display)
    claim_group.style.display = claim_group.style.display == 'block' ? 'none' : 'block';
    claim_group_toggle.style.display = claim_group_toggle.style.display == 'none' ? 'inline-block' : 'none';
  })
}
