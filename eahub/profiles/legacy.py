from django_enumfield import enum


class CauseArea(enum.Enum):

    GLOBAL_HEALTH_AND_DEVELOPMENT = 1
    FARMED_ANIMAL_WELFARE = 2
    LONG_TERM_FUTURE = 3
    GLOBAL_PRIORITIES_RESEARCH = 4
    BUILDING_EA_COMMUNITIES = 5
    CLIMATE_CHANGE = 6
    MENTAL_HEALTH_AND_HAPPINESS = 7
    RATIONALITY = 8
    AI_SAFETY_AND_TECHNICAL_RESEARCH = 9
    AI_STRATEGY_AND_POLICY = 10
    BIORISK_STRATEGY_AND_POLICY = 11
    GLOBAL_COORDINATION_AND_PEACE = 12
    IMPROVING_INSTITUTIONAL_DECISIONS = 13
    WILD_ANIMAL_WELFARE = 14
    OTHER_POLICY_REFORMS = 15
    OTHER_EXISTENTIAL_RISKS = 16

    labels = {
        LONG_TERM_FUTURE: "Long-term future",
        GLOBAL_HEALTH_AND_DEVELOPMENT: "Global health and development",
        GLOBAL_PRIORITIES_RESEARCH: "Global priorities research",
        BUILDING_EA_COMMUNITIES: "Building EA communities",
        CLIMATE_CHANGE: "Climate change",
        MENTAL_HEALTH_AND_HAPPINESS: "Mental health/happiness",
        RATIONALITY: "Rationality",
        AI_SAFETY_AND_TECHNICAL_RESEARCH: "AI safety and technical research",
        AI_STRATEGY_AND_POLICY: "AI strategy and policy",
        BIORISK_STRATEGY_AND_POLICY: "Biorisk strategy and policy",
        GLOBAL_COORDINATION_AND_PEACE: "Global coordination and peace-building",
        IMPROVING_INSTITUTIONAL_DECISIONS: "Improving institutional decision-making",
        FARMED_ANIMAL_WELFARE: "Farmed animal welfare",
        WILD_ANIMAL_WELFARE: "Wild animal welfare",
        OTHER_POLICY_REFORMS: "Other policy reforms",
        OTHER_EXISTENTIAL_RISKS: "Other existential risks",
    }


class ExpertiseArea(enum.Enum):

    MANAGEMENT = 1
    OPERATIONS = 2
    RESEARCH = 3
    GOVERNMENT_AND_POLICY = 4
    ENTREPRENEURSHIP = 5
    SOFTWARE_ENGINEERING = 6
    AI_TECHNICAL_EXPERTISE = 7
    MATH_QUANT_STATS_EXPERTISE = 8
    ECONOMICS_QUANTITATIVE_SOCIAL_SCIENCE = 9
    MOVEMENT_BUILDING = 10
    COMMUNICATIONS = 11
    PHILOSOPHY = 12
    HUMANITIES = 13
    PSYCHOLOGY = 14
    PHYSICS = 15
    MEDICINE = 16
    OTHER_SCIENCE = 17
    EVENT_PLANNING = 18
    FINANCE = 19
    GRAPHIC_DESIGN = 20
    JOURNALISM = 21
    LAW = 22
    PHILANTHROPY_EARNING_TO_GIVE = 23
    PUBLIC_SPEAKING = 24
    RECRUITMENT = 25
    EDUCATION = 26
    QUANTITATIVE_TRADING = 27
    INFORMATION_SECURITY = 28
    PSYCHOLOGY_OF_DECISION_MAKING = 29

    labels = {
        MANAGEMENT: "Management",
        OPERATIONS: "Operations",
        RESEARCH: "Research",
        GOVERNMENT_AND_POLICY: "Government and policy",
        ENTREPRENEURSHIP: "Entrepreneurship",
        SOFTWARE_ENGINEERING: "Software engineering",
        AI_TECHNICAL_EXPERTISE: "AI technical expertise",
        MATH_QUANT_STATS_EXPERTISE: "Math/quant/stats expertise",
        ECONOMICS_QUANTITATIVE_SOCIAL_SCIENCE: "Economics/quantitative social science",
        MOVEMENT_BUILDING: "Movement building",
        COMMUNICATIONS: "Communications",
        PHILOSOPHY: "Philosophy",
        HUMANITIES: "Humanities",
        PSYCHOLOGY: "Psychology",
        PHYSICS: "Physics",
        MEDICINE: "Medicine",
        OTHER_SCIENCE: "Other science",
        EVENT_PLANNING: "Event planning and logistics",
        FINANCE: "Finance",
        GRAPHIC_DESIGN: "Graphic design",
        JOURNALISM: "Journalism",
        LAW: "Law",
        PHILANTHROPY_EARNING_TO_GIVE: "Philanthropy/earning to give",
        PUBLIC_SPEAKING: "Public speaking",
        RECRUITMENT: "Recruitment",
        EDUCATION: "Education",
        QUANTITATIVE_TRADING: "Quantitative Trading",
        INFORMATION_SECURITY: "Information Security",
        PSYCHOLOGY_OF_DECISION_MAKING: "Psychology of Decision Making",
    }


class GivingPledge(enum.Enum):

    GIVING_WHAT_WE_CAN = 1
    THE_LIFE_YOU_CAN_SAVE = 2
    ONE_FOR_THE_WORLD = 3
    FOUNDERS_PLEDGE = 4

    labels = {
        GIVING_WHAT_WE_CAN: "Giving What We Can",
        THE_LIFE_YOU_CAN_SAVE: "The Life You Can Save",
        ONE_FOR_THE_WORLD: "One for the World",
        FOUNDERS_PLEDGE: "Founders Pledge",
    }


class OrganisationalAffiliation(enum.Enum):

    EIGHTY_THOUSAND_HOURS = 1
    ANIMAL_CHARITY_EVALUATORS = 2
    BERI = 3
    CENTER_FOR_APPLIED_RATIONALITY = 4
    CENTER_FOR_HUMAN_COMPATIBLE_AI = 5
    CENTRE_FOR_EFFECTIVE_ALTRUISM = 6
    CSER = 7
    CHARITY_ENTREPRENEURSHIP = 8
    CHARITY_SCIENCE_HEALTH = 9
    FT_FOUNDATION = 10
    FOUNDATIONAL_RESEARCH_INSTITUTE = 11
    FOUNDERS_PLEDGE = 12
    FUTURE_OF_LIFE_INSTITUTE = 13
    GIVEWELL = 14
    GLOBAL_CATASTROPHIC_RISK_INSTITUTE = 15
    GLOBAL_PRIORITIES_INSTITUTE = 16
    LCFI = 17
    LOCAL_EFFECTIVE_ALTRUISM_NETWORK = 18
    MIRI = 19
    ONE_FOR_THE_WORLD = 20
    OPEN_PHILANTHROPY_PROJECT = 21
    RAISING_FOR_EFFECTIVE_GIVING = 22
    RETHINK_CHARITY = 23
    RETHINK_CHARITY_FORWARD = 24
    RETHINK_PRIORITIES = 25
    SENTIENCE_INSTITUTE = 26
    STIFTUNG_FUR_EFFEKTIVEN_ALTRUISMUS = 27
    STUDENTS_FOR_HIGH_IMPACT_CHARITY = 28
    THE_GOOD_FOOD_INSTITUTE = 29
    THE_LIFE_YOU_CAN_SAVE = 30
    WILD_ANIMAL_INITIATIVE = 31
    ALLFED = 32
    FUTURE_OF_HUMANITY_INSTITUTE = 33
    CENTRE_ON_LONG_TERM_RISK = 34
    ANIMAL_ETHICS = 35
    GIVING_WHAT_WE_CAN = 36
    LESS_WRONG = 37
    HAPPIER_LIVES_INSTITUTE = 38
    INNOVATIONS_FOR_POVERTY_ACTION = 39
    JPAL = 40
    APPG_FUTURE_GENERATIONS = 41
    CEEALAR = 42
    LEGAL_PRIORITIES_PROJECT = 43
    SENTIENCE_POLITICS = 44
    WANBAM = 45
    E_A_HUB = 46
    ANIMAL_ADVOCACY_CAREERS = 47
    AYUDA_EFECTIVA = 48
    DOEBEM = 49
    DONATIONAL = 50
    EFFECTIVE_ALTRUISM_FOUNDATION = 51
    EFFECTIVE_GIVING_UK_NETHERLANDS = 52
    EFFECTIV_SPENDEN = 53
    GENERATION_PLEDGE = 54
    GIEFFEKTIVT = 55
    GIVING_MULTIPLIER = 56
    HIGH_IMPACT_ATHLETES = 57
    LETS_FUND = 58
    SO_GIVE = 59
    ALPENGLOW = 60
    PROJEKT_FRAMTID = 61
    CENTRE_FOR_ELECTION_SCIENCE = 62
    ALBERT_SCHWEITZER_FOUNDATION = 63
    ANIMA_INTERNATIONAL = 64
    ANIMAL_ASK = 65
    AQUATIC_LIFE_INSTITUTE = 66
    CREDENCE_INSTITUTE = 67
    FARMED_ANIMAL_FUNDERS = 68
    FAUNALYTICS = 69
    FISH_WELFARE_INITIATIVE = 70
    THE_HUMANE_LEAGUE = 71
    AGAINST_MALARIA_FOUNDATION = 72
    CANOPIE = 73
    END_FUND = 74
    EVIDENCE_ACTION = 75
    FAMILY_EMPOWERMENT_MEDIA = 76
    FORTIFY_HEALTH = 77
    GIVEDIRECTLY = 78
    H_KELLER = 79
    IDINSIGHT = 80
    LEAD_EXPOSURE_ELIMINATION_PROJECT = 81
    MALARIA_CONSORTIUM = 82
    NEW_INCENTIVES = 83
    POLICY_ENTREPRENEURSHIP_NETWORK = 84
    SCI_FOUNDATION = 85
    SIGHTSAVERS_DEWORMING_PROGRAMME = 86
    SUVITA = 87
    OPIS = 88
    OUR_WORLD_IN_DATA = 89
    QUALIA_RESEARCH_INSTITUTE = 90
    GIVING_GREEN = 91
    HIGH_IMPACT_CAREERS_IN_GOVERNMENT = 92
    SPARKWAVE = 93

    labels = {
        EIGHTY_THOUSAND_HOURS: "80,000 Hours",
        ANIMAL_CHARITY_EVALUATORS: "Animal Charity Evaluators (ACE)",
        BERI: "Berkeley Existential Risk Initiative (BERI)",
        CENTER_FOR_APPLIED_RATIONALITY: "Center for Applied Rationality (CFAR)",
        CENTER_FOR_HUMAN_COMPATIBLE_AI: "Center for Human Compatible AI (CHAI)",
        CENTRE_FOR_EFFECTIVE_ALTRUISM: "Centre for Effective Altruism (CEA)",
        CSER: "Centre for the Study of Existential Risk (CSER)",
        CHARITY_ENTREPRENEURSHIP: "Charity Entrepreneurship",
        CHARITY_SCIENCE_HEALTH: "Charity Science Health",
        FT_FOUNDATION: "The Forethought Foundation for Global Priorities Research",
        FOUNDATIONAL_RESEARCH_INSTITUTE: "Foundational Research Institute (FRI)",
        FOUNDERS_PLEDGE: "Founders Pledge",
        FUTURE_OF_LIFE_INSTITUTE: "Future of Life Institute (FLI)",
        GIVEWELL: "GiveWell",
        GLOBAL_CATASTROPHIC_RISK_INSTITUTE: "Global Catastrophic Risk Institute (GCRI)",
        GLOBAL_PRIORITIES_INSTITUTE: "Global Priorities Institute (GPI)",
        LCFI: "Leverhulme Center for the Future of Intelligence (CFI)",
        LOCAL_EFFECTIVE_ALTRUISM_NETWORK: "Local Effective Altruism Network (LEAN)",
        MIRI: "Machine Intelligence Research Institute (MIRI)",
        ONE_FOR_THE_WORLD: "One for the World",
        OPEN_PHILANTHROPY_PROJECT: "Open Philanthropy Project",
        RAISING_FOR_EFFECTIVE_GIVING: "Raising for Effective Giving (REG)",
        RETHINK_CHARITY: "Rethink Charity",
        RETHINK_CHARITY_FORWARD: "Rethink Charity Forward",
        RETHINK_PRIORITIES: "Rethink Priorities",
        SENTIENCE_INSTITUTE: "Sentience Institute",
        STIFTUNG_FUR_EFFEKTIVEN_ALTRUISMUS: "Stiftung für Effektiven Altruismus",
        STUDENTS_FOR_HIGH_IMPACT_CHARITY: "Students for High Impact Charity",
        THE_GOOD_FOOD_INSTITUTE: "The Good Food Institute",
        THE_LIFE_YOU_CAN_SAVE: "The Life You Can Save (TLYCS)",
        WILD_ANIMAL_INITIATIVE: "Wild Animal Initiative",
        ALLFED: "Alliance to Feed the Earth in Disasters (ALLFED)",
        FUTURE_OF_HUMANITY_INSTITUTE: "Future of Humanity Institute (FHI)",
        CENTRE_ON_LONG_TERM_RISK: "Centre on Long-Term Risk (CLR)",
        ANIMAL_ETHICS: "Animal Ethics",
        GIVING_WHAT_WE_CAN: "Giving What We Can (GWWC)",
        LESS_WRONG: "Less Wrong",
        HAPPIER_LIVES_INSTITUTE: "Happier Lives Institute",
        INNOVATIONS_FOR_POVERTY_ACTION: "Innovations for Poverty Action (IPA)",
        JPAL: "Abdul Latif Jameel Poverty Action Lab (J-PAL)",
        APPG_FUTURE_GENERATIONS: "All-Party Parliamentary Group for Future Generations",
        CEEALAR: "Centre for Enabling EA Research and Learning (CEEALAR)",
        LEGAL_PRIORITIES_PROJECT: "Legal Priorities Project",
        SENTIENCE_POLITICS: "Sentience Politics",
        WANBAM: "WANBAM",
        E_A_HUB: "Effective Altruism Hub",
        ANIMAL_ADVOCACY_CAREERS: "Animal Advocacy Careers",
        AYUDA_EFECTIVA: "Ayuda Efectiva",
        DOEBEM: "Doebem",
        DONATIONAL: "Donational",
        EFFECTIVE_ALTRUISM_FOUNDATION: "Effective Altruism Foundation (EAF)",
        EFFECTIVE_GIVING_UK_NETHERLANDS: "Effective Giving UK/Netherlands",
        EFFECTIV_SPENDEN: "Effektiv-Spenden.org",
        GENERATION_PLEDGE: "Generation Pledge",
        GIEFFEKTIVT: "GiEffektivt.No",
        GIVING_MULTIPLIER: "Giving Multiplier.org",
        HIGH_IMPACT_ATHLETES: "High Impact Athletes",
        LETS_FUND: "Let's Fund",
        SO_GIVE: "So Give",
        ALPENGLOW: "Alpenglow",
        PROJEKT_FRAMTID: "Projekt Framtid",
        CENTRE_FOR_ELECTION_SCIENCE: "Centre for Election Science (CES)",
        ALBERT_SCHWEITZER_FOUNDATION: "Albert Schweitzer Foundation",
        ANIMA_INTERNATIONAL: "Anima International",
        ANIMAL_ASK: "Animal Ask",
        AQUATIC_LIFE_INSTITUTE: "Aquatic Life Institute",
        CREDENCE_INSTITUTE: "Credence Institute",
        FARMED_ANIMAL_FUNDERS: "Farmed Animal Funders",
        FAUNALYTICS: "Faunalytics",
        FISH_WELFARE_INITIATIVE: "Fish Welfare Initiative",
        THE_HUMANE_LEAGUE: "The Humane League",
        AGAINST_MALARIA_FOUNDATION: "Against Malaria Foundation (AMF)",
        CANOPIE: "Canopie",
        END_FUND: "END Fund (deworming programme)",
        EVIDENCE_ACTION: "Evidence Action (Deworm the World Initiative programme)",
        FORTIFY_HEALTH: "Fortify Health",
        GIVEDIRECTLY: "GiveDirectly",
        H_KELLER: "Hellen Keller International (Vitamin A supplementation programme)",
        IDINSIGHT: "IDInsight",
        FAMILY_EMPOWERMENT_MEDIA: "Family Empowerment Media",
        LEAD_EXPOSURE_ELIMINATION_PROJECT: "Lead Exposure Elimination Project (LEEP)",
        MALARIA_CONSORTIUM: "Malaria Consortium",
        NEW_INCENTIVES: "New Incentives",
        POLICY_ENTREPRENEURSHIP_NETWORK: "Policy Entrepreneurship Network",
        SCI_FOUNDATION: "SCI Foundation",
        SIGHTSAVERS_DEWORMING_PROGRAMME: "Sightsavers (deworming programme)",
        SUVITA: "Suvita",
        OPIS: "Organisation for the Prevention of Intense Suffering (OPIS)",
        OUR_WORLD_IN_DATA: "Our World in Data",
        QUALIA_RESEARCH_INSTITUTE: "Qualia Research Institute (QRI)",
        GIVING_GREEN: "Giving Green",
        HIGH_IMPACT_CAREERS_IN_GOVERNMENT: "High Impact Careers in Government (HIPE)",
        SPARKWAVE: "SparkWave",
    }
