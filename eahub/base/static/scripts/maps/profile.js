class Profile {
  constructor(location, type) {
    this.label = location.label != undefined ? location.label : undefined
    this.anonymous = location.label != undefined ? false : true
    this.path = location.path != undefined ? location.path : undefined
    this.active = type == 'groups' ? location.active : undefined
  }
}

export { Profile }
