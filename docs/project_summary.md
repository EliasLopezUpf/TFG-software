# Project Summary

*Last updated: 2026-11-26. Sources: `CLAUDE.md`, `docs/TFG_Project_Summary_Claude_Code_Handover.docx` (Nov 2026), and inspection of the repository.*

## Concept

Data Science Bachelor's Thesis (TFG, UPF). It is a **data-driven feasibility study with a business-plan component** for a digital marketplace that connects senior citizens with activities, events and experiences. These are offered by municipalities, associations, *casals de gent gran*, civic and community centres, cultural organisations, sports and social clubs, and private organisers.

The deliverable is a rigorous feasibility study. A fully developed application is not necessarily part of it (to confirm with the tutor). The product format, value proposition and monetisation must **emerge from the research**: they are not predetermined.

## Central research question

> Is there a viable business opportunity for a marketplace connecting the senior population with activities and experiences adapted to their interests and needs?

## Scope

| Dimension | Current definition | Status |
|---|---|---|
| Geography | Catalonia | Working scope, following tutor guidance |
| Primary unit | Comarca | Working; municipal data used for detail, supply mapping and validation |
| Initial case | Costa Brava | Exploratory case only: **not** the market boundary |
| Target population | 60+ | **Provisional.** Compare 65+ and 75+. Demographic population ≠ customers. |

## Two-sided marketplace

- **Demand:** seniors who discover, compare and register for activities. To investigate: interests, participation, information channels, barriers, accessibility and mobility, digital preferences.
- **Supply:** organisers. To investigate: their offer, audience, visibility, dissemination needs, and willingness to participate in or pay for a platform.

## Roadmap (from the handover)

1. Define scope, research question, population and methodology with the tutor.
2. Demographic and territorial market analysis by comarca. ← **done** (notebooks 03–04); fieldwork comarques to agree with the tutor
3. Demand research: survey and interviews.
4. Activity supply and competitor research.
5. Synthesis into segments and an evidence-based value proposition.
6. MVP and two-sided value proposition.
7. Business model, acquisition, operations, partnerships.
8. Financial assumptions, scenarios, break-even, sensitivity.
9. Conclusions, limitations, future work.

## Current state (summary)

- **Done (exploratory, municipal level):** 2025 demographics (60+ by municipality), RFDB 2023 and ETCA 2024 for context, and a Costa Brava case study. See `docs/existing_work_review.md` for the full audit.
- **Done (comarca level, notebook 03):** 60+/65+/75+ size and share for 43 comarques (2025), threshold sensitivity, constant-boundary trends 2011/2021–2025, Idescat projections to 2049 (three scenarios), and RFDB/ETCA context.
- **Done (notebook 04):** context variables (living alone, urbanisation, IST, education), digital use by age (Catalonia, 16–74), five rule-based territorial profiles, proposed fieldwork comarques.
- **Done (notebook 05):** first supply exploration. Online visibility of activities in Baix Empordà, from open data and municipal websites.
- **Not started:** supply inventory (schema and pilot), survey and interviews, competitors, business model.

## Established facts (verified)

- Catalonia's census population on 1 Jan 2025 was 8,124,126, of whom 2,106,500 (25.93 %) were 60+ (Idescat census, notebook 01).
- 65+: 1,601,987 (19.72 %); 75+: 802,324 (9.88 %); 60–74: 1,304,176 (16.05 %) (notebook 03).
- Three comarques (Barcelonès, Vallès Occidental, Baix Llobregat) hold 51 % of Catalonia's 60+ residents; ten hold 76 %.
- 2021→2025 (constant boundaries): 60+ +8.7 % against +4.8 % for the total population; growth in all 43 comarques.
- Idescat projections 2025→2040: 60+ +31 % / +36 % / +42 % (low / medium / high); positive in every comarca.
- 28.1 % of people aged 75+ live alone (2021), about 205,000; Barcelonès 31.1 % (notebook 04).
- Ages 65–74, Catalonia 2025: 92.7 % used the internet in the last 3 months, but 36.1 % bought online (notebook 04).
- Baix Empordà: the open cultural agenda had 351 events in the last 12 months, none aimed at seniors (only 1 of 1,915 since 2018). Only 5 of 29 checked municipal websites link to a seniors or casal page (notebook 05).

## Observations (descriptive, exploratory)

- Small municipalities often have very high shares of 60+ residents (e.g. Colera 45 %, Portbou 41.5 %) but very small absolute numbers. Both absolute size and concentration matter.
- Costa Brava municipalities have a positive seasonal population load (ETCA). This is not age-specific.
- At comarca level, absolute size and senior share point to different territories (Spearman −0.58). The most aged comarques are small and interior, and their senior population grows slowly. The largest and fastest-growing senior populations are in the metropolitan ring and on the coast.
- The Costa Brava comarques are mid-sized senior markets with near-average shares: not demographically exceptional.

## Hypotheses (not yet tested)

- Seniors face information-discovery barriers for local activities.
- Organisers (especially small associations and casals) have limited channels for publicising activities.
- Large metropolitan comarques may face a *discovery* problem (abundant supply), while small aged interior comarques may face *scarce or poorly publicised supply and mobility* problems (from notebook 03, H1).
- Among 65–74, the digital barrier may be online *transactions* (booking, paying) rather than internet access (notebook 04, H4).
- Senior activities exist but are fragmented and hard to find online; casals may publicise mainly offline (notebook 05, H7–H8).
- *All must be investigated empirically; they are not assumed to be true.*

## Open questions for the tutor

- Is Catalonia + comarques the right boundary and unit?
- What methodological depth is expected for Data Science?
- Should there be street surveys and organiser interviews, and at what scale?
- Should the target threshold be 60+, 65+, 75+, or several exploratory thresholds?
- Is the deliverable a complete business plan, or a feasibility study with a business-plan component?
- Is a prototype required, or is a conceptual MVP enough?
