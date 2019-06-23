import $ from 'jquery';
import 'datatables.net';
import 'datatables.net-dt/css/jquery.dataTables.css';

export default class Tables {

  constructor(dataTableProfilesHtmlElement, dataTableGroupsHtmlElement) {
    this.dataTableProfiles = this.createProfiles(dataTableProfilesHtmlElement);
    this.dataTableGroups = this.createGroups(dataTableGroupsHtmlElement);
  }

  createProfiles(htmlElement) {
    console.log('createProfiles');
    return htmlElement.dataTable({
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
    return htmlElement.dataTable({
      lengthChange: false,
      pageLength: 100,
      sDom: 'ltipr'
    } );
  }

  applySearchFunctionalityToAllTables() {
    for (let datatable of [this.dataTableProfiles, this.dataTableGroups]) {
      $("#filterbox").keyup(function() {
        datatable.fnFilter(this.value);
      });
    }
  }
}
