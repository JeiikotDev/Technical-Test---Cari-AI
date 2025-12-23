from app.core.config import Settings, get_settings


class TestSettingsCorsOrigins:
    def test_none_returns_empty_list(self) -> None:
        settings = Settings(cors_origins=None)

        assert settings.cors_origins == []

    def test_empty_string_returns_empty_list(self) -> None:
        settings = Settings(cors_origins="   ")

        assert settings.cors_origins == []

    def test_string_is_split_and_stripped(self) -> None:
        settings = Settings(cors_origins="https://alpha.example.com, https://beta.example.com  ,")

        assert settings.cors_origins == [
            "https://alpha.example.com",
            "https://beta.example.com",
        ]

    def test_list_is_passed_through(self) -> None:
        allowed_origins = ["https://alpha.example.com", "https://beta.example.com"]
        settings = Settings(cors_origins=allowed_origins)

        assert settings.cors_origins == allowed_origins

    def test_unexpected_type_returns_empty_list(self) -> None:
        unexpected_value = 123
        settings = Settings(cors_origins=unexpected_value)

        assert settings.cors_origins == []


class TestSettingsCaching:
    def test_get_settings_is_cached(self) -> None:
        get_settings.cache_clear()

        first_settings = get_settings()
        second_settings = get_settings()

        assert first_settings is second_settings
