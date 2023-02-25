//import {SearchClient} from 'algoliasearch/dist/algoliasearch-lite';
//import algoliasearch from 'algoliasearch/lite';
//import {history as historyRouter} from 'instantsearch.js/es/lib/routers';
//import {singleIndex as singleIndexMapping} from 'instantsearch.js/es/lib/stateMappings';
import VueObserveVisibility from 'vue-observe-visibility';
import {Provide} from 'vue-property-decorator';
import {Component, Prop, Vue} from 'vue-property-decorator';

import HttpService from 'eahub/base/static/components/services/http';


//const SearchFilters = require('./components/search-filters.vue').default;     //TODO


Vue.use(VueObserveVisibility);


@Component
class SimilaritySearchUserData extends Vue {

    /*
    @Prop(String) url: string;
    @Prop(String) image: string;
    @Prop(Number) objectID: number;
    @Prop(String) name: string;
    @Prop(String) job_title: string;
    @Prop(Boolean) available_to_volunteer: boolean;
    @Prop(Boolean) open_to_job_offers: boolean;
    @Prop(Boolean) available_as_speaker: boolean;
    @Prop(Boolean) is_organiser: boolean;
    @Prop(String) country: string;
    @Prop(String) city: string;
    @Prop(String) messaging_url: string;
    @Prop(String) personal_website_url: string;
    @Prop(String) linkedin_url: string;
    @Prop(String) facebook_url: string;
    @Prop(Array) local_groups: string[] = [];
    @Prop(String) summary: string;
    @Prop(String) offering: string;
    @Prop(String) looking_for: string;
    @Prop(Array) expertise: string[] = [];
    @Prop(String) expertise_areas_other: string;
    @Prop(Array) cause_areas: string[] = [];  
    @Prop(String) cause_areas_other: string; 
    */

    //TODO later: remove dummy values for debugging
    @Prop(String) url: string = "url";
    @Prop(String) image: string = "image";
    @Prop(Number) objectID: number = 123;
    @Prop(String) name: string = "name";
    @Prop(String) job_title: string = "job_title";
    @Prop(Boolean) available_to_volunteer: boolean = true;
    @Prop(Boolean) open_to_job_offers: boolean = true;
    @Prop(Boolean) available_as_speaker: boolean = true;
    @Prop(Boolean) is_organiser: boolean = true;
    @Prop(String) country: string = "country";
    @Prop(String) city: string = "city";
    @Prop(String) messaging_url: string = "messaging_url";
    @Prop(String) personal_website_url: string = "personal_website_url";
    @Prop(String) linkedin_url: string = "linkedin_url";
    @Prop(String) facebook_url: string = "facebook_url";
    @Prop(Array) local_groups: string[] = ["local_groups 1", "local_groups 2"];
    @Prop(String) summary: string = "summary";
    @Prop(String) offering: string = "offering";
    @Prop(String) looking_for: string = "looking_for";
    @Prop(Array) expertise: string[] = ["expertise 1", "expertise 2"];
    @Prop(String) expertise_areas_other: string = "expertise_areas_other";
    @Prop(Array) cause_areas: string[] = ["cause_areas 2", "cause_areas 2"];  
    @Prop(String) cause_areas_other: string = "cause_areas_other";          
         
}


@Component({
    components: {
        //SearchFilters,
    },
})
export default class SimilaritySearchComponent extends Vue {
    @Prop(String) profileEmptyImagesRaw: string;
    @Prop(String) profilePk: string;

    /*
    //@Prop(String) algoliaApiKey: string;
    //@Prop(String) algoliaApplicationId: string;
    //@Prop(String) algoliaIndex: string;

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
        //stateMapping: singleIndexMapping(this.algoliaIndex),
    }
    */

    @Provide() profileEmptyImages: URL[] = [];

    @Provide() searchResults: SimilaritySearchUserData[] = [  
        new SimilaritySearchUserData(),     //TODO later: remove dummy data for debugging
        new SimilaritySearchUserData(),
        new SimilaritySearchUserData()
    ];  
    
    private similaritySearchUrl = `/profile/api/profiles/similaritySearch/?id=${escape(this.profilePk)}`;
    private http = new HttpService();

    async mounted() {
        const response = await this.http.get(this.similaritySearchUrl);
        this.searchResults = response.data;
        for (const [index, searchResult] of this.searchResults.entries()) {
            searchResult.objectID = index;
        }

        for (const imageUrl of this.profileEmptyImagesRaw.split(',')) {
            this.profileEmptyImages.push(imageUrl as any as URL);
        }
    }
}
