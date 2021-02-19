import Vue from 'vue';
import InstantSearchPlugin from 'vue-instantsearch';
import VTooltip from 'v-tooltip';
import App from './profile-edit.vue';


Vue.use(InstantSearchPlugin);
Vue.use(VTooltip);


const Widget = Vue.extend({
    render(createElement) {
        return createElement(App, {
            props: {
                algoliaApiKey: this.$el.parentElement.getAttribute('algolia-api-key'),
                algoliaApplicationId: this.$el.parentElement.getAttribute('algolia-application-id'),
                algoliaIndex: this.$el.parentElement.getAttribute('algolia-index'),
                type: this.$el.parentElement.getAttribute('type'),
                typeFieldName: this.$el.parentElement.getAttribute('type-field-name'),
                typeName: this.$el.parentElement.getAttribute('type-name'),
                profilePk: eval(this.$el.parentElement.getAttribute('profile-pk')),
            }
        })
    },
});
const nodes = document.querySelectorAll('.vue-profile-edit');
for (const node of nodes) {
    new Widget({el: node});
}
