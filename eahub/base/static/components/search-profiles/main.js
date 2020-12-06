import Vue from 'vue';
import App from './search.vue';
import InstantSearchPlugin from 'vue-instantsearch';
import VTooltip from 'v-tooltip';


Vue.use(InstantSearchPlugin);
Vue.use(VTooltip);


const AppChild = Vue.extend({
    render(createElement) {
        return createElement(App, {
            props: {
                algoliaApiKey: this.$el.parentElement.getAttribute('algolia-api-key'),
                algoliaApplicationId: this.$el.parentElement.getAttribute('algolia-application-id'),
                algoliaIndex: this.$el.parentElement.getAttribute('algolia-index'),
                profileEmptyImagesRaw: this.$el.parentElement.getAttribute('profile-empty-images-raw'),
            }
        })
    },
});
new AppChild().$mount('.vue-search-component');
