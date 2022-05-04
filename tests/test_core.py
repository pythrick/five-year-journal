from five_year_journal.core.auth import authenticate


async def test_auth_authenticate(faker):
    email = faker.email()
    result = await authenticate(email)
    assert result.access_token is not None
    assert result.refresh_token is not None
