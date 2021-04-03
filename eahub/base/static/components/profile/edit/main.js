import Vue from 'vue';
import InstantSearchPlugin from 'vue-instantsearch';
import App from './profile-tag-input.vue';
import $ from 'jquery';


window.jQuery = $;


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
