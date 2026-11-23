# Quatrogram for iOS

Неподписанная iOS-сборка Quatrogram для сервера gramsrv. IPA собирается полностью в GitHub Actions; локально исходники не хранятся.

- Версия: `13.3.1`
- Тип артефакта: unsigned IPA
- Подпись: пользователь подписывает локально перед установкой

## Сборка

1. Ручной запуск `Import Quatrogram iOS source` — клонирует `iamxvbaba/gramsrv-Telegram-iOS` с подмодулями, применяет брендинг Quatrogram и пушит исходники в `master`.
2. Ручной запуск `Build Quatrogram IPA` — собирает unsigned IPA на macOS-раннере, загружает артефакт `Quatrogram-IPA` и публикует релиз `v13.3.1-ios`.

Прямая ссылка на IPA появится в релизе:

```text
https://github.com/Bobdfog34/Quatrogram-iOS/releases/download/v13.3.1-ios/Quatrogram-13.3.1.ipa
```

## Важно

IPA собран с fake-подписью только для того, чтобы получить установочный архив. Перед установкой на устройство его нужно подписать своим сертификатом и provisioning profile.
