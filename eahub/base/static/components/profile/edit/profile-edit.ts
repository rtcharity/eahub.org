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
    @Provide() isShowPopupBackground: boolean = false;

    @Ref('typesRef') readonly typesRef;
    private tagsUrl = `/profile/api/profiles/${this.profilePk}/`;
    private tagsCreateUrl = `/profile/api/profiles/tags/create/`;
    private http = new HttpService();

    async mounted() {
        const response = await this.http.get(this.tagsUrl);
        this.tagsSelected = response.data[`tags_${this.typeName}`];

        // todo fix vue nextTick bug, ie from vrt
        await this.sleep(300);
        this.typesRef.refine(this.typeName);
        
        this.initPopupBackgroundHandler();
    }

    async processTagSearchInput(value: string) {
        if (value.endsWith(',')) {
            this.searchQuery = '';
            const tagName = value.slice(0, -1)
            const response = await this.http.post(
                this.tagsCreateUrl,
                {name: tagName, type: this.typeName},
            );
            const tag: Tag = response.data;
            await this.add(tag);
        } else if (value.includes(',')) {
            // todo handle
            console.error('invalid input')
        }
    }
    
    hidePopupBackground() {
        const event = new Event('hide-popup-background');
        document.dispatchEvent(event);
    }
    
    initPopupBackgroundHandler() {
        document.addEventListener('hide-popup-background', () => {
            this.isShowPopupBackground = false;
        });
    }

    isSelected(pk: string): boolean {
        return Boolean(
            this.tagsSelected.find(tag => tag.pk === Number(pk))
        );
    }

    async add(tagRaw: TagAlgolia | Tag) {
        const tag: Tag = {
            pk: Number(tagRaw['objectID']) || tagRaw['pk'],
            name: tagRaw.name,
        }
        const tagsPksSelected = this.tagsSelected.map(tag => tag.pk);
        tagsPksSelected.push(tag.pk);
        try {
            let data = {};
            data[`tags_${this.typeName}_pks`] = tagsPksSelected;
            await this.http.patch(this.tagsUrl, data);
        } catch (e) {
            console.error(e);
        }
        
        this.tagsSelected.push(tag);
        this.searchQuery = '';
    }
    
    async remove(pkToDrop: number) {
        const tagsSelectedNew = this.tagsSelected.filter(
            tag => tag.pk !== Number(pkToDrop)
        );
        try {
            let data = {};
            data[`tags_${this.typeName}_pks`] = tagsSelectedNew.map(tag => tag.pk);
            const response = await this.http.patch(this.tagsUrl, data);
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
