import {SearchClient} from 'algoliasearch/dist/algoliasearch-lite';
import {Ref} from 'vue-property-decorator';
import {Provide} from 'vue-property-decorator';
import {Component, Prop, Vue} from 'vue-property-decorator';
import algoliasearch from 'algoliasearch/lite';
import * as Sentry from '@sentry/browser';

import HttpService from 'eahub/base/static/components/services/http';


interface Tag {
    pk?: number
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
    @Prop(String) typeLabelShort: string = "";
    @Prop(String) typeName: string;
    @Prop(Number) profilePk: number;
    @Prop(String) searchResultsCols: string;
    @Prop(String) inputPopupIntro: string = "";

    @Provide() searchClient: SearchClient = algoliasearch(this.algoliaApplicationId, this.algoliaApiKey);
    @Provide() tagsPksSelected: number[] = [];
    @Provide() tagsSelected: Tag[] = [];
    @Provide() tagsToCreate: Tag[] = [];
    @Provide() isShowResultsPopup: boolean = false;
    @Provide() isLoadingInProgress: boolean = false;

    private hideResultsPopupEventName: string = 'hide-popup-background';

    @Ref('typesRef') readonly typesRef;
    @Ref('algoliaInput') readonly algoliaInput;
    private tagsUrl = `/profile/api/profiles/${this.profilePk}/`;
    private tagsCreateUrl = `/profile/api/profiles/tags/create/`;
    private http = new HttpService();

    async mounted() {
        const response = await this.http.get(this.tagsUrl);
        const tagsSelected = response.data[`tags_${this.typeName}`];
        tagsSelected.map(tag => tag.isLoading = false);
        this.tagsSelected = tagsSelected;
        
        this.initResultsPopupHandler();
        this.$nextTick(() => {
            this.typesRef.refine(this.typeName);
        });
    }

    async processTagSearchInput(value: string) {
        if (value.endsWith(',')) {
            this.algoliaInput.value = '';
            const tagName: string = value.slice(0, -1).trim();
            if (tagName === "") {
                return;
            }
            this.tagsToCreate.push({name: tagName});
            const tag = await this.createTag(tagName);
            this.tagsToCreate = [];
            await this.selectTag(tag);
            this.algoliaInput.focus();
        } else if (value.includes(',')) {
            this.algoliaInput.value = '';
            for (const tagNameRaw of value.trim().split(',')) {
                const tagName = tagNameRaw.trim();
                if (tagName === "") {
                    continue
                }
                this.tagsToCreate.push({name: tagName})
                const tag = await this.createTag(tagName);
                await this.selectTag(tag);
            }
            this.tagsToCreate = [];
            this.algoliaInput.focus();
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
        this.isLoadingInProgress = true;

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
        } catch (exc) {
            this.unselectTag(tag.pk);
            Sentry.captureException(
                exc,
                {
                    contexts: {
                        data: {
                            tagRaw: tagRaw,
                            tag: tag,
                            tagsSelected: this.tagsSelected,
                            typeName: this.typeName,
                            profilePk: this.profilePk,
                            responseRaw: JSON.stringify(exc.response),
                        },
                    } 
                }
            );
            alert(`An error occurred:\n ${exc}`);
        }
        tag.isLoading = false;
        this.algoliaInput.value = '';

        this.isLoadingInProgress = false;
    }

    async unselectTag(pkToDrop: number) {
        this.isLoadingInProgress = true;

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
        } catch (exc) {
            tagToDrop.isLoading = false;
            Sentry.captureException(
                exc,
                {
                    contexts: {
                        data: {
                            pkToDrop: pkToDrop,
                            tagsSelected: this.tagsSelected,
                            profilePk: this.profilePk,
                            responseRaw: JSON.stringify(exc.response),
                        },
                    } 
                }
            );
            alert(`An error occurred:\n ${exc}`);
        }
        
        this.isLoadingInProgress = false;
    }
}
