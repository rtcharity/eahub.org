$(document).ready( function () {
    $('.enable-datatable').DataTable( {
      lengthChange: false,
      pageLength: 100
    } );
} );

$('.text-block-from-database').linkify();
