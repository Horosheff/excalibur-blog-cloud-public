# Excalibur — CORE-EEAT lite (20 пунктов)

Упрощённый чеклист по мотивам [CORE-EEAT](https://github.com/aaron-he-zhu/core-eeat-content-benchmark) и [geo-content-optimizer](https://github.com/aaron-he-zhu/seo-geo-claude-skills).  
Excalibur GEO QA: минимум **16/20** Pass для overall PASS (иначе FIX_REQUIRED).

## Context & clarity (C)

| ID | Критерий | Pass |
|----|----------|------|
| C01 | H1/Title отражают primary query из `11-blog-topics.md` | ☐ |
| C02 | Первый абзац — direct answer без «в этой статье» | ☐ |
| C03 | Аудитория ясна (кто читатель, зачем ему это) | ☐ |
| C04 | Термины объяснены при первом появлении (40–60 слов) | ☐ |

## Organization (O)

| ID | Критерий | Pass |
|----|----------|------|
| O01 | H2/H3 совпадают с планом темы | ☐ |
| O02 | Заголовки образуют логичный outline | ☐ |
| O03 | FAQ 5–7, вопросы = реальные queries | ☐ |
| O04 | Списки/шаги для how-to, не сплошной текст | ☐ |

## Referenceability / GEO (R)

| ID | Критерий | Pass |
|----|----------|------|
| R01 | ≥3 standalone answer blocks (40–60 слов) | ☐ |
| R02 | ≥2 quotable факта с источником в research-notes | ☐ |
| R03 | Нет неподтверждённых процентов/цен | ☐ |
| R04 | FAQ answers citability-first (ответ в 1-м предложении) | ☐ |

## Exclusivity / angle (E)

| ID | Критерий | Pass |
|----|----------|------|
| E01 | Уникальный угол из research-notes (не клон топ-3 SERP) | ☐ |
| E02 | Практическая рекомендация в каждой H2-секции | ☐ |
| E03 | Бренд-CTA уместен, ≤3 упоминания | ☐ |

## Experience signals (Exp) — без фейков

| ID | Критерий | Pass |
|----|----------|------|
| Exp01 | Режим A/B соблюдён; нет fake «я сделал» | ☐ |
| Exp02 | Тон из brief/research, не generic AI | ☐ |
| Exp03 | AI-slop blocklist: ≤1 hit | ☐ |

## Expertise (Ept)

| ID | Критерий | Pass |
|----|----------|------|
| Ept01 | Ограничения/риски темы названы честно | ☐ |
| Ept02 | Internal links 2–3 из карточки темы | ☐ |

## Scoring

- **Pass item:** ☐ → ✓
- **Target:** 16+ ✓, нет veto (R03, Exp01, AI-slop ≥2)
- Запиши в `article-qa.md` секцию `## CORE-EEAT lite: N/20`
