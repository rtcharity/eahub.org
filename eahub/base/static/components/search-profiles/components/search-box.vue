<template>
    <div class="search__filters sticky-top">
        <ais-search-box
            v-model="searchQuery"
            :class-names="{
                'ais-SearchBox': 'search__search-box',
                'ais-SearchBox-input': 'form-control form-control-lg',
            }"
        />

        <div class="search__reset-box">
            <ais-current-refinements>
                <template slot="item"
                          slot-scope="{ refine, item, createURL, refinement }"
                >
                    <span class="search__reset-item-label">
                        {{ item.label.replaceAll('_', ' ') }}<span v-show="item.refinements[0].value !== 'true'">: </span>
                    </span>
                    <span v-for="refinement in item.refinements">
                        <slot name="refinement"
                              :refine="item.refine"
                              :refinement="refinement"
                              :createURL="createURL"
                        >
                            <span v-show="refinement.value !== 'true'">{{ refinement.label }}</span>
                            <button class="btn btn-outline search__reset-item-btn" @click="item.refine(refinement)">✕</button>
                        </slot>
                    </span>
                </template>
            </ais-current-refinements>

            <ais-clear-refinements>
                <template v-slot="{ canRefine, refine }">
                    <button
                        type="reset"
                        @click.prevent="refine"
                        v-show="canRefine"
                        class="ais-ClearRefinements-button btn btn-outline-primary btn-md"
                    >
                        <slot name="resetLabel">Clear all</slot>
                    </button>
                </template>
            </ais-clear-refinements>
        </div>

        <h4 class="search__filter-title">Status</h4>
        <div class="search__filter-item">
            <ais-toggle-refinement
                attribute="available_as_speaker"
                :label="'Available as a speaker'"
            />
        </div>
        <div class="search__filter-item">
            <ais-toggle-refinement
                attribute="available_to_volunteer"
                :label="'Available to volunteer'"
            />
        </div>
        <div class="search__filter-item">
            <ais-toggle-refinement
                attribute="open_to_job_offers"
                :label="'Open to job offers'"
            />
        </div>
        <div class="search__filter-item search__filter-item--with-title">
            <h4 class="search__filter-title">Country</h4>
            <ais-refinement-list
                attribute="country"
                searchable
                show-more
                :limit="5"
                :show-more-limit="20"
            />
        </div>
        <div class="search__filter-item search__filter-item--with-title">
            <h4 class="search__filter-title">City</h4>
            <ais-refinement-list
                attribute="city_or_town"
                searchable
                show-more
                :limit="5"
                :show-more-limit="20"
            />
        </div>
        <div class="search__filter-item search__filter-item--with-title">
            <h4 class="search__filter-title">Expertise</h4>
            <ais-refinement-list
                attribute="expertise"
                searchable
                show-more
                :limit="5"
                :show-more-limit="26"
            />
        </div>
        <div class="search__filter-item search__filter-item--with-title">
            <h4 class="search__filter-title">Career interest areas</h4>
            <ais-refinement-list
                attribute="career_interest_areas"
                searchable
                show-more
                :limit="5"
                :show-more-limit="26"
            />
        </div>
        <div class="search__filter-item search__filter-item--with-title">
            <h4 class="search__filter-title">Local groups</h4>
            <ais-refinement-list
                attribute="local_groups"
                searchable
                show-more
                :limit="5"
                :show-more-limit="25"
            />
        </div>
        <div class="search__filter-item search__filter-item--with-title">
            <h4 class="search__filter-title">Organisational affiliations</h4>
            <ais-refinement-list
                attribute="organisational_affiliations"
                searchable
                show-more
                :limit="5"
                :show-more-limit="25"
            />
        </div>
        <div class="search__filter-item search__filter-item--with-title">
            <h4 class="search__filter-title">Cause areas</h4>
            <ais-refinement-list attribute="cause_areas"/>
        </div>
        <div class="search__filter-item search__filter-item--with-title">
            <h4 class="search__filter-title">Giving pledges</h4>
            <ais-refinement-list attribute="giving_pledges"/>
        </div>
    </div>
</template>

<script>
    module.exports = {};
</script>
