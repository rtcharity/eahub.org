$(document).ready( function () {
    console.log("database3")
    $('#enable-datatable').dataTable({
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
} );

$('.text-block-from-database').linkify();
