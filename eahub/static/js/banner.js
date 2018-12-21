var menu_burger = document.getElementById('menu_burger');
var drop_down_links = document.getElementById('drop_down_links');
menu_burger.onclick = function() {
  drop_down_links.style.visibility = drop_down_links.style.visibility == "visible" ? "hidden" : "visible";
}
