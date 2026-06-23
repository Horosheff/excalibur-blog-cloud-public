# QA: B01 primer-seo-stati

date: 2026-06-10 (повтор после fix ссылок)
score_total: 95/100
core_eeat_lite: 20/20
link_verify: pass
verdict: PASS

## Scores

| Блок | Вес | Балл | Комментарий |
|------|-----|------|-------------|
| SEO structure | 20 | 20 | H2/H3, primary query, FAQ-структура, внутренние ссылки — OK |
| GEO / citability | 25 | 24 | Lead answer-first, таблица SEO vs GEO, 6 шагов, 7 FAQ, атомарные H2 |
| CORE-EEAT lite | 15 | 15 | 20/20 (см. ниже) |
| Human voice | 15 | 15 | 0 AI-slop hits, Flesch RU 74 |
| Fact safety | 15 | 13 | fact-check PASS; 8 чисел не в fact-bank (ориентиры объёма — допустимо); vague stat без имени источника |
| Contract HTML | 10 | 8 | linter PASS, объём 8897 ✓, CTA ≤3 ✓; −2 нет `<img>` с alt (рекомендация контракта) |

**Порог PASS:** ≥80, CORE-EEAT ≥16/20, link-verify pass — **выполнен**.

## CORE-EEAT lite: 20/20

| ID | ✓/✗ | Примечание |
|----|-----|------------|
| C01 | ✓ | H1/Title закрывают primary query |
| C02 | ✓ | Lead — direct answer, без «в этой статье» |
| C03 | ✓ | Аудитория: авторы блога, редакция |
| C04 | ✓ | SEO, GEO, llms.txt объяснены при первом появлении |
| O01 | ✓ | H2 совпадают с research-каркасом |
| O02 | ✓ | Логичный outline |
| O03 | ✓ | FAQ 7 пар, реальные queries |
| O04 | ✓ | ol (6 шагов), ul (чеклист), table |
| R01 | ✓ | ≥3 standalone блоков 40–60 слов |
| R02 | ✓ | Wordstat, Webmaster, llms.txt — с внешними ссылками |
| R03 | ✓ | Нет неподтверждённых %; «+140%» только как антипример |
| R04 | ✓ | FAQ: ответ в первом предложении |
| E01 | ✓ | Угол: единый SEO+GEO workflow, self-demo |
| E02 | ✓ | Практика в каждой H2 |
| E03 | ✓ | CTA services ×2, без перебора |
| Exp01 | ✓ | Режим B, без fake «я сделал» |
| Exp02 | ✓ | Тон brief, не generic AI |
| Exp03 | ✓ | 0 slop hits |
| Ept01 | ✓ | Ограничения названы честно |
| Ept02 | ✓ | CTA `example.com/#services` ×2 — HTTP 200 (fix подтверждён) |

## Script reports

| Скрипт | Verdict | Файл |
|--------|---------|------|
| fact-check | PASS | fact-check-report.json |
| link-verify | PASS | link-verify.json |
| html-linter | PASS | html-linter-report.json |
| slop-detector | PASS | slop-detector-report.json |
| cannibalization | PASS | cannibalization-report.json |

## Link verify

- total: 4, failed: 0
- OK: wordstat.yandex.ru, webmaster.yandex.ru, example.com/#services (×2), example.com/
- fix applied: `example.com/services/` → `example.com/#services` (2×)
- see `link-verify.json`

## AI-slop scan

- cliches: 0
- over-long sentences (>25 words): 5 (таблица/чеклист — допустимо для PASS slop-detector)
- Flesch RU: 74.0 (Easy)
- see `slop-detector-report.json`

## Fact-check

- verdict: pass (9 extracted, 1 verified in fact-bank, 8 unverified — ориентиры объёма/lead, не blocker)
- see `fact-check-report.json`

## Cannibalization

- verdict: pass (0 issues, 1 article in blog-dir)
- see `cannibalization-report.json`

## Fix cycle

- cycle 1: writer заменил `/services/` → `/#services`
- cycle 2: повтор GEO QA — PASS

## Optional (не blocker)

- добавить 1 `<img>` с alt по контракту
- уточнить «по данным исследований 2024 года» именем источника (ВЦИОМ) или оставить как в research-notes

## Schema ready (handoff для schema-агента)

BlogPosting: pending | FAQPage: yes (7) | HowTo: no | Review: no | E-E-A-T SameAs Author: pending (author_id: elena-kovaleva)
