function addProfilePic(profilePic) {
  var profileImg = document.getElementById("profile-img")
  var randomAvatarNumber = randomIntegerBetween(1,50)
  if (profilePic == '') {
    profileImg.src = "/static/images/profile_avatars/avatar" + randomAvatarNumber + ".png"
  } else {
    profileImg.src = profilePic;
  }
}

function randomIntegerBetween(min, max) {
  return Math.floor(Math.random() * (max + 1 - min) + min);
}
