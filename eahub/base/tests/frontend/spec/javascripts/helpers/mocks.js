let profileClassMock = class ProfileClassMock {
  constructor(location, type) {
    this.location = location
    this.type = type
  }
}

let spyOnGoogleMarker = jasmine.createSpy('googleMarker_setMap')

let markerClassMock = class MarkerClassMock {
  constructor(mapMock, locationMock, profilesMock, z) {
    this.location = locationMock
    this.googleMarker = {
      setMap: spyOnGoogleMarker
    }
    this.z = z
  }
}

let addListenerMock = function(e, func) {
  return 'something'
}

let googleMarkerMock = class {
  constructor(props) {
    this.label = props.label
    this.setIcon = function(icon) {
      this.icon = icon
    }
    this.setMap = function(map) {
      this.map = map
    }
    this.addListener = addListenerMock
  }
}

let googleSizeMock = class {
  constructor(size1, size2) {
    this.size1 = size1,
    this.size2 = size2
  }
}

let googleMapMock = class {
  constructor(map, mapOptions) {
    this.map = map
    this.mapOptions = mapOptions
  }
}

let latLngMock = class {
  constructor(lat, lng) {
    this.lat = lat
    this.lng = lng
  }
}

let eventListenerMock = class {
  constructor(markerCluster, event, func) {
    this.event = event
  }
}

let infoWindowMock = class {
  constructor() {
    return 'infoWindowMock'
  }
}

let googleMock = {
  maps: {
    Marker: googleMarkerMock,
    Size: googleSizeMock,
    Map: googleMapMock,
    LatLng: latLngMock,
    event: {
      eventListener: eventListenerMock,
      addListener: addListenerMock
    },
    InfoWindow: infoWindowMock
  }
}

const londonLatLng = {lat: 50, lng: 0}
const klaipedaLatLng = {lat: 55, lng: 22}
const windenLatLng = {lat: 50, lng: 7}

let london1Mock = {label: 'London1', lat: londonLatLng.lat, lng: londonLatLng.lng, path: 'london-1', active: "True"}
let london2Mock = {label: 'London2', lat: londonLatLng.lat, lng: londonLatLng.lng, path: 'london-2', active: "False"}
let klaipeda1Mock = {label: 'Klaipeda1', lat: klaipedaLatLng.lat, lng: klaipedaLatLng.lng, path: 'klaipeda-1', active: "True"}
let klaipeda2Mock = {label: 'Klaipeda2', lat: klaipedaLatLng.lat, lng: klaipedaLatLng.lng, path: 'klaipeda-2', active: "False"}

let peterMock = {label: 'Peter', lat: londonLatLng.lat, lng: londonLatLng.lng, path: 'peter'}
let privateMock = {lat: londonLatLng.lat, lng: londonLatLng.lng}

let locationsMock = {
  groups: [london1Mock, london2Mock, klaipeda1Mock, klaipeda2Mock],
  profiles: [peterMock],
  private_profiles: [privateMock]
}

let activeProfileMock = {active: true, lat: 50, lng: 0}
let inactiveProfileMock = {active: false, lat: 50, lng: 0}

let selectorInd = { checked: false }
let selectorGroups = { checked: false }

let htmlElementsMock = {
    selectorInd: selectorInd,
    selectorGroups: selectorGroups,
    map: 'mapElementMock'
}

const markerSettingsMock = {
  image: {
    active: '/static/images/marker_active.svg',
    inactive: '/static/images/marker_inactive.svg'
  },
  size: {
    fullmap: { width: 40, height: 40 },
    profilemap: { width: 20, height: 23 }
  }
}

let markerClustererMock = class {
  constructor(map, markers, options) {
    this.map = map,
    this.markers = markers
    this.options = options
  }
}

let externalModulesMock = {
  google: googleMock,
  markerClusterer: markerClustererMock
}
