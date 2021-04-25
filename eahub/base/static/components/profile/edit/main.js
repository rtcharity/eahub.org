import Vue from 'vue';
import InstantSearchPlugin from 'vue-instantsearch';
import App from './profile-tag-input.vue';
import $ from 'jquery';


window.jQuery = $;


initTagInputs();
initImportButtons();
initPopovers();


function initTagInputs() {
  Vue.use(InstantSearchPlugin);

  const Widget = Vue.extend({
    render(createElement) {
      return createElement(App, {
        props: {
          algoliaApiKey: DJANGO.algoliaApiKey,
          algoliaApplicationId: DJANGO.algoliaApplicationId,
          algoliaIndex: DJANGO.algoliaIndexName,
          profilePk: DJANGO.profilePk,
          typeName: this.$el
          .parentElement.getAttribute('data-type-name'),
          typeLabel: this.$el
          .parentElement.getAttribute('data-type-label'),
          typeLabelShort: this.$el
          .parentElement.getAttribute('data-type-label-short'),
          searchResultsCols: this.$el
          .parentElement.getAttribute('data-search-results-cols'),
          inputPopupIntro: this.$el
          .parentElement.getAttribute('data-input-popup-intro'),
        }
      })
    },
  });
  const nodes = document.querySelectorAll('.vue-profile-tag-input');
  for (const node of nodes) {
    new Widget({el: node});
  }
}


function initImportButtons() {
  const profileVisibilityInput = document.querySelector('[name="visibility"]');
  const profileForm = document.querySelector('#profile-update-form');

  document.querySelectorAll('.btn-submit-public').forEach(button => {
    button.addEventListener('click', () => {
      profileVisibilityInput.value = "public";
      profileForm.submit();
    });
  });
  document.querySelectorAll('.btn-submit-internal').forEach(button => {
    button.addEventListener('click', () => {
      profileVisibilityInput.value = "internal";
      profileForm.submit();
    });
  });
}


function initPopovers() {
  document.addEventListener('DOMContentLoaded', () => {
    for (const popoverElems of document.querySelectorAll('[data-bs-toggle="popover"]')) {
      new bootstrap.Popover(popoverElems);
    }
  });
}