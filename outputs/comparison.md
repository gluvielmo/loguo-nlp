# Condition Comparison

## Summary

| Condition | Entries | Themes | Runtime | Preproc | LLM calls | In tokens | Out tokens | Embed tokens | Est. cost |
|-----------|---------|--------|---------|---------|-----------|-----------|------------|--------------|-----------|
| A: LLM Baseline | 500 | 5 | 36.0s | 0.0s | 1 | 41,917 | 976 | 0 | $0.0069 |
| B: BERTopic + LLM Labels + LFE | 500 | 12 | 86.4s | 50.9s | 1 | 14,298 | 1,242 | 0 | $0.0029 |
| C: Hierarchical + LLM Labels + LFE | 500 | 16 | 92.4s | 13.2s | 2 | 41,400 | 1,787 | 0 | $0.0073 |

## Main Themes

### [A: LLM Baseline]
- Parenthood
- Personal Growth and Reflection
- Humor and Everyday Life
- Pets and Home Life
- Creative Expression and Design

### [B: BERTopic + LLM Labels + LFE]
- Parenthood and Pregnancy
- Nursery design projects
- Life with Dogs
- Nature and Grief
- Hair and beauty experiences

### [C: Hierarchical + LLM Labels + LFE]
- Book Tour Preparations
- Parenting Experiences
- Seasonal Reflections
- Personal Style and Grooming
- Pregnancy and Labor Experiences

## Corpus Overview

### [A: LLM Baseline]
Spanning approximately one year, from January to December 2009, this journal corpus contains 500 entries. The predominant themes include Parenthood and Personal Growth and Reflection, which comprise about 70% of the content, often intertwined with Humor and Everyday Life, which makes up 20%. Notable minority themes include Pets and Home Life, and Creative Expression and Design, reflecting your diverse interests and experiences. The overall compositional character is conversational, engaging, and marked by an enthusiastic, stream-of-consciousness style, allowing for both humor and vulnerability as you navigate this transformative period in your life.

### [B: BERTopic + LLM Labels + LFE]
Your corpus comprises 500 journal entries spanning from January 5, 2009, to March 3, 2010. The dominant themes include Parenthood and Pregnancy (31.4% of entries) and Life with Dogs (21.8%), reflecting a significant focus on family and domestic life. Notable minority themes include Pregnancy and Relationships (9.0%) and Holiday Gift Guide (4.8%), among others, highlighting varying personal interests and experiences. Overall, the compositional character is rich and varied, with entries displaying a conversational tone reflecting personal reflections and interactions.

### [C: Hierarchical + LLM Labels + LFE]
Your journal corpus consists of 500 entries collected from January 5, 2009, to March 3, 2010. The dominant themes prominently include Pregnancy and Labor Experiences, which comprises approximately 25.2% of your entries, and Parenting Experiences, accounting for around 12.9%. Other significant yet marginal themes include Life With Dogs (9.2%) and Seasonal Reflections (8.9%), indicating a diverse range of interests. Overall, the compositional character of your writing is reflective and candid, combining personal experiences with narrative storytelling throughout various aspects of your life.

## Synthesis

### [A: LLM Baseline]
The dominant themes of Parenthood and Personal Growth throughout your writing reflect your journey through the complexities of motherhood, personal agency, and self-discovery. The humor woven into these experiences not only highlights the challenges faced but also serves as a coping mechanism, suggesting a speculative desire to maintain perspective amidst the chaos. Over time, the linguistic register transitions from excitement and curiosity to candid introspection, ultimately merging into a celebration of life’s small victories and artistic expressions. This evolution underscores your resilience and adaptability, offering insights into your psychological landscape during a transformative period.

### [B: BERTopic + LLM Labels + LFE]
The sustained focus on Parenthood and Pregnancy correlated with increased average word counts and a heightened use of direct questions, peaking at 0.144 during specific months, which may suggest an evolving conceptualization of roles within family life. The gradual decline in entries related to Life with Dogs alongside increased reflections on Parenting experiences implies a dynamic shift in your personal narrative, possibly reflecting changing responsibilities and emotional states as familial duties solidified.

### [C: Hierarchical + LLM Labels + LFE]
*(no synthesis)*

## Limitations

### [A: LLM Baseline]
- This analysis may not fully capture the nuance of individual entries due to the subjective nature of language interpretation.
- Potential biases in thematic categorization could overlook sub-themes or intersections between categories.
- The psychological interpretations suggested in the analysis are speculative and based on observable patterns rather than clinically validated insights.

### [B: BERTopic + LLM Labels + LFE]
- Data gaps may exist in entries that could affect the thematic understanding over time.
- The boundaries between themes could present ambiguities due to overlapping content.
- LFE metrics might confound interpretations of emotional tone versus entry content.

### [C: Hierarchical + LLM Labels + LFE]
