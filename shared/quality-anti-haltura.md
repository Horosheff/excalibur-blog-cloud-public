# Excalibur BLOG Anti-Haltura Quality Standard

Этот файл — жёсткий стандарт качества для агентов Excalibur BLOG.

Если результат нарушает этот стандарт, агент обязан ставить `❌ BLOCKER` или `⚠️ FIXES NEEDED`, а не принимать работу как готовую.

## Абсолютные Блокеры

Страница или сайт не могут считаться готовыми, если есть хотя бы один пункт:

- Текст тонкий: страница выглядит как набросок, а не полноценная посадочная.
- Нет `memory/research/site-research-dossier.md` и связанных research-файлов.
- Сайт использует факты/кейсы/цифры/офферы, которых нет в `fact-bank.md`, brief или `site.inv`.
- Нет обязательных блоков страницы.
- Есть placeholder-фразы: `пример`, `в разработке`, `скоро`, `тест`, `lorem`, `placeholder`, `TODO`, `заглушка`.
- Есть фейковые отзывы, рейтинги, кейсы, цены, гарантии, адреса, лицензии или достижения.
- Есть фраза “пример отзыва”, “пример участника”, “в разработке” в публичной части.
- Hero визуально сломан: заголовок обрезан, слои налезают, CTA уходит за экран, важная картинка обрывается.
- Референс имеет нестандартные шейпы/переходы секций, а сайт заменил их generic прямыми блоками без причины.
- MCP-required visual asset заменён stock/fallback/CSS-заглушкой или не записан в `AURA_ASSET_REGISTRY.json`.
- Референс содержит несколько image-bearing зон, а итоговая страница использует только один hero image.
- `meaningful_image_count` меньше `minimum_homepage_visual_assets` / `minimum_meaningful_image_assets_homepage`.
- Per-page `meaningful_image_count` меньше `minimum_meaningful_image_assets` из `AURA_VISUAL_BUDGET.json` для любой выбранной страницы.
- CSS-карточки, градиенты, blobs или section backgrounds засчитаны как meaningful image assets.
- Design Guardian/QA ставит `✅` без browser paint screenshots 1440/375 по главной и каждой выбранной странице и computed style evidence.
- Design Guardian/QA проверяет screenshot evidence только главной, хотя build содержит внутренние страницы.
- `paint-evidence.json` пишет `pass`, но указанные screenshot-файлы отсутствуют в `memory/wp/paint-qa/`.
- Browser network при fresh navigation/cache-bust не загружает theme CSS/JS/images или содержит только main document.
- Live screenshot выглядит как unstyled/default HTML: bullet-nav, plain links, white hero, default browser spacing.
- Screenshot/computed style evidence противоречит `design-integrity-report.md`.
- `AURA_VISUAL_BUDGET.json` или `AURA_SECTION_BLUEPRINTS.json` отсутствуют при сильном visual reference.
- Visual budget/section blueprints требуют плотный, цветной, игровой/брендовый layout, а live paint выглядит generic/mostly-white/text-heavy.
- Любая внутренняя выбранная страница выглядит как generic/default text template и не наследует visual language AURA.
- `AURA_SOURCE_DECOMPOSITION.json` содержит `must_not`, но итоговый сайт нарушает эти запреты.
- `AURA_VISUAL_INVENTORY.json` отсутствует или содержит required visual zones со статусом не `ready`.
- Required visual asset отсутствует локально в `memory/wp/theme/<theme-slug>/`, даже если live URL отдаёт 200.
- `inc/assets.php` ссылается на файл, которого нет в локальной теме/package.
- Объекту нужен прозрачный фон, но нет результата `recraft_remove_background`.
- Cutout asset в теме скачан с `url`, хотя registry содержит `transparent_url` / `packaged_url`.
- Public HTML содержит MCP/tempfile/remote image URL вместо WordPress Media Library (`/wp-content/uploads/`).
- `wp-media-map.json` отсутствует или `attachment_id` пуст для required asset.
- Meaningful image без `alt_text` или с пустым/generic alt.
- Mobile 375px непригоден: горизонтальный скролл, ломается меню, текст/CTA нечитабельны.
- Sitemap отдаёт не 200 или не XML.
- `robots.txt` содержит staging/test host, неправильный `Host`, неправильный `Sitemap` или блокирует нужные публичные страницы.
- Canonical ведёт не на публичный домен.
- Public URL отличается от домена в robots/canonical/schema.
- Форма заявки видна, но не имеет понятных success/error states, consent или anti-spam.
- Нет стандартной страницы “Политика конфиденциальности”.
- Нет стандартной страницы “Политика cookies”.
- Нет видимого cookie banner с кнопкой принятия cookies.
- Cookie banner не содержит ссылку на `Политика cookies` и `Политика конфиденциальности`.
- Honeypot-поле видно пользователю как обычное поле.
- Видимые breadcrumbs/крошки вверху страницы перекрывают меню, hero или CTA.
- На главной нет полноценного раздела “Блог” с реальными темами из `blog-topics.md`.
- На сайте нет раздела/архива блога и single template для Excalibur статей.
- Финальный отчёт пишет `OK`, хотя часть проверок не выполнялась.

## Минимальная Глубина Страниц

### Главная

Минимум:

- 9 содержательных секций без учёта header/footer.
- 5 000+ знаков полезного текста, если brief не требует короткий сайт.
- H1, подзаголовок, 2 CTA.
- Проблема/боль аудитории.
- Решение и позиционирование.
- Услуги/направления.
- Как проходит работа или обучение.
- Для кого / кому не подходит.
- Доказательства: реальные факты, экспертность, процесс, цифры только если подтверждены.
- FAQ с 6+ вопросами.
- Раздел “Блог” с 3-6 реальными темами из `blog-topics.md`, без заглушек.
- Контакт/форма/CTA.
- Внутренние ссылки на ключевые страницы.

### Коммерческая P0/P1 Страница

Минимум:

- 8 содержательных секций.
- 4 000+ знаков полезного текста.
- H1, интент, кому подходит.
- Описание услуги/продукта.
- Проблемы клиента.
- Что входит.
- Процесс/этапы.
- Результат/выгоды.
- Доказательства без выдумок.
- FAQ 5+.
- CTA.
- 3-8 внутренних ссылок.

### Экспертная / Blog Статья

Минимум:

- 8 000+ знаков для полноценного гайда.
- Чёткая структура H2/H3.
- Answer-блоки 40-60 слов.
- Практические примеры.
- FAQ.
- Вывод и CTA.

## Обязательная Карта Блоков

Каждая страница в `page-content-pack.md`, `site-spec.json` и `build-report.json` должна иметь block inventory:

```text
page_slug:
  required_blocks:
  implemented_blocks:
  missing_blocks:
  text_length_target:
  text_length_actual:
  placeholder_scan:
  internal_links_count:
  blog_section_status:
  visible_top_breadcrumbs_status:
  privacy_policy_status:
  cookies_policy_status:
  cookie_banner_status:
  visual_assets_status:
  visual_inventory_status:
  section_transitions_status:
  visual_budget_status:
  section_blueprints_status:
  meaningful_image_count:
  minimum_meaningful_image_assets:
  visual_gap:
  verdict:
```

`missing_blocks` должен быть пустым для `✅ OK`.

## Отзывы и Социальное Доказательство

Разрешено:

- реальные отзывы с источником;
- реальные кейсы с фактом и ограничениями;
- блок “что получает участник” вместо отзывов, если отзывов нет;
- нейтральный блок “формат поддержки”, “как устроен клуб”, “что внутри”.

Запрещено:

- “пример отзыва”;
- выдуманные имена;
- выдуманные цитаты;
- выдуманные рейтинги;
- schema Review/AggregateRating без реальных данных.

## Технические SEO Блокеры

Финальный QA обязан проверять:

- `/sitemap.xml` возвращает 200 и XML.
- `robots.txt` содержит правильный public host.
- `robots.txt` Sitemap указывает на public domain.
- Нет staging domain в visible HTML, robots, canonical, schema, sitemap.
- Canonical self-referencing для indexable pages.
- 404/search/thank-you utility pages закрыты от индексации.

## Как Отчитываться

Если агент нашёл проблему, он обязан писать:

```text
Статус: ❌ BLOCKER
Причина:
- ...
Что исправить:
- ...
Файл/страница:
- ...
```

Нельзя писать `готово`, `OK`, `production-ready`, если есть блокер выше.