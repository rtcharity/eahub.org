$(document).ready( function () {
    $('#datatable-profiles').dataTable({
      order: [[1, 'asc']],
      columns: [
        { "orderable": false, "targets": 0 },
        null,
        null,
        null
      ],
      lengthChange: false,
      pageLength: 100
    } );

    $('#datatable-groups').dataTable({
      lengthChange: false,
      pageLength: 100
    } );
} );

$('.text-block-from-database').linkify();
