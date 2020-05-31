import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';

import 'cookieconsent/build/cookieconsent.min.css';


import { library, dom } from '@fortawesome/fontawesome-svg-core';
import { faGlobe } from '@fortawesome/free-solid-svg-icons';
import { faUserAstronaut } from '@fortawesome/free-solid-svg-icons';
import { faSignInAlt } from '@fortawesome/free-solid-svg-icons';
import { faUserPlus } from '@fortawesome/free-solid-svg-icons';
import { faUser } from '@fortawesome/free-solid-svg-icons';
import { faUsers } from '@fortawesome/free-solid-svg-icons';
import { faBook } from '@fortawesome/free-solid-svg-icons';
import { faExchangeAlt } from '@fortawesome/free-solid-svg-icons';
import { faInfo } from '@fortawesome/free-solid-svg-icons';
import { faComment } from '@fortawesome/free-solid-svg-icons';
import { faSignOutAlt } from '@fortawesome/free-solid-svg-icons';


library.add(faUserAstronaut);
library.add(faSignInAlt);
library.add(faUserPlus);
library.add(faUser);
library.add(faUsers);
library.add(faGlobe);
library.add(faBook);
library.add(faExchangeAlt);
library.add(faInfo);
library.add(faComment);
library.add(faSignOutAlt);


// Replace any existing <i> tags with <svg>
dom.i2svg();
