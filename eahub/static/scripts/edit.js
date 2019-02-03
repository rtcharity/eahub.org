var privacy1_btn = document.getElementById('privacy-1')
var privacy2_btn = document.getElementById('privacy-2')

privacy1_btn.addEventListener('RadioStateChange', function() {
  console.log('change')
  console.log(privacy1_btn)
})
