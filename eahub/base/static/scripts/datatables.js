export default class Datatables {

  constructor(dataTableProfilesHtmlElement, dataTableGroupsHtmlElement) {
    this.dataTableProfiles = this.createProfiles(dataTableProfilesHtmlElement);
    this.dataTableGroups = this.createGroups(dataTableGroupsHtmlElement);
  }

  createProfiles(htmlElement) {
    return htmlElement.DataTable({
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
    });
  }

  createGroups(htmlElement) {
    return htmlElement.DataTable({
      lengthChange: false,
      pageLength: 100,
      sDom: 'ltipr'
    } );
  }

  applySearchFunctionality(datatable) {
    $("#filterbox").keyup(function() {
      datatable.search(this.value).draw();
    });
  }
}
