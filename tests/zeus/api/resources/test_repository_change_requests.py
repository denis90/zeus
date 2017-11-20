from zeus import factories


def test_repo_change_request_list(
        client, default_login, default_change_request, default_repo, default_repo_access):
    resp = client.get(
        '/api/repos/{}/change-requests?show=all'.format(
            default_repo.get_full_name())
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]['id'] == str(default_change_request.id)


def test_repo_change_request_list_without_access(
        client, default_login, default_change_request, default_repo):
    resp = client.get(
        '/api/repos/{}/change-requests'.format(default_repo.get_full_name()))
    assert resp.status_code == 404


def test_repo_change_request_list_mine_with_match(
    client, default_login, default_change_request, default_repo, default_repo_access
):
    resp = client.get(
        '/api/repos/{}/change-requests?show=mine'.format(default_repo.get_full_name()))
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1


def test_repo_change_request_list_mine_without_match(
    client, default_login, default_repo, default_repo_access
):
    revision = factories.RevisionFactory(repository=default_repo)
    source = factories.SourceFactory(revision=revision)
    factories.BuildFactory(source=source)
    resp = client.get(
        '/api/repos/{}/change-requests?show=mine'.format(default_repo.get_full_name()))
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 0
