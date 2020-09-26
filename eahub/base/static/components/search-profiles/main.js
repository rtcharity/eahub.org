import Vue from 'vue';
import App from './search.vue';
import InstantSearchPlugin from 'vue-instantsearch';


Vue.use(InstantSearchPlugin);


const AppChild = Vue.extend({
    render(createElement) {
        return createElement(App, {
            props: {
                algoliaApiKey: this.$el.parentElement.getAttribute('algolia-api-key'),
                algoliaApplicationId: this.$el.parentElement.getAttribute('algolia-application-id'),
                algoliaIndex: this.$el.parentElement.getAttribute('algolia-index'),
            }
        })
    },
});
new AppChild().$mount('.vue-search-component');
