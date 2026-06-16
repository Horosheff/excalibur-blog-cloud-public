# Excalibur BLOG — фирменный концепт обложек

Excalibur BLOG создаёт **один узнаваемый визуальный язык** для всех обложек. Меняется только **сюжет темы**, не стиль.

## Два уровня

| Уровень | Файл | Что фиксирует |
|---------|------|----------------|
| **Концепт** | `memory/cover/cover-concept.md` + `.json` | Семья стиля, палитра, prefix/suffix промпта |
| **Тема** | `memory/cover/cover-prompts.json` | `topic_scene_descriptor` + alt |
| **Техника** | `memory/cover/cover-system.md` | 16:9, MCP, QA |

## Шаг 1 — выбор cover family

Один **primary** `cover_family` на весь блог.

Machine-readable реестр: `shared/blog-cover-family-registry.json` (**33 типа**). Используй **только** slug из реестра.

Обоснуй выбор в `cover-concept.md`: связь с `site-brief.md`, аудиторией, тип контента в `blog-topics.md`.

### Реестр типов (`cover_family`)

#### A. Коллаж и стикеры

| `cover_family` | Когда | Визуал |
|----------------|-------|--------|
| `brand_collage` | Яркий бренд, EdTech, playful | Слои cutout + цветные плашки + overlap |
| `sticker_scrapbook` | Молодая аудитория, DIY, креатив | Стикеры, скотч, torn edges, scrapbook |
| `geometric_blocks` | Современный tech, структура | Крупные геометрические блоки бренда, объект внутри |
| `paper_cutout` | Мягкий детский / craft | Бумажные слои, тени, рукодельная эстетика |
| `polaroid_grid` | Серия кейсов, «истории» | 2–3 polaroid-карточки + один крупный объект |

#### B. Фото и editorial

| `cover_family` | Когда | Визуал |
|----------------|-------|--------|
| `editorial_photo` | B2B, экспертиза, доверие | Реалистичное фото + brand color grade 15–25% |
| `lifestyle_candid` | Lifestyle, wellbeing, сервис | «Живое» фото сцены, тёплый свет, bokeh |
| `product_still_life` | E-commerce, физический продукт | Предметная съёмка на фирменном фоне |
| `documentary_reportage` | Кейсы, «как у нас в жизни» | Репортажный кадр, честный свет |
| `portrait_environment` | Личный бренд, эксперт | Человек/силуэт в контексте |
| `macro_detail` | Качество, материалы, craft | Крупный план детали + blur фона в цветах бренда |

#### C. Иллюстрация

| `cover_family` | Когда | Визуал |
|----------------|-------|--------|
| `illustrated_flat` | SaaS, tech, минимализм | Flat vector, 2–3 accent color |
| `isometric_3d` | Продукт, systems | Изометрия, мягкие тени, brand palette |
| `hand_drawn_sketch` | Обучение, brainstorm | Карандаш/маркер, лёгкая шероховатость |
| `gradient_abstract` | AI, future, abstract topics | Градиенты бренда + symbolic object |
| `line_art_minimal` | Premium-minimal, legal/finance | Контурная графика, много воздуха |
| `clay_3d` | Friendly tech, mobile apps | Clay-style 3D, rounded forms |

#### D. Mixed media

| `cover_family` | Когда | Визуал |
|----------------|-------|--------|
| `mixed_media` | Премиум, magazine feel | Фото base + vector + grain |
| `photo_plus_illustration` | Объясняющие статьи | Фото фона + illustrated overlay |
| `duotone_overlay` | Сильный бренд-цвет | Duotone/tint поверх фото или иллюстрации |
| `glassmorphism_card` | Modern UI brands | Frosted card, blur, accent border |

#### E. UI, mockup, product UI

| `cover_family` | Когда | Визуал |
|----------------|-------|--------|
| `ui_mockup` | Софт, automation, tutorials | UI screen в фирменной рамке |
| `device_frame` | Mobile app, tools | Телефон/ноутбук с screen content (без мелкого текста) |
| `dashboard_screenshot` | Analytics, B2B SaaS | Dashboard-style композиция, brand chrome |

#### F. Персонаж и маскот

| `cover_family` | Когда | Визуал |
|----------------|-------|--------|
| `mascot_series` | Есть site mascot | Тот же персонаж, разные позы/props |
| `character_spotlight` | Brand hero без полного сайта | Один character ~60% кадра |
| `icon_story` | Чек-листы, listicles | 3–5 brand icons как визуальная история |

#### G. Инфографика и data-viz

| `cover_family` | Когда | Визуал |
|----------------|-------|--------|
| `infographic_visual` | Guides, comparisons | Одна схема/diagram без мелкого текста |
| `timeline_roadmap` | Program, journey, steps | Дорожная карта, nodes, brand colors |
| `stat_blocks` | Research, trends | Крупные числа как shapes (не readable digits) |

#### H. Текстура и рамки (без текста в PNG)

| `cover_family` | Когда | Визуал |
|----------------|-------|--------|
| `texture_brand` | Premium calm | Subtle pattern + central object |
| `frame_border` | Classic editorial | Фирменная рамка/углы + hero object |
| `split_panel` | Before/after, vs | Две панели 50/50 в brand colors |

### Правила выбора

1. Смотри **hero сайта**, `AURA_ASSET_REGISTRY.json` (mascot?), `AURA_COLOR_PSYCHOLOGY.md`, аудиторию.
2. Не выбирай family, которой **нет** на landing — обложки продолжают сайт, не спорят с ним.
3. Для ниш с **детьми** — избегай photoreal stock лиц; collage / illustration / mascot.
4. Для **local service** — `editorial_photo`, `lifestyle_candid`, `documentary_reportage`.
5. Если темы на 80% how-to по софту — `ui_mockup` или `device_frame`, не cartoon.
6. В CONCEPT.json: `allowed_cover_families_considered[]` — shortlist из 3 slug + краткий отказ от остальных.

### Hybrid (редко)

```json
{
  "cover_family": "brand_collage",
  "cover_family_hybrid_notes": "mascot_series pose rules inside collage layers",
  "secondary_cover_families": [
    { "archetype": "how_to", "cover_family": "ui_mockup", "max_share_of_topics": 2 }
  ]
}
```

Excalibur **не смешивает** families без записи в CONCEPT.

---

## Шаг 2 — Visual lock (что одинаково на КАЖДОЙ обложке)

Зафиксируй в концепте:

- **Формат:** 16:9, 1200×675, safe crop для карточки 400×225 (центр/правило thirds)
- **Палитра:** 1 background + 2–3 accent из design tokens (HEX)
- **Композиция:** например «главный объект справа 55%, слева цветная полоса 20%», «3-panel collage», «center hero + corner blobs»
- **Текстура:** grain, noise, paper — или «clean digital», но одинаково
- **Формы:** радиусы, волны, diagonal cut — из `AURA_SHAPE_MAP.json`
- **Свет:** направление, контраст, тени — одинаковые
- **Запрет:** текст/логотип/watermark в PNG (alt и title — в WP)

**Variable per topic (только это меняется):**

- главный объект/метафора статьи;
- 1–2 второстепенных prop;
- настроение (calm / energetic / caution) в рамках family.

---

## Шаг 3 — Prompt assembly (как Excalibur собирает MCP)

В `AURA_BLOG_COVER_CONCEPT.json`:

```json
{
  "prompt_assembly_mode": "prefix_scene_suffix",
  "global_prompt_prefix": "Brand blog cover 16:9, [family details], colors #HEX #HEX, soft grain, no text...",
  "global_prompt_suffix": "consistent lighting, thumbnail-safe center composition, professional editorial...",
  "global_negative_prompt": "text, letters, watermark, logo, blurry, low quality, generic stock..."
}
```

Per topic в `AURA_BLOG_COVER_PROMPTS.json`:

```json
{
  "topic_id": "B01",
  "topic_archetype": "informational",
  "topic_scene_descriptor": "friendly robot mascot beside laptop, abstract kid learning vibe, lime accent blob",
  "cover_alt_text": "...",
  "use_concept_assembly": true,
  "gpt_image_2_prompt": null
}
```

**Сборка (Excalibur или AURA в phase 2):**

```text
gpt_image_2_prompt =
  concept.global_prompt_prefix
  + " "
  + topic.topic_scene_descriptor
  + " "
  + concept.global_prompt_suffix
```

AURA в phase 2 может записать уже собранный `gpt_image_2_prompt` в JSON — Excalibur проверяет, что prefix/suffix концепта присутствуют (hash или substring check), иначе пересобирает.

---

## Шаг 4 — Style anchor (рекомендуется)

В режиме blog covers AURA генерирует **одну эталонную обложку**:

```text
memory/design/assets/blog-cover-style-anchor.png
```

- промпт = prefix + `neutral brand showcase scene` + suffix;
- в CONCEPT.json: `style_anchor.local_path`, `style_anchor.prompt_used`;
- следующие темы **не копируют картинку**, но обязаны использовать **тот же prefix/suffix и family**.

Если MCP недоступен — `style_anchor.status: skipped`, но concept lock всё равно обязателен.

---

## Шаг 5 — Topic archetypes

Маппинг intent из `blog-topics.md` → сцену **внутри** family:

| Archetype | Scene bias |
|-----------|------------|
| `informational` | один hero object, спокойный фон |
| `how_to` | hands/tool, step metaphor |
| `comparison` | два объекта, split или side-by-side |
| `parent_guide` | trust, safety, warm |
| `news_case` | headline object, dynamic angle |
| `checklist` | icons/cards as collage pieces |

---

## QA — «один стиль»

Design Guardian / Excalibur run log проверяет:

- все covers одного primary `cover_family` (secondary только по CONCEPT);
- slug валиден по `blog-cover-family-registry.json`;
- одинаковые HEX accents (± допустимый drift);
- layout lock соблюдён (object zone не прыгает wild);
- нет текста в PNG;
- grid preview: 6 thumbs рядом выглядят как **серия одного бренда**.

---

## Примеры (Kovcheg Kids)

**Family:** `brand_collage` + элементы `mascot_series`

- Fixed: off-white `#FAFAF7`, lime `#B8FF3C`, pink `#FF3CAC`, yellow `#FFE066`, rounded sticker frames, soft grain, mascot style match hero
- Variable: robot + topic prop (laptop / shield / game icons)
- Collage: 2–3 layered cutouts, overlap, **не** photoreal stock children faces

**Family:** `editorial_photo` (Petman)

- Fixed: warm natural light, green `#2D6A4F` overlay 20%, leash/harness motif subtle
- Variable: dog breed silhouette or walker POV, Moscow park bokeh

AURA выбирает **один** primary per project.
