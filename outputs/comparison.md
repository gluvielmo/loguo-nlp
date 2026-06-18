# Condition Comparison

## Summary

| Condition | Entries | Themes | Runtime | Preproc | LLM calls | In tokens | Out tokens | Embed tokens | Est. cost |
|-----------|---------|--------|---------|---------|-----------|-----------|------------|--------------|-----------|
| A: LLM Baseline | 500 | 5 | 38.2s | 0.0s | 1 | 41,917 | 975 | 0 | $0.0069 |
| B: BERTopic + LLM Labels + LFE | 500 | 12 | 82.7s | 51.0s | 1 | 17,165 | 2,179 | 0 | $0.0039 |
| C: Hierarchical + LLM Labels + LFE | 500 | 20 | 106.5s | 12.9s | 21 | 43,569 | 5,353 | 0 | $0.0097 |

## Main Themes

### [A: LLM Baseline]
- Family Life and Parenting
- Personal Growth and Self-Reflection
- Daily Life and Humorous Observations
- Health and Wellbeing
- Social Interactions and Community

### [B: BERTopic + LLM Labels + LFE]
- Parenting and Birth Experience
- Nursery decoration project
- Life with pets
- Nature and Grief
- Hair and beauty experiences

### [C: Hierarchical + LLM Labels + LFE]
- Nesting and Personal Growth
- Parenting Challenges and Humor
- Transition and Reflection
- Self-Discovery and Self-Expression
- Transformation through motherhood

## Corpus Overview

### [A: LLM Baseline]
Spanning from January 2009 to October 2010, your writing corpus consists of approximately 500 entries. The dominant themes include family life and parenting, which constitute nearly half of the entries, followed by personal growth and self-reflection, which appear in about a quarter of the corpus. Daily life and humorous observations are also prominent, alongside health and wellbeing, and occasional social interactions, which add depth and variety to the overall narrative. The overall compositional character is marked by a conversational style, integrating humor and vulnerability, creating an engaging and relatable voice throughout your entries.

### [B: BERTopic + LLM Labels + LFE]
You produced 500 journal entries spanning from January 5, 2009, to March 3, 2010. The dominant themes in your writing were centered around Parenting and Birth Experience, which represented approximately 31.4% of entries, followed by Life with Pets at about 21.8%. Notable minority themes included Holiday Gift Guide and Nature and Grief, each making up around 4-5% of entries. Overall, your writing exhibited a personal and reflective character, with a noticeable focus on family life, personal challenges, and everyday experiences.

### [C: Hierarchical + LLM Labels + LFE]
The corpus consists of 500 journal entries spanning from January 5, 2009, to March 3, 2010. The dominant theme throughout this period is transformation through motherhood, comprising about 22.6% of the total entries. Other noteworthy themes include parenting challenges and humor (11.6%) and the joyful chaos of pet ownership (8.2%). Additionally, several stable themes are evident, including humor in parenting and family dynamics, reflective of a sustained focus on family and personal interactions. The overall compositional character reveals an engagingly reflective and humorous style, with fluctuations in thematic emphasis suggesting an adaptive writing process responding to life experiences.

## Synthesis

### [A: LLM Baseline]
Throughout your writing, the dominant themes of family life and personal growth are interwoven with humor and observational wit. As the corpus progresses from early motherhood into a deeper exploration of identity and community, the tonal shifts reflect your growing complexities in handling parenting responsibilities and self-awareness. The combination of these elements indicates a potential psychological development marked by introspection and adaptability, suggesting a nuanced understanding of the challenges and joys inherent in parenthood.

### [B: BERTopic + LLM Labels + LFE]
The dominant theme of Parenting and Birth Experience was notably accompanied by a high average of words per entry during early 2009, where peak engagement was evident in the emotional richness conveyed in your reflections. The fluctuating but persistent focus on Life with Pets may suggest a balancing act between personal responsibility and familial joy, with increased negation rates possibly reflecting internal conflict during pivotal moments of parenting. Overall, the blend of humor, relationship insights, and personal trials across themes indicates a complex narrative woven through your everyday life experiences.

### [C: Hierarchical + LLM Labels + LFE]
The sustained exploration of transformation through motherhood aligned with elevated word counts that culminated in August, suggesting an expansive engagement with this central theme. The consistent first-person pronoun ratios across entries indicate a personal and reflective narrative style, emphasizing individual experiences and emotions related to motherhood and family dynamics throughout the period.

## Limitations

### [A: LLM Baseline]
- The analysis is based solely on the selected corpus and may not represent the full range of experiences or insights available in your personal writing.
- Contextual factors outside of the entries, such as broader life events or emotional states, may influence the themes in ways not captured within the text.
- The analysis primarily focuses on dominant and marginal themes and does not deeply explore the intersectionality of these themes within your life experiences and societal contexts.

### [B: BERTopic + LLM Labels + LFE]
- Potential gaps in thematic representation due to varying interest levels over time.
- Uncertainty in interpreting the emotional content of entries without explicit context.
- Variability in entry length complicates comparisons of thematic depth across time.

### [C: Hierarchical + LLM Labels + LFE]
- Some themes may overlap, complicating thematic distinctions.
- The journal entries are subjective and may not represent a comprehensive view of the author's experiences.
- LFE metrics may not fully capture nuanced changes in emotional tone or complexity.
