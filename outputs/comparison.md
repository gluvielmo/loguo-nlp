# Condition Comparison

## Summary

| Condition | Entries | Themes | Runtime | Preproc | LLM calls | In tokens | Out tokens | Embed tokens | Est. cost |
|-----------|---------|--------|---------|---------|-----------|-----------|------------|--------------|-----------|
| A: LLM Baseline | 500 | 4 | 23.8s | 0.0s | 1 | 41,917 | 857 | 0 | $0.0068 |
| B: BERTopic + LLM Labels | 500 | 12 | 74.6s | 53.1s | 1 | 1,114 | 1,053 | 0 | $0.0008 |
| C: BERTopic + LLM Labels + LFE | 500 | 12 | 79.2s | 43.3s | 1 | 17,230 | 2,118 | 0 | $0.0039 |
| D: Hierarchical + LLM Labels | 500 | 20 | 71.0s | 1.0s | 21 | 28,219 | 3,634 | 0 | $0.0064 |
| E: Hierarchical + LLM Labels + LFE | 500 | 20 | 108.6s | 13.2s | 21 | 43,529 | 5,568 | 0 | $0.0099 |

## Main Themes

### [A: LLM Baseline]
- Motherhood and Parenting
- Home and Family Life
- Personal Growth and Health
- Humor and Everyday Life

### [B: BERTopic + LLM Labels]
- 0_Pregnancy and childbirth
- 8_Baby nursery project
- 1_Life with dogs
- 6_Nature and Grief
- 11_Hair and body care

### [C: BERTopic + LLM Labels + LFE]
- 0_Parenthood and childbirth
- 8_Nursery Design Projects
- 1_Life with dogs
- 6_Nature and Grief
- 11_Hair and beauty experiences

### [D: Hierarchical + LLM Labels]
- Joy and Personal Connection
- Parenting Challenges and Humor
- Nature and Transition
- Self-identity and confidence
- Transformation and Resilience

### [E: Hierarchical + LLM Labels + LFE]
- Joyful Anticipation and Nostalgia
- Parenting Challenges and Humor
- Nature and Emotional Reflection
- Self-Expression and Identity
- Maternal Transformation and Recovery

## Corpus Overview

### [A: LLM Baseline]
The journal spans from January 2009 to October 2010, encompassing over 500 entries. The dominant themes constitute approximately 50% of the corpus, with a strong focus on Motherhood and Parenting, complemented by Home and Family Life, accounting for about 30%. The remaining entries include themes of Personal Growth and Health as well as Humor, making up 10-20%. Overall, your writing blends observations of daily life with deeper reflections on personal experiences, characterized by an engaging, humorous, and often candid tone that invites readers into your world.

### [B: BERTopic + LLM Labels]
Your journal corpus encompasses 500 entries spanning from January 5, 2009, to March 3, 2010. The dominant theme throughout this period is pregnancy and childbirth, representing approximately 31.4% of your entries, followed by life with dogs at 21.8%. Additional minority themes include parenting and relationships, holiday gift guides, and travel experiences, among others. Overall, your writing demonstrates a personal, reflective character, heavily focused on significant life events and relationships, particularly those tied to family and the expectations of parenthood.

### [C: BERTopic + LLM Labels + LFE]
Your journal corpus consists of 500 entries spanning from January 5, 2009, to March 3, 2010. The dominant themes are centered around parenthood and childbirth, which collectively account for approximately 31.4% of your entries, and life with dogs at about 21.8%. Additional notable themes include pregnancy and parenthood, parental experiences, and holiday gift guides. The overall compositional character of your writing exhibits a narrative richness marked by emotional engagement and reflections on daily life dynamics.

### [D: Hierarchical + LLM Labels]
You wrote a total of 500 journal entries spanning from January 5, 2009, to March 3, 2010. The dominant themes throughout your writing were Transformation and Resilience (22.6%) and Parenting Challenges and Humor (11.6%), reflecting significant personal growth and the complexities of family life. Notable minority themes included Life with Pets (8.2%) and Nature and Transition (8.0%), indicating a connection to the environment and the companionship of animals. Overall, your compositional character appears to blend introspection with humor, capturing the myriad experiences of daily life.

### [E: Hierarchical + LLM Labels + LFE]
The journal corpus spans a total of 500 entries from January 5, 2009, to March 3, 2010. The writing centers primarily around maternal transformation and recovery, which accounts for approximately 22.6% of the entries, followed by several other significant themes, including parenting challenges and humor (11.6%) and chaos and playfulness in life (8.2%). Notable minority themes include emotional attachment to scent and ritual and anxiety and interpersonal conflict, each with a smaller proportion of entries. The overall compositional character leans towards a reflective and confessional style, often infused with humor and emotion, indicating a deep engagement with both personal and familial experiences.

## Synthesis

### [A: LLM Baseline]
The dominant themes of Motherhood and Parenting, Home Life, and Personal Growth bring forward a recurring dialogue about the joys and struggles of nurturing both children and self. Your evolving tone portrays both the heartfelt complexity and humor that characterize parenting, suggesting a journey that is both challenging and rewarding. Possible psychological reflections within these themes indicate an adaptive coping mechanism where humor serves as a significant tool for managing the pressures and joys of family life.

### [B: BERTopic + LLM Labels]
The prominence of themes like pregnancy and childbirth corresponded with a high rate of past-tense usage during mid-2009 (0.45), which may suggest a focus on experiences and anticipatory narratives. As you shifted to topics related to parenting and relationships, the uncertainty rate increased, possibly reflecting the complexities and evolving dynamics associated with your new role as a parent.

### [C: BERTopic + LLM Labels + LFE]
The dominant focus on parenthood and childbirth throughout the corpus coincided with a varying first-person pronoun ratio, which peaked at 0.074 in the early entries. This could reflect a growing personal engagement and emotional investment in these themes. The fluctuations in uncertainty rates, particularly during periods of increased focus on pregnancy and family life, may suggest a complex interplay of anticipation and apprehension in your experiences as a parent.

### [D: Hierarchical + LLM Labels]
The sustained focus on Transformation and Resilience along with Parenting Challenges and Humor signifies a blend of introspective and familial elements in your writing. One possible interpretation is that the absence of LFE data may mask variations in emotional tone or intensity as themes evolved, suggesting that deeper psychological nuances could be present despite stability in surface-level content.

### [E: Hierarchical + LLM Labels + LFE]
The narratives surrounding maternal transformation and recovery dominated the corpus, coinciding with elevated first-person pronoun usage (0.060) and a gradual increase in uncertainty rates, which may suggest an ongoing process of self-definition and emotional complexity related to motherhood. Simultaneously, parenting challenges and humor, even as it declined, remained impactful, especially reflected by occasional spikes in direct questioning (0.146), indicating that the writer engaged actively with the uncertainties of parenting in humorous ways. The interplay between chaotic themes and reflective self-expression throughout the entries could reflect a balancing act between maintaining humor and processing underlying emotional challenges.

## Limitations

### [A: LLM Baseline]
- This analysis primarily focuses on thematic exploration without delving into deeper emotional complexities.
- Longitudinal patterns may be influenced by external circumstances not reflected in the writing itself.
- The subjective nature of personal writing can lead to biased representations of experiences.

### [B: BERTopic + LLM Labels]
- Absence of linguistic feature extraction limits the analysis of nuanced shifts in writing style.
- Theme boundaries may overlap, making it challenging to delineate distinct experiences.
- Potential biases in the frequency of entries may not represent daily experiences accurately.

### [C: BERTopic + LLM Labels + LFE]
- The analysis relies solely on the written entries, which may not capture the full context of experiences.
- The clustering of themes may obscure nuanced individual experiences within overlapping areas.
- The fluctuating nature of LFE metrics could be influenced by life events not wholly described in the written entries.

### [D: Hierarchical + LLM Labels]
- Lack of linguistic feature extraction limits analysis of writing style and emotional expression.
- Themes were not explored within potentially overlapping categories, which may obscure finer distinctions.
- Insufficient context on external events during the timeframe may restrict understanding of influences on thematic shifts.

### [E: Hierarchical + LLM Labels + LFE]
- Potential gaps in the emotional depth of themes due to self-censorship in journaling.
- The temporal organization of themes may overlap and create boundaries that are not distinctly separable.
- LFE metrics may mask subtleties in narrative tone that are not solely quantitative.
