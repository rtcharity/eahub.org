let claim_group = {
  toggle_btn: document.getElementById('claim_group_toggle'),
  confirm_field: document.getElementById('claim_group_confirm_field'),
  togglers: document.getElementsByClassName('claim_group_toggler')
}

let report_group_inactive = {
  toggle_btn: document.getElementById('report_group_inactive_toggle'),
  confirm_field: document.getElementById('report_group_inactive_confirm_field'),
  togglers: document.getElementsByClassName('report_group_inactive_toggler')
}

let report_profile_abuse = {
  toggle_btn: document.getElementById('report_profile_abuse_toggle'),
  confirm_field: document.getElementById('report_profile_abuse_confirm_field'),
  togglers: document.getElementsByClassName('report_profile_abuse_toggler')
}

function toggleButton(obj) {
  for (let toggler of obj.togglers) {
    toggler.addEventListener('click', function() {
      obj.confirm_field.style.display = obj.confirm_field.style.display == 'block' ? 'none' : 'block';
      obj.toggle_btn.style.display = obj.toggle_btn.style.display == 'none' ? 'inline-block' : 'none';
    })
  }
}

toggleButton(claim_group)
toggleButton(report_group_inactive)
toggleButton(report_profile_abuse)
