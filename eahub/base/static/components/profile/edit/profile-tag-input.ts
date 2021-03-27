import {SearchClient} from 'algoliasearch/dist/algoliasearch-lite';
import algoliasearch from 'algoliasearch/lite';
import HttpService from 'eahub/base/static/components/services/http';
import {Ref} from 'vue-property-decorator';
import {Provide} from 'vue-property-decorator';
import {Component, Prop, Vue} from 'vue-property-decorator';


interface Tag {
    pk: number
    name: string
    count?: number
    types?: [
        {type: string}
    ]
    isLoading?: boolean
}


interface TagAlgolia {
    objectID: string
    name: string
    description: string
}


@Component
export default class ProfileTagInputComponent extends Vue {
    @Prop(String) algoliaApiKey: string;
    @Prop(String) algoliaApplicationId: string;
    @Prop(String) algoliaIndex: string;
    @Prop(String) typeLabel: string;
    @Prop(String) typeName: string;
    @Prop(Number) profilePk: number;
    @Prop(String) searchResultsCols: string;

    @Provide() searchClient: SearchClient = algoliasearch(this.algoliaApplicationId, this.algoliaApiKey);
    @Provide() searchQuery: string = '';
    @Provide() tagsPksSelected: number[] = [];
    @Provide() tagsSelected: Tag[] = [];
    @Provide() isShowResultsPopup: boolean = false;

    private hideResultsPopupEventName: string = 'hide-popup-background';

    @Ref('typesRef') readonly typesRef;
    private tagsUrl = `/profile/api/profiles/${this.profilePk}/`;
    private tagsCreateUrl = `/profile/api/profiles/tags/create/`;
    private http = new HttpService();

    async mounted() {
        const response = await this.http.get(this.tagsUrl);
        const tagsSelected = response.data[`tags_${this.typeName}`];
        tagsSelected.map(tag => tag.isLoading = false);
        this.tagsSelected = tagsSelected;

        this.$nextTick(() => {
            this.typesRef.refine(this.typeName);
        });
        this.initResultsPopupHandler();
    }

    async processTagSearchInput(value: string) {
        if (value.endsWith(',')) {
            this.searchQuery = '';
            const tagName = value.slice(0, -1);
            const tag = await this.createTag(tagName);
            await this.selectTag(tag);
        } else if (value.includes(',')) {
            this.searchQuery = '';
            for (const tagNameRaw of value.trim().split(',')) {
                const tagName = tagNameRaw.trim();
                if (tagName === "") {
                    continue
                }
                const tag = await this.createTag(tagName);
                await this.selectTag(tag);
            }
        }
    }

    async createTag(tagName: string): Promise<Tag> {
        const response = await this.http.post(
            this.tagsCreateUrl,
            {name: tagName, type: this.typeName},
        );
        const tag: Tag = response.data;
        tag.isLoading = false;
        return tag;
    }

    showResultsPopup() {
        const event = new Event(this.hideResultsPopupEventName);
        document.dispatchEvent(event);
        this.isShowResultsPopup = true;
    }

    initResultsPopupHandler() {
        document.addEventListener(this.hideResultsPopupEventName, () => {
            this.isShowResultsPopup = false;
        });
    }

    isSelected(pk: string): boolean {
        return Boolean(
            this.tagsSelected.find(tag => tag.pk === Number(pk))
        );
    }

    async selectTag(tagRaw: TagAlgolia | Tag) {
        const tag: Tag = {
            pk: Number(tagRaw['objectID']) || tagRaw['pk'],
            name: tagRaw.name,
            isLoading: true,
        };
        const tagsPksSelected = this.tagsSelected.map(tag => tag.pk);
        tagsPksSelected.push(tag.pk);
        this.tagsSelected.push(tag);
        try {
            let data = {};
            data[`tags_${this.typeName}_pks`] = tagsPksSelected;
            await this.http.patch(this.tagsUrl, data);
            tag.isLoading = false;
        } catch (e) {
            this.unselectTag(tag.pk);
            alert('An error occurred');
        }
        this.searchQuery = '';
    }

    async unselectTag(pkToDrop: number) {
        const tagToDrop = this.tagsSelected.find(tag => tag.pk === Number(pkToDrop));
        tagToDrop.isLoading = true;
        const tagsSelectedNew = this.tagsSelected.filter(
            tag => tag.pk !== Number(pkToDrop)
        );
        try {
            let data = {};
            data[`tags_${this.typeName}_pks`] = tagsSelectedNew.map(tag => tag.pk);
            await this.http.patch(this.tagsUrl, data);
            this.tagsSelected = tagsSelectedNew;
        } catch (e) {
            tagToDrop.isLoading = false;
            alert('An error occurred');
        }
    }
}
