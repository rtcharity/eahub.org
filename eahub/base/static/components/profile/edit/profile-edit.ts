import {SearchClient} from 'algoliasearch/dist/algoliasearch-lite';
import algoliasearch from 'algoliasearch/lite';
import {Ref} from 'vue-property-decorator';
import {Provide} from 'vue-property-decorator';
import {Component, Prop, Vue} from 'vue-property-decorator';
import HttpService from 'eahub/base/static/components/services/http';


interface Tag {
    pk: number
    name: string
    count?: number
    types?: [
        {type: string}
    ]
}


interface TagAlgolia {
    objectID: string
    name: string
    description: string
}


@Component
export default class ProfileEditComponent extends Vue {
    @Prop(String) algoliaApiKey: string;
    @Prop(String) algoliaApplicationId: string;
    @Prop(String) algoliaIndex: string;
    @Prop(String) typeLabel: string;
    @Prop(String) typeName: string;
    @Prop(Number) profilePk: number;

    @Provide() searchClient: SearchClient = algoliasearch(this.algoliaApplicationId, this.algoliaApiKey);
    @Provide() searchQuery: string = '';
    @Provide() tagsPksSelected: number[] = [];
    @Provide() tagsSelected: Tag[] = [];

    @Ref('typesRef') readonly typesRef;
    private profileUrl = `/profile/api/profiles/${this.profilePk}/`;
    private http = new HttpService();

    async mounted() {
        const response = await this.http.get(this.profileUrl);
        this.tagsSelected = response.data[`tags_${this.typeName}`];

        await this.sleep(300);
        this.typesRef.refine(this.typeName);
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

    async add(tagRaw: TagAlgolia) {
        const tag: Tag = {
            pk: Number(tagRaw.objectID),
            name: tagRaw.name,
        }
        const tagsPksSelected = this.tagsSelected.map(tag => tag.pk);
        tagsPksSelected.push(tag.pk);
        try {
            let data = {};
            data[`tags_${this.typeName}_pks`] = tagsPksSelected;
            const response = await this.http.patch(this.profileUrl, data);
            console.log(response)
        } catch (e) {
            console.log(e);
        }
        
        this.tagsSelected.push(tag);
    }
    
    async remove(pkToDrop: number) {
        const tagsSelectedNew = this.tagsSelected.filter(
            tag => tag.pk !== Number(pkToDrop)
        );
        try {
            let data = {};
            data[`tags_${this.typeName}_pks`] = tagsSelectedNew.map(tag => tag.pk);
            console.log(data);
            const response = await this.http.patch(this.profileUrl, data);
            console.log(response)
            this.tagsSelected = tagsSelectedNew;
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
