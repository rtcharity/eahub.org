import {SearchClient} from 'algoliasearch/dist/algoliasearch-lite';
import algoliasearch from 'algoliasearch/lite';
import {history as historyRouter} from 'instantsearch.js/es/lib/routers';
import {singleIndex as singleIndexMapping} from 'instantsearch.js/es/lib/stateMappings';
import VueObserveVisibility from 'vue-observe-visibility';
import {Provide} from 'vue-property-decorator';
import {Component, Prop, Vue} from 'vue-property-decorator';


const SearchFilters = require('./components/search-filters.vue').default;


Vue.use(VueObserveVisibility);


@Component({
    components: {
        SearchFilters,
    },
})
export default class SearchComponent extends Vue {
    @Prop(String) algoliaApiKey: string;
    @Prop(String) algoliaApplicationId: string;
    @Prop(String) algoliaIndex: string;
    @Prop(String) profileEmptyImagesRaw: string;

    @Provide() isSearchPopupVisible: boolean = false;
    @Provide() searchClient: SearchClient = algoliasearch(this.algoliaApplicationId, this.algoliaApiKey);
    @Provide() searchQuery: string = '';
    @Provide() routing = {
        router: historyRouter({
            // an exact copy of the default createURL that drops pagination
            // and thus fixes #1034 
            // original code: https://github.com/algolia/instantsearch.js/blob/718bf458152bb55bab1efb542adb8e31298c0c3c/src/lib/routers/history.ts#L29
            createURL: ({qsModule, routeState, location}) => {
                delete routeState.page;

                const {protocol, hostname, port = '', pathname, hash} = location;
                const queryString = qsModule.stringify(routeState);
                const portWithPrefix = port === '' ? '' : `:${port}`;
                return `${protocol}//${hostname}${portWithPrefix}${pathname}?${queryString}${hash}`;
            },
        }),
        stateMapping: singleIndexMapping(this.algoliaIndex),
    }
    @Provide() profileEmptyImages: URL[] = [];
    
    mounted() {
        for (const imageUrl of this.profileEmptyImagesRaw.split(',')) {
            this.profileEmptyImages.push(imageUrl as any as URL);
        }
    }
}
