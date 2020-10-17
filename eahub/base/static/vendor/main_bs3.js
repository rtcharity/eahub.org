import 'bootstrap3';
import 'bootstrap3/dist/css/bootstrap.css';

import 'cookieconsent/build/cookieconsent.min.css';

import '@fortawesome/fontawesome-free/js/fontawesome'
import '@fortawesome/fontawesome-free/js/solid'
import '@fortawesome/fontawesome-free/js/regular'
import '@fortawesome/fontawesome-free/js/brands'

import { library, dom } from '@fortawesome/fontawesome-svg-core';
import { faGlobe, faUserAstronaut, faSignInAlt, faUserPlus, faUser, faUsers, faBook, faExchangeAlt,
         faInfo, faComment, faSignOutAlt, faPencilAlt, faEnvelope, faSitemap, faBed, faFlag, faPlus,
         faLock, faMap, faDownload, faTrash, faEnvelopeSquare } from '@fortawesome/free-solid-svg-icons';

library.add(faUserAstronaut, faSignInAlt, faUserPlus, faUser, faUsers, faGlobe, faBook, faExchangeAlt,
faInfo, faComment, faSignOutAlt, faPencilAlt, faEnvelope, faSitemap, faFlag, faBed, faPlus, faLock, faMap,
faDownload, faTrash, faEnvelopeSquare);

// Replace any existing <i> tags with <svg>
dom.i2svg();
