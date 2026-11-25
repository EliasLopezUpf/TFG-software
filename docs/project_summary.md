# Project Summary

*Last updated: 2026-11-25. Sources: `CLAUDE.md`, `docs/TFG_Project_Summary_Claude_Code_Handover.docx` (Nov 2026), and inspection of the repository.*

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
2. Demographic and territorial market analysis by comarca. ← **next**
3. Demand research: survey and interviews.
4. Activity supply and competitor research.
5. Synthesis into segments and an evidence-based value proposition.
6. MVP and two-sided value proposition.
7. Business model, acquisition, operations, partnerships.
8. Financial assumptions, scenarios, break-even, sensitivity.
9. Conclusions, limitations, future work.

## Current state (summary)

- **Done (exploratory, municipal level):** 2025 demographics (60+ by municipality), RFDB 2023 and ETCA 2024 for context, and a Costa Brava case study. See `docs/existing_work_review.md` for the full audit.
- **Not started:** comarca analysis, trends and projections, supply inventory, survey, business model.

## Established facts (verified)

- Catalonia's census population on 1 Jan 2025 was 8,124,126, of whom 2,106,500 (25.93 %) were 60+ (Idescat census, notebook 01).
- 60–74: 16.05 %, 75–84: 6.85 %, 85+: 3.02 % of the population (shares only; see the review for the double-counting issue in the absolute counts).

## Observations (descriptive, exploratory)

- Small municipalities often have very high shares of 60+ residents (e.g. Colera 45 %, Portbou 41.5 %) but very small absolute numbers. Both absolute size and concentration matter.
- Costa Brava municipalities have a positive seasonal population load (ETCA). This is not age-specific.

## Hypotheses (not yet tested)

- Seniors face information-discovery barriers for local activities.
- Organisers (especially small associations and casals) have limited channels for publicising activities.
- *Both must be investigated empirically; they are not assumed to be true.*

## Open questions for the tutor

- Is Catalonia + comarques the right boundary and unit?
- What methodological depth is expected for Data Science?
- Should there be street surveys and organiser interviews, and at what scale?
- Should the target threshold be 60+, 65+, 75+, or several exploratory thresholds?
- Is the deliverable a complete business plan, or a feasibility study with a business-plan component?
- Is a prototype required, or is a conceptual MVP enough?
