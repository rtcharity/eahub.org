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

    var menu_btn = document.getElementById('burger-btn')
    var navbar = document.getElementById('navbar')

    applySearchFunctionality(dataTableProfiles)
    applySearchFunctionality(dataTableGroups)

    addSettingForMultiselectForms()

    toggleNavbar(navbar, menu_btn)
    disappearOnMovingCursorAway(navbar)
});

function applySearchFunctionality(datatable) {
  $("#filterbox").keyup(function() {
    datatable.search(this.value).draw();
  });
}

function addSettingForMultiselectForms() {
  var selectors_with_old_style = [$('#id_local_groups'), $('#id_available_as_speaker'), $('#id_open_to_job_offers'), $('#id_available_to_volunteer')]

  addMultiSelectClassTo(selectors_with_old_style)
  enableSearchForMultiselectFormsWithItemsMoreThan(10)
  $('.multiselect-form').multiselect({
    numberDisplayed: 1
  })
}

function addMultiSelectClassTo(selectors_with_old_style) {
  selectors_with_old_style.forEach(function(selector) {
    selector.removeClass('selectmultiple').addClass('form-control multiselect-form')
  })
}

function enableSearchForMultiselectFormsWithItemsMoreThan(num) {
  let className = 'select-with-more-than-'+num+'-items'
  addClassNameToMultiSelectFormsWithMoreThan(num, className)
  $('.' + className).multiselect({
    enableCaseInsensitiveFiltering: true
  })
}

function addClassNameToMultiSelectFormsWithMoreThan(num, className) {
  const multiselect_forms = document.getElementsByClassName('multiselect-form')
  for (var i=0; i < multiselect_forms.length; i++) {
    let multiselect_form = multiselect_forms[i]
    if (multiselect_form.length > num) multiselect_form.classList.add(className)
  }
}

function toggleNavbar(navbar, menu_btn) {
  menu_btn.addEventListener('click', function() {
    navbar.style.display = navbar.style.display == 'inline-block' ? 'none' : 'inline-block';
  })
}

function disappearOnMovingCursorAway(navbar) {
  navbar.onmouseout = function(event) {
    var element_left = event.target
    var element_new = event.relatedTarget
    if (element_new.className.includes('container') || element_new.id == 'body') {
      navbar.style.display = 'none'
    }
  }
}
