import Vue from 'vue';
import InstantSearchPlugin from 'vue-instantsearch';
import App from './profile-edit.vue';
import $ from 'jquery';


window.jQuery = $;


Vue.use(InstantSearchPlugin);


const Widget = Vue.extend({
  render(createElement) {
    return createElement(App, {
      props: {
        algoliaApiKey: this.$el
          .parentElement.parentElement.getAttribute('data-algolia-api-key'),
        algoliaApplicationId: this.$el
          .parentElement.parentElement.getAttribute('data-algolia-application-id'),
        algoliaIndex: this.$el
          .parentElement.parentElement.getAttribute('data-algolia-index'),
        profilePk: this.$el
          .parentElement.parentElement.getAttribute('data-profile-pk'),
        typeName: this.$el
          .parentElement.getAttribute('data-type-name'),
        typeLabel: this.$el
          .parentElement.getAttribute('data-type-label'),
        searchResultsCols: this.$el
          .parentElement.getAttribute('data-search-results-cols')
        ,
      }
    })
  },
});
const nodes = document.querySelectorAll('.vue-profile-edit');
for (const node of nodes) {
  new Widget({el: node});
}
