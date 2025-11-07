# -*- coding: utf-8 -*-
import json
from datetime import datetime
from odoo import http
from odoo.http import request

class GithubReleaseWebhookController(http.Controller):

    @http.route('/github/release-webhook', type='http', auth='public', methods=['POST'], csrf=False)
    def github_release_webhook(self, **kwargs):
        """Endpoint mínimo para recibir el JSON del workflow de GitHub.
        Crea un registro en github.webhook.log con los campos más útiles.
        """
        # Lee el cuerpo como bytes y parsea JSON
        try:
            raw = request.httprequest.data
            payload = json.loads(raw.decode('utf-8')) if raw else (request.jsonrequest or {})
        except Exception:
            payload = request.jsonrequest or {}
            raw = json.dumps(payload).encode("utf-8")

        # Extrae campos esperados (según tu workflow)
        repo = payload.get("repository")
        repo_owner = payload.get("repo_owner")
        pr_number = payload.get("pr_number")
        title = payload.get("title")
        body = payload.get("body")
        html_url = payload.get("html_url")
        state = payload.get("state")
        merged = payload.get("merged")
        merged_at = payload.get("merged_at")
        merged_by = payload.get("merged_by")
        base_branch = payload.get("base_branch")
        head_branch = payload.get("head_branch")
        merge_commit_sha = payload.get("merge_commit_sha")
        labels = payload.get("labels")
        assignees = payload.get("assignees")
        requested_reviewers = payload.get("requested_reviewers")

        # Convert merged_at si viene como string ISO
        merged_at_dt = False
        if isinstance(merged_at, str):
            try:
                merged_at_dt = datetime.fromisoformat(merged_at.replace('Z', '+00:00')).replace(tzinfo=None)
            except Exception:
                merged_at_dt = False

        # Crea el registro
        rec = request.env["github.webhook.log"].sudo().create({
            "name": title,
            "repository": repo,
            "repo_owner": repo_owner,
            "pr_number": pr_number or 0,
            "html_url": html_url,
            "state": state,
            "merged": bool(merged),
            "merged_at": merged_at_dt or False,
            "merged_by": merged_by,
            "base_branch": base_branch,
            "head_branch": head_branch,
            "merge_commit_sha": merge_commit_sha,
            "labels": json.dumps(labels, ensure_ascii=False) if labels is not None else False,
            "assignees": json.dumps(assignees, ensure_ascii=False) if assignees is not None else False,
            "requested_reviewers": json.dumps(requested_reviewers, ensure_ascii=False) if requested_reviewers is not None else False,
            "body": body,
            "raw_payload": raw.decode('utf-8') if isinstance(raw, (bytes, bytearray)) else json.dumps(payload, ensure_ascii=False),
        })

        # Devuelve un JSON mínimo
        headers = [('Content-Type', 'application/json; charset=utf-8')]
        return request.make_response(
            json.dumps({"ok": True, "id": rec.id}),
            headers=headers,
            status=200,
        )