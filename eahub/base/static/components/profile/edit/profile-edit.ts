import {SearchClient} from 'algoliasearch/dist/algoliasearch-lite';
import algoliasearch from 'algoliasearch/lite';
import axios from 'axios';
import Cookies from 'js-cookie';
import VueObserveVisibility from 'vue-observe-visibility';
import {Ref} from 'vue-property-decorator';
import {Provide} from 'vue-property-decorator';
import {Component, Prop, Vue} from 'vue-property-decorator';


Vue.use(VueObserveVisibility);


interface Tag {
    pk: number
    name: string
    types: [
        {type: string}
    ]
}


@Component
export default class ProfileEditComponent extends Vue {
    @Prop(String) algoliaApiKey: string;
    @Prop(String) algoliaApplicationId: string;
    @Prop(String) algoliaIndex: string;
    @Prop(String) type: string;
    @Prop(String) typeName: string;
    @Prop(String) typeFieldName: string;
    @Prop(Number) profilePk: number;

    @Provide() searchClient: SearchClient = algoliasearch(this.algoliaApplicationId, this.algoliaApiKey);
    @Provide() searchQuery: string = '';
    @Provide() tagsPksSelected: number[] = [];
    @Provide() tagsSelected: Tag[] = [];

    @Ref('typesRef') readonly typesRef;
    private profileUrl = `/profile/api/profiles/${this.profilePk}/`;

    async mounted() {
        const response = await axios.get(this.profileUrl);
        this.tagsSelected = response.data[this.typeFieldName];

        await this.sleep(300);
        this.typesRef.refine(this.type);
    }

    checkSearchTagInput(value) {
        console.log('change', value);
        if (value.includes(',')) {
            this.searchQuery = '';
        }
    }

    isSelected(pk: string): boolean {
        return Boolean(
            this.tagsSelected.find(tag => tag.pk === Number(pk))
        );
    }

    async remove(pkToDrop: number) {
        const tagsSelected = this.tagsSelected.filter(
            tag => tag.pk !== Number(pkToDrop)
        );
        try {
            let data = {};
            data[`${this.typeFieldName}_pks`] = tagsSelected.map(tag => tag.pk);
            const response = await axios.patch(
                this.profileUrl,
                data,
                {
                    headers: {
                        'X-CSRFToken': Cookies.get('csrftoken')
                    }
                }
            );
            console.log(response)
            this.tagsSelected = tagsSelected;
        } catch (e) {
            console.log(e);
        }
    }

    private async sleep(ms): Promise<any> {
        return new Promise(res => {
            setTimeout(res, ms);
        });
    }
}
