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
} );

$('.text-block-from-database').linkify();

function applySearchFunctionality (datatable) {
  $("#filterbox").keyup(function() {
    datatable.search(this.value).draw();
  });
}
