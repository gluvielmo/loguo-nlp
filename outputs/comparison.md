# Condition Comparison

## Summary

| Condition | Entries | Themes | Runtime | Preproc | LLM calls | In tokens | Out tokens | Embed tokens | Est. cost |
|-----------|---------|--------|---------|---------|-----------|-----------|------------|--------------|-----------|
| A: LLM Baseline | 500 | 5 | 11.8s | 0.0s | 1 | 41,641 | 700 | 0 | $0.0067 |
| B: BERTopic + LLM Labels | 500 | 12 | 29.7s | 19.3s | 1 | 621 | 750 | 0 | $0.0005 |
| C: BERTopic + LLM Labels + LFE | 500 | 12 | 38.6s | 28.6s | 1 | 6,606 | 782 | 0 | $0.0015 |
| D: Hierarchical + LLM Labels | 500 | 20 | 59.6s | 0.1s | 21 | 8,859 | 3,755 | 0 | $0.0036 |
| E: Hierarchical + LLM Labels + LFE | 500 | 20 | 83.5s | 12.0s | 21 | 14,019 | 4,346 | 0 | $0.0047 |

## Main Themes

### [A: LLM Baseline]
- Parenthood and Motherhood
- Humor and Light-heartedness
- Home and Family Dynamics
- Personal Growth and Challenges
- Community and Social Connections

### [B: BERTopic + LLM Labels]
- 0_Childbirth Experience
- 1_Gift guide collection
- 5_Nature and Photography
- 2_Beauty and self-care
- 9_Organizing Baby Essentials

### [C: BERTopic + LLM Labels + LFE]
- 0_Personal childbirth experience
- 1_Nursery Design Inspiration
- 5_Nature and Reflection
- 2_Beauty and Personal Care
- 9_Organizing Baby Essentials

### [D: Hierarchical + LLM Labels]
- Parenting Challenges and Humor
- Nostalgia and Everyday Wonders
- Embarrassment and Innocence
- Frustration and Disruption
- Sensory Experiences and Comfort

### [E: Hierarchical + LLM Labels + LFE]
- Chaos of Parenthood
- Nostalgia and Adaptation
- Childhood Mischief and Discomfort
- Chaos and Control
- Nostalgia and Comfort through Scents

## Surprising Patterns

### [A: LLM Baseline]
- The journal reflects an increasing complexity in the author's relationships with her children, showing a deepening understanding of parenting.
- Despite the prevalent humor, there is a consistent reflection on mental health, highlighting the author’s efforts to maintain balance amidst chaos.
- The author displays a continual evolution in home management and organization, correlating it with emotional states and family dynamics.

### [B: BERTopic + LLM Labels]
- Despite being a period of significant life change, entries on Nature and Photography remained stable, suggesting that the journaler valued continuity in personal interests.
- The quick emergence of Gift guide collection entries indicates an adaptation to the baby-centric lifestyle, incorporating more broader family themes.
- The decline in humorous entries relating to the Vasectomy Experience was unexpected, signaling a potential re-evaluation of past decisions amid new parenting challenges.

### [C: BERTopic + LLM Labels + LFE]
- The theme of Beauty and Personal Care had entries that remained stable throughout, despite the focus shifting more towards childbirth.
- Surprisingly, the theme of Vasectomy humor appeared sporadically after a strong initial presence in early entries.
- Nature and Reflection emerged as an underrepresented theme with only 8 entries overall, reflecting perhaps a minimal connection to external environments during pregnancy.

### [D: Hierarchical + LLM Labels]
- The overwhelming prevalence of 'Parenting Challenges and Humor' indicates a strong coping mechanism through humor amid parenting stresses.
- The minimal entries under distress themes suggest either a high resilience or a lack of articulation regarding deeper emotional struggles.
- The occurrence of 'Nostalgia' themes, although low, indicates a reflective tendency alongside the immediate challenges of parenting.

### [E: Hierarchical + LLM Labels + LFE]
- Despite the overwhelming theme of chaos, there were moments of significant appreciation for beauty and place that emerged.
- The low frequency of entries related to emotional manipulation suggests either a resolution of such dynamics or a significant shift in focus towards parenting.
- Unexpectedly, even in chaos, the writer maintained a consistent element of whimsical playfulness and imagination which is rarely noted in parenthood challenges.

## Reflection Questions

### [A: LLM Baseline]
1. What were the most significant turning points in my journey as a mother, and how did they shape my identity?
2. In what ways has humor served as a coping mechanism during challenging times in my life?
3. How have the dynamics in my family evolved over time with the addition of new members?

### [B: BERTopic + LLM Labels]
1. How has my identity as a parent evolved over this period?
2. What strategies have I employed to maintain self-care amid the challenges of new motherhood?
3. In what ways do I feel my creativity has been influenced or hindered by my responsibilities?

### [C: BERTopic + LLM Labels + LFE]
1. How did the experience of childbirth change my perception of personal care and aesthetics?
2. In what ways did my priorities shift once the baby arrived?
3. What were my hopes and fears surrounding motherhood as reflected in my writing?

### [D: Hierarchical + LLM Labels]
1. How have my experiences with parenting humor influenced my overall well-being?
2. What do the moments of nostalgia represent in my current life, and why are they so few?
3. How do I reconcile feelings of frustration in parenting with the moments of joy that accompany it?

### [E: Hierarchical + LLM Labels + LFE]
1. What are the specific chaotic moments that have shaped my parenting experience?
2. How can I harness my reflections on beauty and appreciation to enhance my daily life?
3. In what ways do my childhood experiences influence my parenting style?
