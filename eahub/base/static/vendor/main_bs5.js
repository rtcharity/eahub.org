window.bootstrap = require('bootstrap/dist/js/bootstrap.bundle.js');
require('./main.scss');

import 'cookieconsent/build/cookieconsent.min.css';

import '@fortawesome/fontawesome-free/js/fontawesome'
import '@fortawesome/fontawesome-free/js/solid'
import '@fortawesome/fontawesome-free/js/regular'
import '@fortawesome/fontawesome-free/js/brands'

import { library, dom } from '@fortawesome/fontawesome-svg-core';
import { faGlobe, faUserAstronaut, faSignInAlt, faUserPlus, faUser, faUsers, faBook, faExchangeAlt,
         faInfo, faComment, faSignOutAlt, faPencilAlt, faEnvelope, faSitemap, faBed, faFlag, faPlus,
         faLock, faMap, faDownload, faTrash, faEnvelopeSquare, faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons';

library.add(faUserAstronaut, faSignInAlt, faUserPlus, faUser, faUsers, faGlobe, faBook, faExchangeAlt,
faInfo, faComment, faSignOutAlt, faPencilAlt, faEnvelope, faSitemap, faFlag, faBed, faPlus, faLock, faMap,
faDownload, faTrash, faEnvelopeSquare, faExternalLinkAlt);

// Replace any existing <i> tags with <svg>
dom.i2svg();


import * as Sentry from "@sentry/browser";
import { Integrations } from "@sentry/tracing";

// todo move up before other scripts
Sentry.init({
    dsn: "https://f439be67331248918a9e6f35965bb6a6@o487305.ingest.sentry.io/5545929",
    integrations: [new Integrations.BrowserTracing()],
    tracesSampleRate: 1.0,
});
