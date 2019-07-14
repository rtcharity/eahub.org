import { CookieConsent } from 'cookieconsent';
document.addEventListener('DOMContentLoaded', () => {
  cookieconsent.initialise({
    "palette": {
      "popup": {
        "background": "#635274"
      },
      "button": {
        "background": "#A7DBAB",
        "text": "white"
      }
    },
    "content": {
      "href": "https://eahub.org/privacy-policy"
    }
  })
});
