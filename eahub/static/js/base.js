$(document).ready( function () {
    $('.enable-datatable').DataTable({
      "columnDefs": [
        { "orderable": false, "targets": 0 }
      ],
      lengthChange: false,
      pageLength: 100
    } );
} );

$('.text-block-from-database').linkify();
