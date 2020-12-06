import {SearchClient} from 'algoliasearch/dist/algoliasearch-lite';
import {Provide} from 'vue-property-decorator';
import {Vue, Component, Prop} from 'vue-property-decorator';
import algoliasearch from 'algoliasearch/lite';
import VueObserveVisibility from 'vue-observe-visibility';
import { history as historyRouter } from 'instantsearch.js/es/lib/routers';
import { singleIndex as singleIndexMapping } from 'instantsearch.js/es/lib/stateMappings';


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
        router: historyRouter(),
        stateMapping: singleIndexMapping('profiles'),
    }
    @Provide() profileEmptyImages: URL[] = [];
    
    mounted() {
        for (const imageUrl of this.profileEmptyImagesRaw.split(',')) {
            this.profileEmptyImages.push(imageUrl as any as URL);
        }
    }
}
