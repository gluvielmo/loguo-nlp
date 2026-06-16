# Condition Comparison

## Summary

| Condition | Entries | Themes | Runtime | Preproc | LLM calls | In tokens | Out tokens | Embed tokens | Est. cost |
|-----------|---------|--------|---------|---------|-----------|-----------|------------|--------------|-----------|
| A: LLM Baseline | 500 | 5 | 12.9s | 0.0s | 1 | 41,641 | 674 | 0 | $0.0067 |
| B: LFE Only | 500 | 0 | 21.0s | 12.4s | 1 | 250 | 361 | 0 | $0.0003 |
| C: BERTopic + LLM Labels | 500 | 12 | 43.3s | 37.2s | 1 | 363 | 435 | 0 | $0.0003 |
| D: BERTopic + LLM Labels + LFE | 500 | 12 | 53.4s | 39.3s | 1 | 403 | 406 | 0 | $0.0003 |
| E: Hierarchical + LLM Labels | 500 | 20 | 62.4s | 0.1s | 21 | 8,591 | 3,620 | 0 | $0.0035 |
| F: Hierarchical + LLM Labels + LFE | 500 | 20 | 78.2s | 12.1s | 21 | 8,627 | 3,682 | 0 | $0.0035 |
| G: Hierarchical + Keywords | 500 | 20 | 8.2s | 0.2s | 1 | 432 | 402 | 0 | $0.0003 |
| H: Hierarchical + Keywords + LFE | 500 | 20 | 21.1s | 12.1s | 1 | 471 | 524 | 0 | $0.0004 |

## Main Themes

### [A: LLM Baseline]
- Parenthood
- Mental Health
- Home and Lifestyle
- Relationships
- Self-Discovery

### [B: LFE Only]

### [C: BERTopic + LLM Labels]
- 0_Personal birth journey
- 1_Nursery Design Inspirations
- 5_Nature and Personal Reflection
- 2_Personal care products
- 9_Organizing personal belongings

### [D: BERTopic + LLM Labels + LFE]
- 0_Personal Birth Experience
- 1_Gift Guide and Home Decor
- 5_Nature and Grief
- 2_Personal care products
- 9_Organizing Baby Gear

### [E: Hierarchical + LLM Labels]
- Chaos and Parenting Humor
- Nostalgia and Family Life
- Childhood Innocence and Awkwardness
- Frustration and Overwhelm
- Nostalgia and sensory comfort

### [F: Hierarchical + LLM Labels + LFE]
- Parenting Challenges and Humor
- Nostalgia and Distraction
- Childhood Innocence and Discomfort
- Frustration and Chaos
- Nostalgia and Comfort

### [G: Hierarchical + Keywords]
- jon / leta / baby
- hours / times / nuts
- taking / aren / uncomfortable
- outside / thinking / marlo
- lotion / wine / body

### [H: Hierarchical + Keywords + LFE]
- jon / leta / baby
- hours / times / nuts
- taking / aren / uncomfortable
- outside / thinking / marlo
- lotion / wine / body

## Surprising Patterns

### [A: LLM Baseline]
- The transformation in narrative voice seems to both soften and strengthen concurrently over time, indicating a balance between vulnerability and confidence.
- The journaler frequently shifts from humor to serious reflection, illustrating a dynamic approach to storytelling that captures the unpredictability of parenting.
- There is consistent engagement with mental health themes, revealing a commitment to self-awareness that deepens over time.

### [B: LFE Only]
- The relatively high average of negations per entry could indicate ongoing challenges or conflict, rather than a resolution-oriented mindset.
- A low first-person pronoun ratio suggests that the writer might be expressing feelings or experiences that are less about self-reflection and more about external circumstances.
- Despite an average of 253.8 words per entry, the focus on negations suggests that quantity of writing does not equal qualitative introspection.

### [C: BERTopic + LLM Labels]
- The overwhelming dominance of the birth journey theme suggests a singular focus that could overshadow other personal interests and experiences during this time.
- The low frequency of entries related to personal care products contrasts with the emotional weight of the birth journey, indicating possible neglect of self-care amid significant life events.
- Humor surrounding topics like pets and vasectomies appears surprisingly limited, which could suggest a more serious emotional undercurrent despite the humor's typical role in processing life changes.

### [D: BERTopic + LLM Labels + LFE]
- The frequency of the theme 'Nature and Grief' was notably low, despite potential life changes during this period that often provoke reflections on loss.
- Humor ('Vasectomy humor') made an appearance as a theme in a significant but minimal way, suggesting a coping mechanism for the journaler in dealing with family planning issues.
- The relatively low presence of family-oriented entries compared to personal experiences points to a potential isolation felt by the journaler, emphasizing personal introspection over community.

### [E: Hierarchical + LLM Labels]
- Despite the chaotic nature of parenting humor dominating the corpus, there were very few entries addressing deeper emotional struggles or psychological themes beyond surface-level observations.
- Nostalgia appears in various forms, yet most entries reflect a longing for family life rather than personal experiences, indicating the author's primary engagement with collective rather than individual nostalgia.
- Frustration and disdain appear in strikingly few entries considering the potentially overwhelming nature of parenting, suggesting either a coping mechanism at play or selective narration of experiences.

### [F: Hierarchical + LLM Labels + LFE]
- The overwhelming focus on Parenting Challenges and Humor, accounting for 88% of the entries, indicates an intense dedication to the intricacies of parenthood, overshadowing other themes.
- The low occurrences of themes such as Emotional Manipulation and Trust reflect a potential avoidance of deeper interpersonal conflicts, which might suggest a focus on humor as a coping mechanism.
- Despite only a handful of entries addressing nostalgia, the range of nostalgia-related themes reveals a complex interplay between memory and identity across various contexts.

### [G: Hierarchical + Keywords]
- A dominant theme revolves around the family dynamics and interactions, as indicated by frequent mentions of 'jon', 'leta', and 'baby', illustrating a strong focus on personal relationships during this period.
- The relatively low occurrence of entries about specific activities or hobbies, like 'taking', 'hours', and 'nuts', suggests a possible prioritization of family over personal leisure or individual interests.
- The presence of terms related to animals, like 'dogs' and 'walk', although less frequent, offers insight into the journaler's domestic environment and potentially comforting relationships with pets.

### [H: Hierarchical + Keywords + LFE]
- The overwhelming focus on 'jon', 'leta', and 'baby' in 440 entries indicates a strong emotional or developmental phase, possibly linked to parenthood or significant familial relationships.
- The low frequency of varied themes suggests either a highly concentrated emotional focus or a limitation in the journaler's experiences during this time.
- The very low presence of first-person pronouns (only 0.0615 ratio) indicates a tendency to focus on external subjects rather than personal introspection, despite the intimate nature of family themes.

## Reflection Questions

### [A: LLM Baseline]
1. How have my experiences as a parent shaped my understanding of self?
2. What recurring themes in my journaling reflect my evolving relationship with mental health?
3. In what ways have my friendships influenced my parenting style and overall happiness?

### [B: LFE Only]
1. What recurring themes or challenges do I notice in my writing over time?
2. How do my feelings of negativity correlate with the events happening in my life during this period?
3. In what ways can I reframe negative experiences to see them in a more positive light?

### [C: BERTopic + LLM Labels]
1. How did my personal birth journey influence my identity and relationships during this period?
2. In what ways can I balance preparation for significant life events with self-care and personal interests?
3. What insights do I gain from reflecting on my experiences and emotions related to nature during this year?

### [D: BERTopic + LLM Labels + LFE]
1. How did the significant themes of 'Personal Birth Experience' shape my identity during this time?
2. What elements of humor in coping were present during challenging experiences, and how have they evolved since?
3. In what ways did my reflections on grief relate to the joy found in other entries?

### [E: Hierarchical + LLM Labels]
1. How do you balance humor with the more serious challenges you face in parenting?
2. In what ways do your nostalgic feelings influence how you perceive your current family life?
3. What specific moments of chaos have made you feel most connected to your child?

### [F: Hierarchical + LLM Labels + LFE]
1. How has my perspective on parenting evolved since I began writing these entries?
2. What role does humor play in my daily challenges, and how does it help me cope?
3. Why do I find myself gravitating toward nostalgic reflections, and what do they reveal about my current state?

### [G: Hierarchical + Keywords]
1. How has the focus on family dynamics shaped my identity and priorities during this time?
2. What feelings or events prompted me to write about 'taking', 'hours', and 'uncomfortable' so infrequently?
3. In what ways have changes in my community affected my sense of self and my relationships with others?

### [H: Hierarchical + Keywords + LFE]
1. How have my relationships with 'jon' and 'leta' influenced my sense of self and my experiences during this time?
2. What might the recurring themes suggest about my priorities or concerns in this period of my life?
3. In what ways do I feel comfortable or uncomfortable in expressing my emotions in my writing?
