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
  return null
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

let london1Mock = {label: 'London1', lat: londonLatLng.lat, lng: londonLatLng.lng, path: 'london-1', active: true}
let london2Mock = {label: 'London2', lat: londonLatLng.lat, lng: londonLatLng.lng, path: 'london-2', active: false}
let klaipeda1Mock = {label: 'Klaipeda1', lat: klaipedaLatLng.lat, lng: klaipedaLatLng.lng, path: 'klaipeda-1', active: true}
let klaipeda2Mock = {label: 'Klaipeda2', lat: klaipedaLatLng.lat, lng: klaipedaLatLng.lng, path: 'klaipeda-2', active: false}

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
  getElementById: function(id) {
    if (id === 'map_selector_ind') return selectorInd
    else if (id === 'map_selector_groups') return selectorGroups
    else if (id == 'map') return 'mapElementMock'
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
