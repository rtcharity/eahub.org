var profileClass = class {
  constructor(location, mapType) {
    this.label = location.label != undefined ? location.label : undefined
    this.anonymous = location.label != undefined ? false : true
    this.path = location.path != undefined ? location.path : undefined
    this.active = mapType == 'groups' ? true : undefined
  }
}
