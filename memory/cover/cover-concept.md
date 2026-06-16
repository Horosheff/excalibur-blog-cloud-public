# Cover concept — Excalibur BLOG

Единый визуальный язык обложек. **Excalibur BLOG** сам выбирает и фиксирует `cover_family` при первом прогоне (не AURA).

Machine-readable: `cover-concept.json`  
Реестр семейств: `shared/blog-cover-family-registry.json`  
Методология: `shared/blog-cover-brand-concept.md`

## Fixed (не менять между темами)

- `cover_family` из JSON
- `global_prompt_prefix` / `global_prompt_suffix` / `global_negative_prompt`
- `color_lock`, `composition_lock`

## Variable (на тему)

- `topic_scene_descriptor` в `cover-prompts.json`
- alt-текст обложки

## Сборка промпта MCP

```text
{global_prompt_prefix} + {topic_scene_descriptor} + {global_prompt_suffix}
```

Negative: `global_negative_prompt`

## Style anchor (опционально)

`memory/cover/assets/style-anchor.png` — эталон серии для MCP reference.
