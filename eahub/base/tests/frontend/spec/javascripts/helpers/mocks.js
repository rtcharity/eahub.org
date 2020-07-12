const londonLatLng = {lat: 50, lng: 0};
const klaipedaLatLng = {lat: 55, lng: 22};
const windenLatLng = {lat: 50, lng: 7};
const london1Mock = {label: 'London1', lat: londonLatLng.lat, lng: londonLatLng.lng, path: 'london-1', active: "True"};
const london2Mock = {label: 'London2', lat: londonLatLng.lat, lng: londonLatLng.lng, path: 'london-2', active: "False"};
const klaipeda1Mock = {label: 'Klaipeda1', lat: klaipedaLatLng.lat, lng: klaipedaLatLng.lng, path: 'klaipeda-1', active: "True"};
const klaipeda2Mock = {label: 'Klaipeda2', lat: klaipedaLatLng.lat, lng: klaipedaLatLng.lng, path: 'klaipeda-2', active: "False"};
const peterMock = {label: 'Peter', lat: londonLatLng.lat, lng: londonLatLng.lng, path: 'peter'};
const privateMock = {lat: londonLatLng.lat, lng: londonLatLng.lng};
const selectorInd = { checked: false };
const selectorGroups = { checked: false };
const spyOnGoogleMarker = jasmine.createSpy('googleMarker_setMap');
const addListenerMock = function(e, func) {
  return 'something'
}
const googleMarkerMock = class GoogleMarkerMock {
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
const googleSizeMock = class GoogleSizeMock {
  constructor(size1, size2) {
    this.size1 = size1,
    this.size2 = size2
  }
}
const googleMapMock = class GoogleMapMock {
  constructor(map, mapOptions) {
    this.map = map
    this.mapOptions = mapOptions
  }
}
const latLngMock = class LatLngMock {
  constructor(lat, lng) {
    this.lat = lat
    this.lng = lng
  }
}
const eventListenerMock = class {
  constructor(markerCluster, event, func) {
    this.event = event
  }
}
const infoWindowMock = class {
  constructor() {
    return 'infoWindowMock'
  }
}
const googleMock = {
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
};
const markerClustererMock = class {
  constructor(map, markers, options) {
    this.map = map,
    this.markers = markers
    this.options = options
  }
}


export default {
  profileClassMock: class ProfileClassMock {
    constructor(location, type) {
      this.location = location
      this.type = type
    }
  },
  spyOnGoogleMarker: spyOnGoogleMarker,
  markerClassMock: class MarkerClassMock {
    constructor(mapMock, locationMock, profilesMock, z) {
      this.location = locationMock
      this.googleMarker = {
        setMap: spyOnGoogleMarker
      }
      this.z = z
    }
  },
  klaipedaLatLng: klaipedaLatLng,
  londonLatLng: londonLatLng,
  london1Mock: london1Mock,
  london2Mock: london2Mock,
  klaipeda1Mock: klaipeda1Mock,
  klaipeda2Mock: klaipeda2Mock,
  peterMock: peterMock,
  privateMock: privateMock,
  locationsMock: {
    groups: [london1Mock, london2Mock, klaipeda1Mock, klaipeda2Mock],
    profiles: [peterMock],
    private_profiles: [privateMock]
  },
  activeProfileMock: {active: true, lat: 50, lng: 0},
  inactiveProfileMock: {active: false, lat: 50, lng: 0},
  htmlElementsMock: {
      selectorInd: selectorInd,
      selectorGroups: selectorGroups,
      map: 'mapElementMock'
  },
  markerSettingsMock: {
    image: {
      active: '/static/global/images/marker_active.svg',
      inactive: '/static/global/images/marker_inactive.svg'
    },
    size: {
      fullmap: { width: 40, height: 40 },
      profilemap: { width: 20, height: 23 }
    }
  },
  googleMock: googleMock,
  externalModulesMock: {
    google: googleMock,
    markerClusterer: markerClustererMock
  }
}
