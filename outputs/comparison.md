# Condition Comparison

## Summary

| Condition | Entries | Themes | Runtime | Preproc | LLM calls | In tokens | Out tokens | Embed tokens | Est. cost |
|-----------|---------|--------|---------|---------|-----------|-----------|------------|--------------|-----------|
| A: LLM Baseline | 500 | 5 | 49.5s | 0.0s | 1 | 41,917 | 942 | 0 | $0.0069 |
| B: BERTopic + LLM Labels | 500 | 12 | 24.4s | 15.3s | 1 | 828 | 472 | 0 | $0.0004 |
| C: BERTopic + LLM Labels + LFE | 500 | 12 | 77.2s | 22.3s | 1 | 17,643 | 1,089 | 0 | $0.0033 |
| D: Hierarchical + LLM Labels | 500 | 20 | 57.8s | 0.2s | 21 | 9,152 | 3,509 | 0 | $0.0035 |
| E: Hierarchical + LLM Labels + LFE | 500 | 20 | 82.6s | 12.9s | 21 | 22,819 | 4,294 | 0 | $0.0060 |

## Main Themes

### [A: LLM Baseline]
- Motherhood and Parenting
- Personal Growth and Challenges
- Family Dynamics
- Pets and Home Life
- Seasonal Changes and Nature

### [B: BERTopic + LLM Labels]
- 0_Childbirth Experience
- 1_Home Decor Gifts
- 5_Nature and Memory
- 2_Personal care experiences
- 9_Organizing baby essentials

### [C: BERTopic + LLM Labels + LFE]
- 0_Birth Experience Insights
- 1_Nursery and gift ideas
- 5_Nature and Reflection
- 2_Beauty and self-care
- 9_Organizing baby essentials

### [D: Hierarchical + LLM Labels]
- Chaos and Parental Humor
- Nostalgia and Parenting Insights
- Innocence and Embarrassment
- Overwhelmed by Chaos
- Sensory Comfort and Attachment

### [E: Hierarchical + LLM Labels + LFE]
- Parenting Challenges and Humor
- Curiosity and Wonder
- Childhood Innocence and Boundaries
- Chaos and Control
- Comfort in Scented Products

## Corpus Overview

### [A: LLM Baseline]
The journal corpus encompasses 500 entries covering a span of approximately two years, predominantly reflecting the journey of motherhood and parenting, which likely constitutes the largest thematic proportion. The next most significant theme is personal growth and challenges, with many entries highlighting experiences and reflections on mental health amidst parenting responsibilities. Family dynamics are also profoundly explored, showcasing the intricate relationships within your family. Pets and the whimsical aspects of home life serve as notable minority themes that bring a lighthearted perspective to everyday experiences. The overall compositional character of your writing is conversational, engaging, and infused with humor, often combining poignant reflections with humorous observations on the chaos of family life.

### [B: BERTopic + LLM Labels]
Your journal corpus consists of 500 entries spanning from January 5, 2009, to March 3, 2010. The predominant theme is the childbirth experience, comprising approximately 72.1% of the entries, indicating a significant focus on this life event and its surrounding emotions and experiences. Notable minority themes include home decor gifts (9.5%) and a variety of other subjects, such as personal care, winter reflections, family celebrations, and nature, each contributing a smaller but meaningful portion to your writing. Overall, your compositional character seems to reflect a deep engagement with familial and personal milestones, primarily centered around childbirth during this period, while also touching on a diverse range of experiences and reflections.

### [C: BERTopic + LLM Labels + LFE]
Your journal corpus consists of 500 entries spanning from January 5, 2009, to March 3, 2010. The dominant theme throughout this time was 'Birth Experience Insights', which made up approximately 72.1% of your entries, reflecting a strong preoccupation with the birth milestones and related experiences. Notable minority themes included 'Nursery and gift ideas' (9.5%), 'Beauty and self-care' (2.5%), and 'Family gatherings and celebrations' (2.5%), among others. The overall compositional character of your writing appears reflective and personal, with frequent engagement in self-inquiry and the exploration of emotions surrounding key life events.

### [D: Hierarchical + LLM Labels]
The corpus consists of 500 journal entries spanning from January 5, 2009, to March 3, 2010. The dominant theme throughout your writing is chaos and parental humor, which encompasses approximately 88% of your entries. Notable minority themes include appreciation of home and beauty, sensory comfort and attachment, and whimsy and playfulness, which collectively account for a modest 4% of the writing. The overall compositional character reflects a blend of humor amidst the chaos of parenting, showcasing how personal experiences—including stress and joy—intertwine with daily observations and reflections.

### [E: Hierarchical + LLM Labels + LFE]
Your journal corpus comprises 500 entries penned over a time span from January 5, 2009, to March 3, 2010. The dominant theme throughout your writings is 'Parenting Challenges and Humor,' accounting for approximately 88% of all entries. Notable minority themes include 'Appreciation of Home and Beauty' and 'Comfort in Scented Products,' though these represent a much smaller portion at 2.2% and 1.4%, respectively. The overall compositional character of your writing reflects a blend of humor and light-heartedness amid the often chaotic and challenging nuances of parenting.

## Synthesis

### [A: LLM Baseline]
Over time, the dominant themes of motherhood, personal growth, and family dynamics deeply intertwine with your writing style, which remains conversational and humorous throughout. As your experiences as a parent accumulate, the reflections grow more nuanced, with emotional layers accompanying the humor. This suggests a capacity to navigate the complexities of life while recognizing and articulating personal challenges, which may reflect a journey of resilience in the face of the demands of motherhood.

### [B: BERTopic + LLM Labels]
The dominant theme of the childbirth experience may reflect intense emotional and psychological engagement during this life transition, possibly coinciding with changes in writing style as other themes begin to emerge in the later entries. The absence of linguistic feature extraction data limits the ability to draw more nuanced connections between these themes and stylistic shifts, making it speculative to assert any specific patterns in the writing register during this period.

### [C: BERTopic + LLM Labels + LFE]
The sustained emphasis on 'Birth Experience Insights' throughout the corpus corresponds with a generally low negation rate and steady first-person usage, suggesting a confident exploration of personal experiences related to childbirth. However, as additional themes emerged, particularly in the latter part of the observed period, fluctuations in negation and uncertainty rates may reflect shifting emotional states and a broader engagement with life beyond the immediate experience of parenthood. This could suggest an evolving identity in response to new roles and responsibilities.

### [D: Hierarchical + LLM Labels]
The pattern of chaos and parental humor is distinctly marked throughout the entirety of your writing and aligns with a perceived ongoing engagement in the challenges and joys of parenting. The lack of linguistic feature extraction data may limit the understanding of stylistic shifts that could further illuminate emotional undercurrents, yet the recurring themes may suggest a deep engagement with both the turmoil and humor found in daily life as a parent.

### [E: Hierarchical + LLM Labels + LFE]
The sustained focus on 'Parenting Challenges and Humor' throughout the corpus coincided with relatively consistent first-person pronoun usage, averaging around 0.063, indicating a deeply personal engagement with the subject matter. The fluctuations in negation rates, particularly the increase to 0.025 in early 2010, may suggest escalating internal conflicts or more critical reflections as your experiences in parenting evolved.

## Limitations

### [A: LLM Baseline]
- This analysis focuses solely on thematic content without incorporating quantifiable linguistic features.
- There may be subjective interpretations of themes that can vary based on individual reader perspectives.
- The emotional or psychological interpretations suggested are speculative and may not fully capture the writer's intent.

### [B: BERTopic + LLM Labels]
- No linguistic feature extraction data available for assessing writing style.
- The theme boundary definitions may introduce ambiguity in understanding theme transitions.
- Limited exploration of psychological aspects due to the absence of contextual factors in the entries.

### [C: BERTopic + LLM Labels + LFE]
- Data gaps may exist in emotional expression due to the overall dominance of a single theme.
- The constraints of LFE metrics may not fully capture the complexities of emotional and psychological states.
- The ambiguity in theme boundaries may lead to underrepresentation or overrepresentation of emerging life experiences.

### [D: Hierarchical + LLM Labels]
- No linguistic feature extraction data available, limiting insights into writing style changes.
- Potential ambiguity in theme boundaries, particularly among minor themes.
- The analysis covers only a snapshot of entries, which may not capture complete contextual or emotional nuances.

### [E: Hierarchical + LLM Labels + LFE]
- The corpus has a significant imbalance in thematic representation, which may skew interpretations of emotional states.
- There are gaps in data for certain months, particularly in the nuanced exploration of less dominant themes.
- Linguistic metrics may not fully account for the emotional complexity or intent behind specific entries.
