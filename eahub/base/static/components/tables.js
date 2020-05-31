import $ from 'jquery';
import 'datatables.net';
import 'datatables.net-dt/css/jquery.dataTables.css';


$(document).ready(() => {
  initTables();
})


function initTables() {
  const tables = new Tables($('#datatable-profiles'), $('#datatable-groups'), $('#datatable-talentsearch'));
  tables.applySearchFunctionalityToAllTables();
}


class Tables {

  constructor(dataTableProfilesHtmlElement, dataTableGroupsHtmlElement, dataTableTalentHtmlElement) {
    this.dataTableProfiles = this.createProfiles(dataTableProfilesHtmlElement);
    this.dataTableGroups = this.createGroups(dataTableGroupsHtmlElement);
    this.dataTableTalent = this.createTalent(dataTableTalentHtmlElement)
  }

  createProfiles(htmlElement) {
    return htmlElement.dataTable({
      order: [[1, 'asc']],
      columns: [
        { "orderable": false, "targets": 0 },
        null, // Name
        null, // City/Town
        null, // Country
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
    for (let datatable of [this.dataTableProfiles, this.dataTableGroups, this.dataTableTalent]) {
      if (!datatable) {
        return;
      }
      $("#filterbox").keyup(function() {
        datatable.fnFilter(this.value);
      });
    }
  }

  createTalent(dataTableTalentHtmlElement) {
    if (dataTableTalentHtmlElement.length === 0) {
      return;
    }
    const getColumnConfig = function(fieldName) {
      if (fieldName == 'image') {
        return {"orderable": false, "targets": 0};
      }

      const searchable = [
          'expertise_areas',
          'cause_areas',
          'city_or_town',
          'country',
      ].includes(fieldName);
      const orderable = [
          'name',
          'city_or_town',
          'country',
      ].includes(fieldName);

      return {"searchable": searchable, "orderable": orderable};
    };

    const columns = [];
    $('#datatable-talentsearch-headers th').each(function() {
      const columnConfig = getColumnConfig($(this).data('name'));
      columns.push(columnConfig);
    });

    return dataTableTalentHtmlElement.dataTable({
      order: [[1, 'asc']],
      columns: columns,
      lengthChange: false,
      pageLength: 100,
      sDom: 'ltipr'
    } );
  }
}
